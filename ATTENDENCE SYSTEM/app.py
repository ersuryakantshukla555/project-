from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with attendance
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    students = Student.query.order_by(Student.roll_no).all()
    return render_template('students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        name = request.form['name']
        section = request.form['section']
        
        # Check if roll number already exists
        existing_student = Student.query.filter_by(roll_no=roll_no).first()
        if existing_student:
            flash('Student with this roll number already exists!', 'error')
            return redirect(url_for('add_student'))
        
        student = Student(roll_no=roll_no, name=name, section=section)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.roll_no = request.form['roll_no']
        student.name = request.form['name']
        student.section = request.form['section']
        
        # Check if roll number already exists (excluding current student)
        existing_student = Student.query.filter(
            Student.roll_no == request.form['roll_no'],
            Student.id != student_id
        ).first()
        if existing_student:
            flash('Student with this roll number already exists!', 'error')
            return redirect(url_for('edit_student', student_id=student_id))
        
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students'))
    
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/attendance')
def attendance():
    students = Student.query.order_by(Student.roll_no).all()
    return render_template('attendance.html', students=students)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    date_str = request.form['date']
    attendance_data = request.form.getlist('attendance')
    
    # Convert date string to date object
    attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Get all students
    students = Student.query.all()
    
    for student in students:
        # Check if attendance already exists for this date
        existing_attendance = Attendance.query.filter_by(
            student_id=student.id, 
            date=attendance_date
        ).first()
        
        # Determine status (Present if student_id in attendance_data, else Absent)
        status = 'Present' if str(student.id) in attendance_data else 'Absent'
        
        if existing_attendance:
            existing_attendance.status = status
        else:
            attendance = Attendance(
                student_id=student.id,
                date=attendance_date,
                status=status
            )
            db.session.add(attendance)
    
    db.session.commit()
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('attendance'))

@app.route('/view_attendance')
def view_attendance():
    date_filter = request.args.get('date')
    section_filter = request.args.get('section')
    
    query = db.session.query(Attendance, Student).join(Student)
    
    if date_filter:
        query = query.filter(Attendance.date == datetime.strptime(date_filter, '%Y-%m-%d').date())
    
    if section_filter:
        query = query.filter(Student.section == section_filter)
    
    attendance_records = query.order_by(Student.roll_no, Attendance.date).all()
    
    # Get unique dates and sections for filters
    dates = db.session.query(Attendance.date).distinct().order_by(Attendance.date.desc()).all()
    sections = db.session.query(Student.section).distinct().order_by(Student.section).all()
    
    return render_template('view_attendance.html', 
                         attendance_records=attendance_records,
                         dates=[d[0] for d in dates],
                         sections=[s[0] for s in sections])

@app.route('/export_excel')
def export_excel():
    # Get all attendance records with student information
    records = db.session.query(Attendance, Student).join(Student).order_by(Student.roll_no, Attendance.date).all()
    
    # Create DataFrame
    data = []
    for attendance, student in records:
        data.append({
            'Roll No': student.roll_no,
            'Name': student.name,
            'Section': student.section,
            'Date': attendance.date.strftime('%Y-%m-%d'),
            'Status': attendance.status
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    filename = f'attendance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    # Prefer configurable export directory, fall back to local 'exports', then '/tmp/exports'
    preferred_dir = os.environ.get('EXPORT_DIR', 'exports')
    export_dir = preferred_dir
    try:
        os.makedirs(export_dir, exist_ok=True)
        test_path = os.path.join(export_dir, '.write_test')
        with open(test_path, 'w') as f:
            f.write('ok')
        os.remove(test_path)
    except Exception:
        export_dir = os.path.join('/tmp', 'exports')
        os.makedirs(export_dir, exist_ok=True)
    
    filepath = os.path.join(export_dir, filename)
    df.to_excel(filepath, index=False, sheet_name='Attendance Report')
    
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
