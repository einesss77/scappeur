from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "projects.db"

def get_projects():
    """ Récupère les projets depuis la base de données """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, link, price, offers, category, status FROM projects WHERE status != 'Archivé'")
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
    projects = get_projects()
    categories = get_categories()
    print(f"📌 Catégories disponibles : {categories}")  # Debugging
    return render_template("index.html", projects=projects, categories=categories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

