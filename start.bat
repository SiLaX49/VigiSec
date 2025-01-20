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

REM Démarrer le backend via start.sh
echo Starting backend...
start "" "C:\Program Files\Git\bin\bash.exe" -c "cd backend && ./start.sh"

REM Vérifier si le backend a échoué
IF ERRORLEVEL 1 (
    echo Backend failed to start. Please check the backend logs.
    pause
    exit /b 1
)

REM Démarrer le frontend
echo Starting frontend...
cd frontend
npm start
cd ..

REM Lancer l'application Electron
echo Starting Electron...
npx electron . || (
    echo Electron failed to start. Please check your setup.
    pause
    exit /b 1
)

REM Script terminé
echo All services started successfully.
pause
