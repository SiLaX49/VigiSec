@echo off

REM Lancer les services Docker avec Docker Compose
echo Starting Docker services...
docker-compose up --build -d

REM Attendre un moment pour permettre à Docker de démarrer
timeout /t 5 >nul

REM Démarrer le backend via start.sh
echo Starting backend...
start "" "C:\Program Files\Git\bin\bash.exe" -c "cd backend && ./start.sh"

REM Attendre un moment pour permettre au backend de démarrer
timeout /t 5 >nul

REM Démarrer le frontend via npm start
echo Starting frontend...
cd frontend
npm start
