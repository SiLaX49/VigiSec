# VigiSec

**VigiSec** est une application hybride développée pour analyser des fichiers locaux et identifier les potentielles menaces de sécurité en s’appuyant sur des API publiques. Ce projet est réalisé par **De Boisanger Sebastian**, **Morisseau Noa**, et **Monnier Sohail** dans le cadre de leur formation en cybersécurité.

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Docker** et **Docker Compose** : nécessaires pour exécuter l'application via des conteneurs.
- **Python 3.10** : requis si vous souhaitez exécuter le backend sans Docker.
- **Node.js** : indispensable pour le frontend.

---

## 🚀 Installation

### 1. Cloner le projet
Exécutez la commande suivante pour cloner le dépôt GitHub :
```bash
git clone https://github.com/SiLaX49/vigisec.git
cd vigisec
```

### 2. Configuration initiale

#### Avec Docker
Lancez le script `setup.bat` pour configurer l'application avec Docker :
```bash
setup.bat
```
Ce script :
- Installe les dépendances nécessaires.
- Configure les conteneurs Docker pour le frontend, le backend, et la base de données (le cas échéant).

#### Sans Docker
Si vous préférez exécuter l'application manuellement :
1. Installez les dépendances Python :
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Installez les dépendances Node.js :
   ```bash
   cd frontend
   npm install
   ```

---

## ▶️ Lancement

#### Avec Docker
Pour démarrer l'application, exécutez le script `start.bat` :
```bash
start.bat
```
Ce script démarre les conteneurs Docker et rend l'application accessible.

#### Sans Docker
Si vous exécutez manuellement l'application :
1. Démarrez le backend :
   ```bash
   python backend/app.py
   ```
2. Lancez le frontend :
   ```bash
   cd frontend
   npm start
   ```

---

## 🛠️ Structure du projet

- **`frontend/`** : contient l'application Electron pour l'interface utilisateur.
- **`backend/`** : gère l'analyse des fichiers et les interactions avec les API tierces.
- **`docker/`** : configurations Docker pour conteneuriser les services.
- **`scripts/`** : scripts facilitant l'installation et le démarrage (`setup.bat`, `start.bat`).

---

## ✍️ Auteurs

- **Sebastian**
- **Noa**
- **sadburberry**

---
