# Image de base Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Commande pour démarrer le backend
CMD ["python", "app.py"]
