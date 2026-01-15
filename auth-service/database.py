"""
Auth Service - Database Module
Shared database for authentication
"""

import sqlite3
import os
from datetime import datetime

# Shared database file mounted via Docker volume at /data
DB_PATH = os.path.join('/data', 'saas_control_panel.db')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(username, email, password):
    """Create a new user"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return {'success': False, 'error': 'Username already exists'}
        else:
            return {'success': False, 'error': 'Email already exists'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def update_last_login(user_id):
    """Update last login timestamp"""
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """List all active users (id, username, email)"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, username, email FROM users WHERE is_active = 1')
    users = [dict(row) for row in c.fetchall()]
    conn.close()
    return users
