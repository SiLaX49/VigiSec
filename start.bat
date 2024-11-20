@echo off

REM Lancer les services backend et base de données avec Docker Compose
echo Starting backend and database services...
docker-compose up --build -d

REM Attendre que le backend soit prêt (facultatif)
timeout /t 5

REM Lancer Electron
echo Starting Electron app...
cd frontend
npm start
