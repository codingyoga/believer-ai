from datetime import datetime
import sqlite3
from models import Goals, Goal
from typing import List 

def init_db():
    with sqlite3.connect('app.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            hours_logged INTEGER NOT NULL,
            date TEXT NOT NULL,
            user_input TEXT
        );
        ''')
        conn.commit()

def insert_goal(goal: dict, db_path='app.db'):
    # Extract data
    title = goal['title']
    hours_logged = goal['hours_logged']
    date = datetime.now().strftime("%Y-%m-%d") if goal['date'].lower() == "today" else goal['date']
    user_input = goal['user_input']

    # Insert into database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO goals (title, hours_logged, date, user_input)
            VALUES (?, ?, ?, ?)
        """, (title, hours_logged, date, user_input))
        conn.commit()

def fetch_goals(db_path='app.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, hours_logged, date, user_input FROM goals
        """)
        rows = cursor.fetchall()
        return [Goal(id=row[0], title=row[1], hours_logged=row[2], date=row[3], user_input=row[4]) for row in rows]

def drop_table(db_path='app.db', table_name='goals'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        print(f"Table '{table_name}' has been deleted.")

#drop_table()
init_db()