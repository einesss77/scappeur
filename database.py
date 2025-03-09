import sqlite3

DB_NAME = "projects.db"

def init_db():
    """ Initialise la base de données SQLite """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            price TEXT,
            offers TEXT,
            category TEXT,
            status TEXT DEFAULT "Nouveau",
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_project(title, link, price, offers, category):
    """ Insère un projet dans la base de données s'il n'existe pas déjà """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO projects (title, link, price, offers, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, link, price, offers, category))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Évite les doublons grâce à "link UNIQUE"
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Base de données initialisée !")
