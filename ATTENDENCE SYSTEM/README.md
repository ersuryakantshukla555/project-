# College Attendance Management System

A comprehensive web-based attendance management system built with Python Flask, MySQL, and Bootstrap. This system allows you to manage student information, mark daily attendance, and export data to Excel format.

## Features

### Student Management
- ✅ Add new students with roll number, name, and section
- ✅ Edit existing student information
- ✅ Delete students from the system
- ✅ Sort students by roll number
- ✅ Unique roll number validation

### Attendance Tracking
- ✅ Mark daily attendance for all students
- ✅ Present/Absent status tracking
- ✅ Date-based attendance records
- ✅ MySQL database storage

### Data Export
- ✅ Export attendance data to Excel format
- ✅ Comprehensive attendance reports
- ✅ Filter and view attendance history

### User Interface
- ✅ Modern, responsive Bootstrap design
- ✅ Mobile-friendly interface
- ✅ Intuitive navigation
- ✅ Real-time feedback with flash messages

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Data Export**: Pandas, OpenPyXL
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package installer)

### Step 1: Clone/Download the Project
```bash
# Navigate to your project directory
cd "ATTENDENCE SYSTEM"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup
1. Make sure MySQL is running on your system
2. Update database credentials in `app.py` if needed:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/attendance_system'
   ```
3. Run the database setup script:
   ```bash
   python database_setup.py
   ```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the System
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### 1. Adding Students
- Click on "Students" in the navigation menu
- Click "Add New Student" button
- Fill in the student details (Roll No, Name, Section)
- Click "Add Student"

### 2. Managing Students
- View all students in the student list
- Edit student information using the "Edit" button
- Delete students using the "Delete" button
- Students are automatically sorted by roll number

### 3. Marking Attendance
- Click on "Mark Attendance" in the navigation
- Select the date for attendance
- Check the boxes for present students
- Use "Select All" or "Deselect All" for convenience
- Click "Save Attendance"

### 4. Viewing Attendance Records
- Click on "View Attendance" to see all records
- Filter by date or section using the filter options
- View attendance status for each student

### 5. Exporting Data
- Click "Export to Excel" to download attendance data
- The Excel file will contain all attendance records with student information

## Database Schema

### Students Table
- `id`: Primary key
- `roll_no`: Unique roll number
- `name`: Student's full name
- `section`: Student's section (A, B, C, D)
- `created_at`: Record creation timestamp

### Attendance Table
- `id`: Primary key
- `student_id`: Foreign key to students table
- `date`: Attendance date
- `status`: Present or Absent
- `created_at`: Record creation timestamp

## Configuration

### Database Configuration
Update the database connection string in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/attendance_system'
```

### Security
- Change the SECRET_KEY in `app.py` for production use
- Use environment variables for sensitive information
- Implement proper authentication for production deployment

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL server is running
   - Check database credentials
   - Verify database exists

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Port Already in Use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions, please create an issue in the project repository.

---

**Note**: This system is designed for educational purposes. For production use, implement proper security measures, authentication, and data backup strategies.
# attendence-management-system-2025
