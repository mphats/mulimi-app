#!/usr/bin/env python3
"""
MySQL Database Setup Script for Agri AI Backend
This script helps you set up the MySQL database for your Django project.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def create_database():
    """Create the MySQL database if it doesn't exist."""
    
    # Load environment variables
    load_dotenv()
    
    # Get database configuration from environment
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'agri_ai_db')
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{db_name}' created successfully or already exists!")
            
            # Show existing databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("\n📋 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            cursor.close()
            connection.close()
            print(f"\n🎉 MySQL setup completed successfully!")
            print(f"   Database: {db_name}")
            print(f"   Host: {db_host}")
            print(f"   Port: {db_port}")
            print(f"   User: {db_user}")
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure MySQL server is running")
        print("   2. Check your MySQL credentials in .env file")
        print("   3. Ensure MySQL user has CREATE DATABASE privileges")
        print("   4. Try connecting manually: mysql -u root -p")

def test_connection():
    """Test the database connection with the specified database."""
    
    load_dotenv()
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', 3306))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'agri_ai_db')
    
    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        if connection.is_connected():
            print(f"✅ Successfully connected to database '{db_name}'!")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"   MySQL Server version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database = cursor.fetchone()
            print(f"   Current database: {database[0]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error connecting to database '{db_name}': {e}")
        return False

if __name__ == "__main__":
    print("🚀 MySQL Database Setup for Agri AI Backend")
    print("=" * 50)
    
    # Create database
    create_database()
    
    print("\n" + "=" * 50)
    
    # Test connection
    print("🧪 Testing database connection...")
    test_connection()
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("   1. Run: python manage.py makemigrations")
    print("   2. Run: python manage.py migrate")
    print("   3. Run: python manage.py runserver")
    print("   4. Test your login page at: http://127.0.0.1:8000/login/")
