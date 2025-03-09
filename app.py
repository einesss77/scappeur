from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "projects.db"

def get_projects(status="Nouveau"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, link, price, offers, category, status FROM projects WHERE status = ? ORDER BY timestamp DESC", (status,))
    projects = [{"id": row[0], "title": row[1], "link": row[2], "price": row[3], "offers": row[4], "category": row[5], "status": row[6]} for row in c.fetchall()]
    conn.close()
    return projects

@app.route('/')
def home():
    return render_template("index.html", projects=get_projects())

@app.route('/archive')
def archive():
    return render_template("index.html", projects=get_projects("Non Intéressant"))

@app.route('/mark_project', methods=['POST'])
def mark_project():
    project_id = request.json.get("id")
    new_status = request.json.get("status")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE projects SET status = ? WHERE id = ?", (new_status, project_id))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
