#!/usr/bin/env python3
"""
Database setup script for Attendance Management System
Run this script to create the database and tables
"""

import pymysql
from app import app, db

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',  # Change this to your MySQL password
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_system")
            print("✅ Database 'attendance_system' created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    finally:
        if 'connection' in locals():
            connection.close()
    
    return True

def create_tables():
    """Create all tables in the database"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully!")
            return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    print("🚀 Setting up Attendance Management System Database...")
    print("=" * 50)
    
    # Step 1: Create database
    if not create_database():
        print("❌ Failed to create database. Please check your MySQL connection.")
        return
    
    # Step 2: Create tables
    if not create_tables():
        print("❌ Failed to create tables. Please check your database configuration.")
        return
    
    print("=" * 50)
    print("🎉 Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Update the database credentials in app.py if needed")
    print("2. Run: python app.py")
    print("3. Open your browser and go to: http://localhost:5000")

if __name__ == "__main__":
    main()
