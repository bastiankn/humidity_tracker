import sqlite3
import pandas as pd

# Construct the path to the database file in the backend directory
db_filename = "backend/sensor.db"

def create_sqlite_database(filename):
    """Creates a connection to an SQLite database file and sets up a table to store the sensor data."""
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
    """Inserts a new record of humidity and temperature data into the database."""
    conn = None
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute('''
            INSERT INTO DH11 (humidity, temperature, timestamp)
            VALUES (?, ?, datetime('now'))
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
        print("Deleted old records")
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def fetch_all_data(db_name):
    '''Fetches all records from the DH11 table and returns them as a pandas DataFrame.'''
    conn = sqlite3.connect(db_name)
    query = "SELECT * FROM DH11"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == '__main__':
    '''In order to delete the records older than 24hrs the python file needs to be run'''
    create_sqlite_database(db_filename)
    delete_old_data(db_filename)
