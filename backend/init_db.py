import sqlite3
from datetime import datetime, timedelta

def create_sqlite_database(filename):
    """Create a database connection to an SQLite database and create the table."""
    conn = None
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS DH11 (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                humidity INTEGER NOT NULL,
                temperature INTEGER NOT NULL
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_data(filename, humidity, temperature):
    """Insert a new record into the DH11."""
    conn = None
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute('''
            INSERT INTO DH11 (humidity, temperature)
            VALUES (?, ?)
        ''', (humidity, temperature))
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def delete_old_data(filename):
    """Delete records older than 24 hours from the database."""
    conn = None
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute('''
            DELETE FROM DH11
            WHERE timestamp <= datetime('now', '-1 day')
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_sqlite_database("sensor.db")
    delete_old_data("sensor.db")
    insert_data("sensor.db", 55, 22)
