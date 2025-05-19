import sqlite3
from datetime import datetime, date # realtime

database_path = "D:\STUDY\Face_Recognition_System\database\\attendance.db"

def init_database(database_path):
    conn = sqlite3.connect(database_path) # connect to database SQLit (or create db if it doesn't exit)
    c = conn.cursor() # Create cursor object to interact with database
    
    # create "attendance" table
    c.execute(
         """CREATE TABLE IF NOT EXISTS attendance (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               timestamp TEXT,
               date_only TEXT
           )"""
    )
    # save and close
    conn.commit()
    conn.close()

def log_attendance(name, database_path):
    '''
    -> attendance each person once a day -> avoid repeating
    '''
    if name == "Unknown":
        print("Unknown people")
        return
        
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_only = now.date().isoformat() # (YYYY-MM-DD)
    
    # Check if attendance
    c.execute(
        "SELECT * FROM attendance WHERE name=? AND date_only=?",
        (name, date_only)
    )
    existing = c.fetchone()
    
    # if not attendanced -> create a timestamp
    if not existing: 
        c.execute(
            'INSERT INTO attendance (name, timestamp, date_only) VALUES (?, ?, ?)',
            (name, timestamp, date_only)
        )
        conn.commit()
        print("f[INFO] has attendance: {name} time {timestamp}")
    else : # if attendanced -> OK
        print("f[INFO] {name} has attendance today")
        
    conn.close()

def get_attendance(database_path):
    '''
    Return list of people attendance (sort newest)
    '''
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    # get information from newest
    c.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    records = c.fetchall()  # all results
    
    conn.close()
    return records


def get_people(database_path):
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM attendance")
    people = [row[0] for row in c.fetchall()]
    conn.close()
    return people
  
def get_attendance_by_date(target_date, database_path):
    """
    return list of people 
    target_date: Format YYYY-MM-DD (string hoặc date object)
    """
    if isinstance(target_date, date):
        target_date = target_date.isoformat()

    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    c.execute("SELECT name, timestamp FROM attendance WHERE date_only=? ORDER BY timestamp DESC", (target_date,))
    records = c.fetchall()
    conn.close()
    return records


