import sqlite3
from flask import Flask, render_template, request, jsonify
from database import create_table, save_ticket, get_all_tickets
from classifier import classify_ticket
app = Flask(__name__)

create_table()
# Web interface
@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not description:
            result = {
                "error": "Please enter your name and ticket description."
            }

        else:
            category, severity, priority = classify_ticket(description)

            ticket_id = save_ticket(
                name,
                description,
                category,
                severity,
                priority
            )

            result = {
                "id": ticket_id,
                "name": name,
                "description": description,
                "category": category,
                "severity": severity,
                "priority": priority,
                "email": email,
                "department": department,
            }

    tickets = get_all_tickets()

    return render_template(
        "index.html",
        result=result,
        tickets=tickets
    )


# REST API for submitting tickets
@app.route("/api/tickets", methods=["POST"])
def submit_ticket_api():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data required"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    department = data.get("department", "").strip()
    description = data.get("description", "").strip()

    if not name or not email or not department or not description:
        return jsonify({
            "error": "Name, email, department, and description are required"
        }), 400

    category, severity, priority = classify_ticket(description)

    ticket_id = save_ticket(
        name,
        description,
        category,
        severity,
        priority,
        email,
        department
    )

    return jsonify({
        "ticket_id": ticket_id,
        "name": name,
        "description": description,
        "category": category,
        "severity": severity,
        "priority": priority,
        "status": "Open"
    }), 201


# REST API to view stored tickets
@app.route("/api/tickets", methods=["GET"])
def view_tickets_api():

    tickets = get_all_tickets()

    ticket_list = []

    for ticket in tickets:

        ticket_list.append({
            "id": ticket[0],
            "name": ticket[1],
            "description": ticket[2],
            "category": ticket[3],
            "severity": ticket[4],
            "priority": ticket[5],
            "status": ticket[6]
        })

    return jsonify(ticket_list)

# Dashboard page and its data API


# Dashboard page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/stats")
def dashboard_stats():

    conn = sqlite3.connect("tickets.db")
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

    return jsonify({
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_severity": by_severity,
        "by_category": by_category,
        "recent": [
            {
                "id": t[0],
                "name": t[1],
                "category": t[2],
                "priority": t[3]
            }
            for t in recent
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)
