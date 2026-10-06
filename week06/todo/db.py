import sqlite3
import os

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "todo.db")


def get_connection(db_path=None):
    if db_path is None:
        db_path = DEFAULT_DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_connection(db_path)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


def get_todos(db_path=None):
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("""
            SELECT id, title, done, created_at
            FROM todos
            ORDER BY done ASC, id DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_todo(todo_id, db_path=None):
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def add_todo(title, db_path=None):
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("INSERT INTO todos (title, done) VALUES (?, 0)", (title,))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def toggle_todo(todo_id, db_path=None):
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("SELECT done FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        new_done = 0 if row["done"] else 1
        conn.execute("UPDATE todos SET done = ? WHERE id = ?", (new_done, todo_id))
        conn.commit()
        return True
    finally:
        conn.close()


def delete_todo(todo_id, db_path=None):
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
