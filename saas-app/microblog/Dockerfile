FROM python:3.10-slim

# Variables d'environnement Python / Flask
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=microblog.py
ENV FLASK_RUN_HOST=0.0.0.0

# Dossier de travail dans le conteneur
WORKDIR /app

# Dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Port exposé par l'application
EXPOSE 5000

# Commande de démarrage
CMD flask db upgrade && flask run --port=5000
