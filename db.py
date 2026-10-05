import sqlite3
import json
from datetime import datetime

DB_FILE = "journal.db"

def init_db():
    """Create the entries table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw TEXT,
            event TEXT,
            situation TEXT,
            emotions TEXT,
            intensity TEXT,
            triggers TEXT,
            created_at TIMESTAMP,
            entities TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            value TEXT,
            mention_count INTEGER DEFAULT 1,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            evidence TEXT
        )
    ''')
    # Handle migration for existing entries table (add entities column if it doesn't exist)
    try:
        cursor.execute('ALTER TABLE entries ADD COLUMN entities TEXT')
    except sqlite3.OperationalError:
        pass # Column already exists
    conn.commit()
    conn.close()

def insert_entry(raw, event, situation, emotions, intensity, triggers, created_at=None):
    """Insert a new journal entry into the database."""
    if created_at is None:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO entries (raw, event, situation, emotions, intensity, triggers, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (raw, event, situation, json.dumps(emotions), intensity, json.dumps(triggers), created_at))
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return entry_id

def get_all_entries():
    """Retrieve all entries ordered by date descending (newest first)."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_next_day_entry(created_at_str):
    """Retrieve the first entry strictly after the given date to see what happened next."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE created_at > ? ORDER BY created_at ASC LIMIT 1', (created_at_str,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
def upsert_preferences(prefs):
    """Insert or increment preference mention counts."""
    if not prefs:
        return
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for p in prefs:
        cat = p.get('category', '')
        val = p.get('value', '')
        evi = p.get('evidence', '')
        
        cursor.execute('SELECT id, mention_count FROM preferences WHERE category=? AND value=?', (cat, val))
        row = cursor.fetchone()
        if row:
            cursor.execute('UPDATE preferences SET mention_count=?, last_seen=?, evidence=? WHERE id=?', (row[1]+1, now, evi, row[0]))
        else:
            cursor.execute('''
                INSERT INTO preferences (category, value, mention_count, first_seen, last_seen, evidence) 
                VALUES (?, ?, 1, ?, ?, ?)
            ''', (cat, val, now, now, evi))
    conn.commit()
    conn.close()

def get_top_preferences():
    """Get the most mentioned preferences (cap 12, min 2)."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM preferences WHERE mention_count >= 2 ORDER BY mention_count DESC LIMIT 12')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_entry_entities(entry_id, entities_json):
    """Save extracted entities back to an existing entry."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE entries SET entities=? WHERE id=?', (entities_json, entry_id))
    conn.commit()
    conn.close()
