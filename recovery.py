import json
import sqlite3
from datetime import datetime

DB_FILE = "journal.db"
NEGATIVE_EMOTIONS = {"anxious", "sad", "angry", "frustrated", "overwhelmed", "disappointed"}

def is_negative(entry):
    """
    Returns True if intensity is medium/high and any emotion is negative.
    """
    if isinstance(entry, dict):
        intensity = entry.get('intensity', 'low').lower()
        emotions_val = entry.get('emotions', [])
    else:
        intensity = entry['intensity'].lower()
        emotions_val = entry['emotions']
        
    if intensity not in ["medium", "high"]:
        return False
        
    # Handle JSON string parsing if reading directly from SQLite row
    if isinstance(emotions_val, str):
        try:
            emotions = json.loads(emotions_val)
        except Exception:
            emotions = []
    else:
        emotions = emotions_val
        
    for e in emotions:
        if e.lower() in NEGATIVE_EMOTIONS:
            return True
            
    return False

def get_next_day(created_at_str):
    """
    Finds the earliest entry within 48 hours after the given timestamp.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get the very next entry
    cursor.execute('SELECT * FROM entries WHERE created_at > ? ORDER BY created_at ASC LIMIT 1', (created_at_str,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        fmt = "%Y-%m-%d %H:%M:%S"
        try:
            t1 = datetime.strptime(created_at_str, fmt)
            t2 = datetime.strptime(row['created_at'], fmt)
            
            # Ensure it is strictly within 48 hours
            if (t2 - t1).total_seconds() <= 48 * 3600:
                return dict(row)
        except Exception:
            return dict(row) # Fallback if time parsing fails
            
    return None
