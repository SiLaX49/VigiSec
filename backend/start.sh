#!/bin/bash

# Activer l'environnement virtuel
source venv/Scripts/activate || source venv/bin/activate

# Lancer Flask
flask run --host=0.0.0.0 --port=5000
