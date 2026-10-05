import os
import sqlite3
from datetime import datetime

# Database path in backend directory
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'history.db')

def get_connection():
    """Returns a SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the predictions table in SQLite if it does not exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL,
            image_data TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[INFO] SQLite Database initialized at '{DB_PATH}'")

def insert_prediction(filename, predicted_class, confidence, image_data=None):
    """Inserts a new prediction record into SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO predictions (filename, predicted_class, confidence, timestamp, image_data)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, predicted_class, float(confidence), timestamp_str, image_data))
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": prediction_id,
        "filename": filename,
        "predicted_class": predicted_class,
        "confidence": round(float(confidence), 2),
        "timestamp": timestamp_str,
        "image_data": image_data
    }

def get_all_predictions():
    """Retrieves all stored prediction records ordered by newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, filename, predicted_class, confidence, timestamp, image_data
        FROM predictions
        ORDER BY id DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    predictions = []
    for r in rows:
        predictions.append({
            "id": r["id"],
            "filename": r["filename"],
            "predicted_class": r["predicted_class"],
            "confidence": round(r["confidence"], 2),
            "timestamp": r["timestamp"],
            "image_data": r["image_data"]
        })
    return predictions

def delete_all_predictions():
    """Clears all records from the predictions table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM predictions')
    conn.commit()
    conn.close()
    return True
