import sqlite3
import json
from datetime import datetime, timedelta

DB_FILE = "journal.db"

# Raw entries stored as a list of dicts for easy editing
# Persona: Ananya, 2nd-year VIT Chennai student
DEMO_ENTRIES = [
    # --- CYCLE 1: Assessment -> Comparison -> Anxiety -> Recovery ---
    {"raw": "Just had my OS cat-1 exam. The paper was so weird. Not sure if I even passed.", "event": "OS CAT-1 Exam", "situation": "Felt uncertain after taking the OS exam.", "emotions": ["anxious"], "intensity": "high", "triggers": ["exam performance"]},
    {"raw": "Everyone outside the exam hall was discussing answers. They all got completely different stuff than me. I feel like an idiot.", "event": "Discussing exam answers", "situation": "Compared exam answers with classmates and felt stupid.", "emotions": ["sad", "overwhelmed"], "intensity": "high", "triggers": ["comparison with peers", "fear of falling behind"]},
    {"raw": "Can't stop thinking about that exam. Why am I always the one struggling while everyone else gets it easily? Im so annoyed with myself.", "event": "Post-exam self-criticism", "situation": "Ruminating over exam performance and comparing myself to others.", "emotions": ["frustrated", "angry"], "intensity": "high", "triggers": ["self-criticism", "comparison with peers"]},
    {"raw": "Talked to Priya from my hostel block. She was struggling too. We decided to study together next time. Feeling a bit lighter.", "event": "Talked to a friend", "situation": "Shared exam stress with a friend and made a study plan.", "emotions": ["calm"], "intensity": "medium", "triggers": ["talking to a friend", "making a plan"]},
    {"raw": "Woke up feeling okay today. Just did my laundry and watched some Netflix. Much needed chill day.", "event": "Chill day", "situation": "Relaxed and did chores.", "emotions": ["calm"], "intensity": "low", "triggers": ["rest"]},
    
    # --- HAPPY ---
    {"raw": "Had biryani at the food court today with the whole gang. We laughed so much my stomach hurts.", "event": "Biryani with friends", "situation": "Ate good food with friends and laughed a lot.", "emotions": ["happy", "excited"], "intensity": "high", "triggers": ["friends", "good food"]},
    {"raw": "Joined the new robotics club! The seniors seem super cool and I'm pumped to build something.", "event": "Joined robotics club", "situation": "Joined a new club and met cool seniors.", "emotions": ["excited"], "intensity": "medium", "triggers": ["club event", "new experiences"]},
    
    # --- TIRED / BURNOUT ---
    {"raw": "8 AM classes should be illegal. I barely slept and the prof just droned on for an hour and a half.", "event": "Boring morning class", "situation": "Attended an early class on no sleep.", "emotions": ["numb", "frustrated"], "intensity": "medium", "triggers": ["lack of sleep", "boring class"]},
    
    # --- CYCLE 2 ---
    {"raw": "Data Structures lab assessment was today. My code kept throwing a segmentation fault. Barely submitted something.", "event": "DSA Lab Assessment", "situation": "Struggled with coding errors during lab.", "emotions": ["anxious", "frustrated"], "intensity": "high", "triggers": ["exam performance", "coding error"]},
    {"raw": "Looked at Rahul's screen and his code was running perfectly. Im definitely going to get a lower grade. Just feel so behind everyone.", "event": "Saw peer's working code", "situation": "Noticed classmate's code working while mine failed.", "emotions": ["sad", "disappointed"], "intensity": "high", "triggers": ["comparison with peers", "fear of falling behind"]},
    {"raw": "I literally can't code. I don't know why I took CS. I feel so dumb compared to the rest of the batch.", "event": "Imposter syndrome", "situation": "Felt intense imposter syndrome after a bad lab.", "emotions": ["sad", "overwhelmed"], "intensity": "high", "triggers": ["self-criticism", "comparison with peers"]},
    {"raw": "Went for a walk around the campus lake. Listened to some music. Realized it's just one lab and I can practice more.", "event": "Campus walk", "situation": "Took a walk to clear my head.", "emotions": ["calm"], "intensity": "medium", "triggers": ["going for a walk", "music"]},
    
    # --- NEUTRAL ---
    {"raw": "Just a normal Tuesday. Classes, lunch, more classes. Nothing special happened.", "event": "Normal day", "situation": "Had a regular, uneventful day.", "emotions": ["calm"], "intensity": "low", "triggers": ["routine"]},
    {"raw": "Wifi went down in the hostel so I actually read a book for once. Not bad.", "event": "No wifi", "situation": "Read a book because internet was down.", "emotions": ["calm"], "intensity": "low", "triggers": ["reading"]},
    
    # --- HAPPY / BURNOUT ---
    {"raw": "Got a surprise holiday tomorrow! So happy I can finally sleep in.", "event": "Surprise holiday", "situation": "Found out tomorrow is a holiday.", "emotions": ["happy", "excited"], "intensity": "high", "triggers": ["holiday", "sleep"]},
    {"raw": "I have 3 assignments due this week and I haven't started any. I just feel so drained from everything.", "event": "Assignment pileup", "situation": "Feeling overwhelmed by upcoming deadlines.", "emotions": ["anxious", "numb"], "intensity": "high", "triggers": ["deadlines", "burnout"]},
    
    # --- CYCLE 3 ---
    {"raw": "Surprise pop quiz in Math today. Totally blanked on the formulas.", "event": "Math Pop Quiz", "situation": "Took a surprise quiz and forgot the material.", "emotions": ["anxious", "disappointed"], "intensity": "medium", "triggers": ["exam performance"]},
    {"raw": "Heard everyone talking about how easy the quiz was. I must be the only one who messed up.", "event": "Quiz comparison", "situation": "Heard classmates say the quiz was easy.", "emotions": ["sad", "frustrated"], "intensity": "high", "triggers": ["comparison with peers", "fear of falling behind"]},
    {"raw": "I'm so mad at myself for not reviewing the notes yesterday. I'm literally sabotaging my own GPA.", "event": "Angry at self", "situation": "Blaming myself for poor performance.", "emotions": ["angry", "frustrated"], "intensity": "high", "triggers": ["self-criticism"]},
    {"raw": "Sat in the library and actually made a proper study schedule for the month. Feeling a bit more in control now.", "event": "Made study plan", "situation": "Created a study schedule to get back on track.", "emotions": ["calm", "happy"], "intensity": "medium", "triggers": ["making a study plan", "library"]},
    
    # --- RANDOM / OTHERS TO HIT 25 ---
    {"raw": "Found a really cute stray cat near the cafeteria today! I fed it some biscuits.", "event": "Found a cat", "situation": "Fed a stray cat on campus.", "emotions": ["happy"], "intensity": "medium", "triggers": ["animals", "campus"]},
    {"raw": "Missed breakfast because I overslept. Had to run to class on an empty stomach. Terrible start.", "event": "Missed breakfast", "situation": "Overslept and had to rush to class hungry.", "emotions": ["frustrated", "angry"], "intensity": "medium", "triggers": ["oversleeping", "hunger"]},
    {"raw": "Finally finished the huge physics assignment. It took 6 hours but it's DONE.", "event": "Finished physics", "situation": "Completed a massive assignment.", "emotions": ["excited", "calm"], "intensity": "high", "triggers": ["deadlines", "completion"]},
    {"raw": "Video called my parents today. It was nice to just talk to them and forget about college for an hour.", "event": "Called parents", "situation": "Talked to family back home.", "emotions": ["happy", "calm"], "intensity": "medium", "triggers": ["family"]},
    {"raw": "Just feeling weird today. Not sad, but not happy either. Just kinda floating through the day.", "event": "Weird mood", "situation": "Feeling unmotivated and slightly detached.", "emotions": ["numb"], "intensity": "low", "triggers": ["burnout"]}
]

def load_demo_data():
    """Insert 25 demo entries for Ananya, only if table is empty."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check for existing data
    cursor.execute("SELECT COUNT(*) FROM entries")
    count = cursor.fetchone()[0]
    
    if count > 0:
        conn.close()
        return False, f"Database already has {count} entries. Please clear data first!"
        
    # Set the ending date to 2026-10-05 20:00:00
    end_date = datetime(2026, 10, 5, 20, 0, 0)
    
    inserted_count = 0
    
    # Iterate through entries backwards so the first item gets the oldest date
    for i, entry in enumerate(reversed(DEMO_ENTRIES)):
        # Spread entries out roughly 1.2 days apart to cover 30 days
        entry_date = end_date - timedelta(days=(24 - i) * 1.2)
        date_str = entry_date.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO entries (raw, event, situation, emotions, intensity, triggers, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry["raw"],
            entry["event"],
            entry["situation"],
            json.dumps(entry["emotions"]),
            entry["intensity"],
            json.dumps(entry["triggers"]),
            date_str
        ))
        inserted_count += 1
        
    conn.commit()
    conn.close()
    return True, f"Success! Loaded {inserted_count} demo entries."

def clear_all_data():
    """Delete all rows from the entries table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries")
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    import db
    db.init_db()
    success, msg = load_demo_data()
    print(msg)
