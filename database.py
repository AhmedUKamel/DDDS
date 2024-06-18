from datetime import datetime
import sqlite3
import bcrypt

DATABASE_NAME = "driver_drowsiness_detection.db"

def initialize_tables():
    """Initialize the database tables"""

    initialize_users_table()
    initialize_prediction_events_table()

def initialize_users_table():
    """Initialize the SQLite database for storing system users."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def register_user(username, password):
    """Register a new user with a username and password."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, password))

        connection.commit()
        connection.close()

        return True

    except Exception:
        return False

def login_user(username, password):
    """Login a user by checking the username and password."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password FROM users WHERE username = ?
    """, (username,))
    result = cursor.fetchone()

    connection.commit()
    connection.close()

    return result and bcrypt.checkpw(password.encode('utf-8'), result[0])

def initialize_prediction_events_table():
    """Initialize the SQLite database for storing drowsiness events."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_events (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            ear_value REAL,
            is_drowsy INTEGER NOT NULL CHECK (is_drowsy IN (0, 1)),
            username TEXT,

            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)

    connection.commit()
    connection.close()

def insert_prediction_event(ear_value, username):
    """Insert a drowsiness event to the SQLite database."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO prediction_events (timestamp, ear_value, username)
        VALUES (?, ?, ?)
    """, (timestamp, ear_value, username))

    connection.commit()
    connection.close()