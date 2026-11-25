import sqlite3
DB_NAME = "tickets.db"
def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT,
            severity TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Open'
        )
    """)
    # Add new columns if they don't already exist
    cursor.execute("PRAGMA table_info(tickets)")
    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:
        cursor.execute("ALTER TABLE tickets ADD COLUMN email TEXT")

    if "department" not in columns:
     cursor.execute("ALTER TABLE tickets ADD COLUMN department TEXT")
    

    conn.commit()
    conn.close()


def save_ticket(name, description, category, severity, priority,
                email="", department=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (name, description, category, severity, priority,
         email, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, category, severity, priority,
          email, department))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id

def get_all_tickets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
    tickets = cursor.fetchall()

    conn.close()
    return tickets




def get_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
    by_status = dict(cursor.fetchall())

    cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
    by_priority = dict(cursor.fetchall())

    cursor.execute("SELECT severity, COUNT(*) FROM tickets GROUP BY severity")
    by_severity = dict(cursor.fetchall())

    cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
    by_category = dict(cursor.fetchall())

    cursor.execute("""
        SELECT id, name, category, priority
        FROM tickets
        ORDER BY id DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()

    conn.close()

    recent_list = [
        {
            "id": t[0],
            "name": t[1],
            "category": t[2],
            "priority": t[3]
        }
        for t in recent
    ]

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_severity": by_severity,
        "by_category": by_category,
        "recent": recent_list
    }
