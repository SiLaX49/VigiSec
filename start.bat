@echo off

REM Démarrer les services Docker
echo Starting Docker services...
docker-compose up -d

REM Vérifier si Docker a démarré correctement
IF ERRORLEVEL 1 (
    echo Failed to start Docker services. Please check your Docker setup.
    pause
    exit /b 1
)

REM Attendre un moment pour permettre aux services de démarrer
timeout /t 5 >nul

REM Démarrer le backend dans une nouvelle fenêtre
echo Starting backend...
start "" cmd /c "cd backend && .\start.sh"

REM Démarrer le frontend dans le terminal principal
echo Starting frontend...
cd frontend
npm start

REM Retour à la racine une fois le frontend arrêté
cd ..

REM Lancer l'application Electron dans une nouvelle fenêtre
echo Starting Electron...
start "" cmd /c "npx electron ."

REM Script terminé
echo All services started successfully.
pause
