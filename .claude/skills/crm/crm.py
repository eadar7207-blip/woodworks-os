#!/usr/bin/env python3
"""Prospect CRM - Manage sales pipeline and activity history."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".claude" / "projects" / "adar-realty" / "crm.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    """Initialize database with prospects and activities tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS prospects (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        company TEXT,
        email TEXT,
        phone TEXT,
        stage TEXT DEFAULT 'lead',
        created_at TEXT,
        updated_at TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        prospect_name TEXT NOT NULL,
        activity_type TEXT,
        notes TEXT,
        created_at TEXT,
        FOREIGN KEY(prospect_name) REFERENCES prospects(name)
    )''')
    
    conn.commit()
    conn.close()

def create_prospect(name, company, email, phone):
    """Create a new prospect."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    try:
        c.execute(
            'INSERT INTO prospects (name, company, email, phone, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
            (name, company, email, phone, now, now)
        )
        conn.commit()
        return {"status": "success", "message": f"Prospect '{name}' created", "prospect": {"name": name, "company": company, "email": email, "phone": phone, "stage": "lead"}}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": f"Prospect '{name}' already exists"}
    finally:
        conn.close()

def log_activity(prospect_name, activity_type, notes):
    """Log an activity for a prospect."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute(
        'INSERT INTO activities (prospect_name, activity_type, notes, created_at) VALUES (?, ?, ?, ?)',
        (prospect_name, activity_type, notes, now)
    )
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": f"Activity logged for '{prospect_name}'", "activity": {"type": activity_type, "notes": notes, "timestamp": now}}

def view_prospect(name):
    """View prospect details."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT name, company, email, phone, stage, created_at FROM prospects WHERE name = ?', (name,))
    prospect = c.fetchone()
    
    if not prospect:
        conn.close()
        return {"status": "error", "message": f"Prospect '{name}' not found"}
    
    c.execute('SELECT activity_type, notes, created_at FROM activities WHERE prospect_name = ? ORDER BY created_at DESC', (name,))
    activities = c.fetchall()
    
    conn.close()
    
    return {
        "status": "success",
        "prospect": {
            "name": prospect[0],
            "company": prospect[1],
            "email": prospect[2],
            "phone": prospect[3],
            "stage": prospect[4],
            "created_at": prospect[5]
        },
        "activities": [
            {"type": a[0], "notes": a[1], "date": a[2]}
            for a in activities
        ]
    }

def update_prospect_stage(name, new_stage):
    """Update prospect stage in pipeline."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute('UPDATE prospects SET stage = ?, updated_at = ? WHERE name = ?', (new_stage, now, name))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": f"Updated '{name}' to stage: {new_stage}"}

def view_pipeline():
    """View entire sales pipeline."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT stage, COUNT(*) FROM prospects GROUP BY stage')
    stages = {row[0]: row[1] for row in c.fetchall()}
    
    c.execute('SELECT name, company, email, stage, created_at FROM prospects ORDER BY stage, created_at DESC')
    prospects = c.fetchall()
    
    conn.close()
    
    return {
        "status": "success",
        "summary": stages,
        "prospects": [
            {"name": p[0], "company": p[1], "email": p[2], "stage": p[3], "created": p[4]}
            for p in prospects
        ]
    }

def view_activities(prospect_name):
    """View all activities for a prospect."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT activity_type, notes, created_at FROM activities WHERE prospect_name = ? ORDER BY created_at DESC', (prospect_name,))
    activities = c.fetchall()
    
    conn.close()
    
    return {
        "status": "success",
        "prospect": prospect_name,
        "activities": [
            {"type": a[0], "notes": a[1], "date": a[2]}
            for a in activities
        ]
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create" and len(sys.argv) >= 6:
        result = create_prospect(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif command == "log" and len(sys.argv) >= 5:
        result = log_activity(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == "view" and len(sys.argv) >= 3:
        result = view_prospect(sys.argv[2])
    elif command == "update" and len(sys.argv) >= 4:
        result = update_prospect_stage(sys.argv[2], sys.argv[3])
    elif command == "pipeline":
        result = view_pipeline()
    elif command == "activities" and len(sys.argv) >= 3:
        result = view_activities(sys.argv[2])
    else:
        result = {"error": "Invalid command"}
    
    print(json.dumps(result, indent=2))
