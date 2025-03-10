# Utiliser une image légère de Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système (dont Google Chrome et ChromeDriver)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    chromium-driver \
    chromium && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers du projet
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le bon port
EXPOSE 5000

# Lancer l'application Flask et le scraper
CMD ["sh", "-c", "python server.py & python scraper_service.py"]
