import sqlite3
import datetime
from typing import List, Dict, Any

def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        date_created TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )""")
   
    # Intervals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intervals (
        interval_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        interval_days INTEGER NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )""")
    
    # Reminders log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminder_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        reminder_date TEXT,
        status TEXT,
        FOREIGN KEY (task_id) REFERENCES tasks(task_id)
    )""")
   
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def insert_task(task_name: str, intervals: List[int]) -> int:
    """Insert a new task with its intervals."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    try:
        # Insert task
        date_created = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO tasks (task_name, date_created) VALUES (?, ?)
        """, (task_name, date_created))
       
        task_id = cursor.lastrowid
        
        # Insert intervals
        for interval_days in intervals:
            cursor.execute("""
            INSERT INTO intervals (task_id, interval_days) VALUES (?, ?)
            """, (task_id, interval_days))
        
        conn.commit()
        return task_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_tasks() -> Dict[int, Dict[str, Any]]:
    """Retrieve all tasks with their intervals."""
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.task_id, t.task_name, t.date_created, t.is_active, i.interval_days 
        FROM tasks t
        LEFT JOIN intervals i ON t.task_id = i.task_id
        WHERE t.is_active = 1
        ORDER BY t.task_id, i.interval_days
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    tasks = {}
    for task_id, task_name, date_created, is_active, interval_days in rows:
        if task_id not in tasks:
            tasks[task_id] = {
                "task_name": task_name,
                "date_created": date_created,
                "is_active": bool(is_active),
                "intervals": []
            }
        if interval_days is not None:
            tasks[task_id]["intervals"].append(interval_days)
    
    return tasks

def deactivate_task(task_id: int):
    """Deactivate a task (soft delete)."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE tasks SET is_active = 0 WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()

def log_reminder(task_id: int, status: str):
    """Log when a reminder was sent."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO reminder_log (task_id, reminder_date, status) 
    VALUES (?, ?, ?)
    """, (task_id, datetime.datetime.now().isoformat(), status))
    
    conn.commit()
    conn.close()