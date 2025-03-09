import schedule
import time
import requests
import sqlite3
from scraper_codeur import scrape_projects

# ⚙️ Configuration du bot Telegram
TELEGRAM_BOT_TOKEN = "7884783894:AAFhQBXgLxDKoksoBOOcHPTmj2T9kK7379I"
TELEGRAM_CHAT_ID = "1538199248"


def send_telegram_message(message):
    """ Envoie un message sur Telegram """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Notification Telegram envoyée avec succès !")
    else:
        print(f"⚠️ Erreur lors de l'envoi Telegram : {response.text}")


def get_latest_projects():
    """ Récupère les derniers projets insérés dans la base de données """
    conn = sqlite3.connect("projects.db")
    c = conn.cursor()
    c.execute("SELECT id, title, price, link FROM projects ORDER BY timestamp DESC LIMIT 5")
    projects = c.fetchall()
    conn.close()
    return projects


def check_new_projects():
    """ Vérifie s'il y a de nouveaux projets et envoie une notification """
    old_projects = set(get_latest_projects())  # Récupère les projets actuels
    new_projects = scrape_projects()  # Scrape les nouveaux projets
    new_entries = set(get_latest_projects()) - old_projects  # Compare les anciens et nouveaux projets

    if new_entries:
        message = "🚀 Nouveaux projets trouvés sur Codeur.com :\n"
        for project in new_entries:
            message += f"\n🔹 {project[1]} - {project[2]}\n🔗 {project[3]}\n"

        send_telegram_message(message)
    else:
        print("✅ Aucun nouveau projet détecté.")


# 📌 Planification : Scraping toutes les 30 minutes
schedule.every(30).minutes.do(check_new_projects)

print("✅ Service de scraping lancé ! Il vérifie toutes les 30 minutes.")

# 🔄 Boucle infinie pour garder le service actif
while True:
    schedule.run_pending()
    time.sleep(60)  # Vérifie les tâches chaque minute
