"""
SaaS Control Panel - Database Module
SQLite database for users, containers, activity logs, and metrics
"""

import sqlite3
import os
from datetime import datetime, timedelta
import json

# Use a shared Docker volume for the database so multiple services can access it
# The volume will be mounted at /data in the containers
DB_PATH = os.path.join('/data', 'saas_control_panel.db')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Containers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS containers (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            container_id TEXT UNIQUE NOT NULL,
            container_name TEXT NOT NULL,
            port INTEGER,
            status TEXT DEFAULT 'created',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_started TIMESTAMP,
            last_stopped TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Activity logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            container_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (container_id) REFERENCES containers(id)
        )
    ''')
    
    # Metrics table (for performance tracking)
    c.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY,
            container_id INTEGER NOT NULL,
            cpu_percent REAL,
            memory_percent REAL,
            network_in INTEGER,
            network_out INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (container_id) REFERENCES containers(id)
        )
    ''')
    
    # Create indexes for better performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_containers_user_id ON containers(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON activity_logs(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_metrics_container_id ON metrics(container_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)')
    
    conn.commit()
    conn.close()

# ============================================
# USER OPERATIONS
# ============================================

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
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'Username or email already exists'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    """Get all users"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, username, email, created_at FROM users WHERE is_active = 1')
    users = [dict(row) for row in c.fetchall()]
    conn.close()
    return users

def update_last_login(user_id):
    """Update last login timestamp"""
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# ============================================
# CONTAINER OPERATIONS
# ============================================

def create_container(user_id, container_id, container_name, port):
    """Create container record in database"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO containers (user_id, container_id, container_name, port, status)
            VALUES (?, ?, ?, ?, 'created')
        ''', (user_id, container_id, container_name, port))
        conn.commit()
        container_pk = c.lastrowid
        conn.close()
        
        # Log activity
        log_activity(user_id, container_pk, 'container_created', f'Created container {container_name}')
        
        return {'success': True, 'container_id': container_pk}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_user_containers(user_id):
    """Get all containers for a user"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, container_id, container_name, port, status, 
               created_at, last_started, last_stopped 
        FROM containers 
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    containers = [dict(row) for row in c.fetchall()]
    conn.close()
    return containers

def get_all_containers():
    """Get all containers (for admin)"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.container_id, c.container_name, c.port, c.status,
               c.created_at, c.last_started, u.username, u.id as user_id
        FROM containers c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
    ''')
    containers = [dict(row) for row in c.fetchall()]
    conn.close()
    return containers

def get_container_by_name(container_name):
    """Get a single container record by its stored name"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.container_id, c.container_name, c.port, c.status,
               c.created_at, c.last_started, c.last_stopped, u.username, u.id as user_id
        FROM containers c
        JOIN users u ON c.user_id = u.id
        WHERE c.container_name = ?
    ''', (container_name,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_container_status(container_id, status):
    """Update container status"""
    conn = get_db()
    c = conn.cursor()
    
    if status == 'running':
        c.execute('UPDATE containers SET status = ?, last_started = CURRENT_TIMESTAMP WHERE id = ?', 
                 (status, container_id))
    elif status == 'stopped':
        c.execute('UPDATE containers SET status = ?, last_stopped = CURRENT_TIMESTAMP WHERE id = ?', 
                 (status, container_id))
    else:
        c.execute('UPDATE containers SET status = ? WHERE id = ?', (status, container_id))
    
    conn.commit()
    conn.close()

def delete_container(container_id):
    """Delete container record"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM containers WHERE id = ?', (container_id,))
    conn.commit()
    conn.close()

# ============================================
# ACTIVITY LOG OPERATIONS
# ============================================

def log_activity(user_id, container_id, action, details):
    """Log an activity"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO activity_logs (user_id, container_id, action, details)
        VALUES (?, ?, ?, ?)
    ''', (user_id, container_id, action, details))
    conn.commit()
    conn.close()

def get_user_activity_logs(user_id, limit=50):
    """Get activity logs for a user"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, action, details, timestamp
        FROM activity_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))
    logs = [dict(row) for row in c.fetchall()]
    conn.close()
    return logs

def get_all_activity_logs(limit=100):
    """Get all activity logs (for admin)"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT al.id, u.username, al.action, al.details, al.timestamp
        FROM activity_logs al
        LEFT JOIN users u ON al.user_id = u.id
        ORDER BY al.timestamp DESC
        LIMIT ?
    ''', (limit,))
    logs = [dict(row) for row in c.fetchall()]
    conn.close()
    return logs

# ============================================
# METRICS OPERATIONS
# ============================================

def store_metric(container_id, cpu_percent, memory_percent, network_in=0, network_out=0):
    """Store container metric"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO metrics (container_id, cpu_percent, memory_percent, network_in, network_out)
        VALUES (?, ?, ?, ?, ?)
    ''', (container_id, cpu_percent, memory_percent, network_in, network_out))
    conn.commit()
    conn.close()

def get_container_metrics(container_id, hours=7):
    """Get metrics for a container (last N hours)"""
    conn = get_db()
    c = conn.cursor()
    
    since = datetime.now() - timedelta(hours=hours)
    c.execute('''
        SELECT cpu_percent, memory_percent, network_in, network_out, timestamp
        FROM metrics
        WHERE container_id = ? AND timestamp > ?
        ORDER BY timestamp ASC
    ''', (container_id, since.isoformat()))
    
    metrics = [dict(row) for row in c.fetchall()]
    conn.close()
    return metrics

def get_container_stats(container_id):
    """Get aggregated stats for a container"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('''
        SELECT 
            AVG(cpu_percent) as avg_cpu,
            MAX(cpu_percent) as max_cpu,
            AVG(memory_percent) as avg_memory,
            MAX(memory_percent) as max_memory
        FROM metrics
        WHERE container_id = ? AND timestamp > datetime('now', '-7 days')
    ''', (container_id,))
    
    stats = dict(c.fetchone() or {})
    conn.close()
    return stats

# ============================================
# STATISTICS
# ============================================

def get_admin_stats():
    """Get admin dashboard statistics"""
    conn = get_db()
    c = conn.cursor()
    
    # Total users
    c.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1')
    total_users = c.fetchone()['count']
    
    # Total containers
    c.execute('SELECT COUNT(*) as count FROM containers')
    total_containers = c.fetchone()['count']
    
    # Running containers
    c.execute("SELECT COUNT(*) as count FROM containers WHERE status = 'running'")
    running_containers = c.fetchone()['count']
    
    # Failed containers
    c.execute("SELECT COUNT(*) as count FROM containers WHERE status = 'error'")
    failed_containers = c.fetchone()['count']
    
    # Average uptime
    c.execute('''
        SELECT 
            AVG(CAST((julianday('now') - julianday(created_at)) AS FLOAT)) as avg_days_active
        FROM containers
        WHERE status = 'running'
    ''')
    result = c.fetchone()
    avg_uptime_days = result['avg_days_active'] or 0
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_containers': total_containers,
        'running_containers': running_containers,
        'failed_containers': failed_containers,
        'avg_uptime_days': round(avg_uptime_days, 2)
    }

# Initialize database on import
init_db()
