# Utiliser Python comme image de base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source dans le conteneur
COPY . .

# Exposer le port de Flask
EXPOSE 5000

# Commande pour démarrer le backend
CMD ["python", "app.py"]
