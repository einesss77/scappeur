# Utiliser une image légère de Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 (Flask tourne dessus par défaut)
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "server.py"]
