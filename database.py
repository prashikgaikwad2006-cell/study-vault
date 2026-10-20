import sqlite3
import os
import shutil
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

if os.environ.get('VERCEL'):
    DB_PATH = '/tmp/studyvault.db'
    bundled_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'studyvault.db')
    if not os.path.exists(DB_PATH) and os.path.exists(bundled_db):
        try:
            shutil.copyfile(bundled_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'studyvault.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. users table (matches PDF Section 3.3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. courses table (matches PDF Section 3.3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name VARCHAR(120) NOT NULL,
            course_code VARCHAR(30) UNIQUE NOT NULL,
            description TEXT
        )
    ''')

    # 3. subjects table (matches PDF Section 3.3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            subject_name VARCHAR(120) NOT NULL,
            subject_code VARCHAR(30) NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
        )
    ''')

    # 4. study_materials table (matches PDF Section 3.3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS study_materials (
            material_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            uploaded_by INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            file_name VARCHAR(255) NOT NULL,
            file_path TEXT NOT NULL,
            file_type VARCHAR(30) NOT NULL,
            file_size VARCHAR(50) DEFAULT '1.2 MB',
            category VARCHAR(50) DEFAULT 'Lecture Notes',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE,
            FOREIGN KEY (uploaded_by) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')

    # 5. downloads table (matches PDF Section 3.3)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            download_id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            user_id INTEGER,
            downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES study_materials (material_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE SET NULL
        )
    ''')

    # 6. bookmarks / favorites table for enhanced student UX
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            bookmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(material_id, user_id),
            FOREIGN KEY (material_id) REFERENCES study_materials (material_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("StudyVault Database initialized successfully.")
