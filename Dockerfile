# Utiliser une image légère de Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le bon port
EXPOSE 8080

# Lancer l'application Flask sur 0.0.0.0:8080
CMD ["python", "server.py"]
