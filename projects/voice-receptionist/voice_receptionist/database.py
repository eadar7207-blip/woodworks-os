"""
SQLite database for voice receptionist
Stores calls, leads, appointments, and activities
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

DB_PATH = 'voice_receptionist.db'


class Database:
    """SQLite database manager"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_schema()

    def init_schema(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                call_id TEXT PRIMARY KEY,
                agent_id TEXT,
                caller_phone TEXT,
                caller_name TEXT,
                caller_email TEXT,
                intent TEXT,
                outcome TEXT,
                duration_seconds INTEGER,
                transcript TEXT,
                call_state TEXT,
                created_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')

        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments_scheduled (
                id TEXT PRIMARY KEY,
                call_id TEXT,
                property_address TEXT,
                appointment_type TEXT,
                scheduled_time TIMESTAMP,
                attendee_email TEXT,
                attendee_name TEXT,
                confirmed BOOLEAN,
                created_at TIMESTAMP,
                FOREIGN KEY(call_id) REFERENCES calls(call_id)
            )
        ''')

        # Leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads_captured (
                id TEXT PRIMARY KEY,
                call_id TEXT,
                lead_name TEXT,
                phone TEXT,
                email TEXT,
                lead_score TEXT,
                property_interest TEXT,
                timeline TEXT,
                budget TEXT,
                notes TEXT,
                synced_to_crm BOOLEAN DEFAULT 0,
                created_at TIMESTAMP,
                FOREIGN KEY(call_id) REFERENCES calls(call_id)
            )
        ''')

        # Skill calls log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_calls (
                id TEXT PRIMARY KEY,
                call_id TEXT,
                skill_name TEXT,
                endpoint TEXT,
                status_code INTEGER,
                succeeded BOOLEAN,
                error TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP,
                FOREIGN KEY(call_id) REFERENCES calls(call_id)
            )
        ''')

        conn.commit()
        conn.close()

        logger.info(f"Database initialized at {self.db_path}")

    def create_call(self, call_state):
        """Create a new call record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO calls
            (call_id, agent_id, caller_phone, created_at, call_state)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            call_state['call_id'],
            call_state.get('agent_id'),
            call_state.get('caller_phone'),
            datetime.utcnow().isoformat(),
            json.dumps(call_state)
        ))

        conn.commit()
        conn.close()

        logger.info(f"Created call record: {call_state['call_id']}")

    def update_call(self, call_id, call_state):
        """Update call record with latest state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE calls
            SET caller_name = ?, caller_email = ?, intent = ?, outcome = ?,
                duration_seconds = ?, call_state = ?
            WHERE call_id = ?
        ''', (
            call_state.get('contact', {}).get('name'),
            call_state.get('contact', {}).get('email'),
            call_state.get('intent'),
            call_state.get('state'),
            (
                int((
                    datetime.fromisoformat(call_state.get('completed_at', '').replace('Z', '+00:00'))
                    - datetime.fromisoformat(call_state.get('started_at', '').replace('Z', '+00:00'))
                ).total_seconds())
                if call_state.get('completed_at')
                else 0
            ),
            json.dumps(call_state),
            call_id
        ))

        conn.commit()
        conn.close()

        logger.info(f"Updated call record: {call_id}")

    def get_calls(self, agent_id=None, limit=50, offset=0):
        """Get call records with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if agent_id:
            cursor.execute('''
                SELECT call_id, agent_id, caller_phone, caller_name, intent, duration_seconds, created_at
                FROM calls
                WHERE agent_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (agent_id, limit, offset))
        else:
            cursor.execute('''
                SELECT call_id, agent_id, caller_phone, caller_name, intent, duration_seconds, created_at
                FROM calls
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_call(self, call_id):
        """Get a specific call record"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM calls WHERE call_id = ?', (call_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            result = dict(row)
            result['call_state'] = json.loads(result['call_state'])
            return result
        return None

    def create_appointment(self, appointment_data):
        """Log a scheduled appointment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO appointments_scheduled
            (id, call_id, property_address, appointment_type, scheduled_time, attendee_email, attendee_name, confirmed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            appointment_data.get('id'),
            appointment_data.get('call_id'),
            appointment_data.get('property_address'),
            appointment_data.get('appointment_type'),
            appointment_data.get('scheduled_time'),
            appointment_data.get('attendee_email'),
            appointment_data.get('attendee_name'),
            appointment_data.get('confirmed', False),
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

    def create_lead(self, lead_data):
        """Log a captured lead"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO leads_captured
            (id, call_id, lead_name, phone, email, lead_score, property_interest, timeline, budget, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            lead_data.get('id'),
            lead_data.get('call_id'),
            lead_data.get('lead_name'),
            lead_data.get('phone'),
            lead_data.get('email'),
            lead_data.get('lead_score'),
            lead_data.get('property_interest'),
            lead_data.get('timeline'),
            lead_data.get('budget'),
            lead_data.get('notes'),
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

    def get_stats(self):
        """Get aggregated statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total calls
        cursor.execute('SELECT COUNT(*) as count FROM calls')
        total_calls = cursor.fetchone()[0]

        # Calls in last 24 hours
        yesterday = (datetime.utcnow() - timedelta(hours=24)).isoformat()
        cursor.execute('SELECT COUNT(*) as count FROM calls WHERE created_at > ?', (yesterday,))
        calls_24h = cursor.fetchone()[0]

        # Total leads
        cursor.execute('SELECT COUNT(*) as count FROM leads_captured')
        total_leads = cursor.fetchone()[0]

        # Total appointments
        cursor.execute('SELECT COUNT(*) as count FROM appointments_scheduled')
        total_appointments = cursor.fetchone()[0]

        # Average call duration
        cursor.execute('SELECT AVG(duration_seconds) as avg_duration FROM calls WHERE duration_seconds > 0')
        avg_duration = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_calls': total_calls,
            'calls_24h': calls_24h,
            'total_leads': total_leads,
            'total_appointments': total_appointments,
            'avg_call_duration_seconds': int(avg_duration),
            'timestamp': datetime.utcnow().isoformat()
        }
