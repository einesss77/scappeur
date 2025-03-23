from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_NAME = "projects.db"

def get_projects(page=1, per_page=50):
    """ Récupère les projets paginés et triés par date """
    offset = (page - 1) * per_page
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT id, title, link, price, offers, date_publication, category, status 
        FROM projects 
        WHERE status != 'Archivé' 
        ORDER BY datetime(timestamp) DESC 
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    projects = [dict(zip([column[0] for column in c.description], row)) for row in c.fetchall()]
    conn.close()
    return projects

def get_categories():
    """ Récupère la liste des catégories uniques """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM projects")
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return categories

@app.route("/")
def home():
    page = int(request.args.get("page", 1))
    projects = get_projects(page)
    categories = get_categories()
    return render_template("index.html", projects=projects, categories=categories, page=page)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
