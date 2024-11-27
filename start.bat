@echo off

REM Spécifie les ports à libérer
set PORTS=5000 3000 8000

echo Checking for occupied ports...

for %%P in (%PORTS%) do (
    REM Identifier le processus utilisant le port %%P
    for /f "tokens=5" %%a in ('netstat -ano ^| find "%%P" ^| find "LISTENING"') do (
        echo Found process %%a using port %%P. Terminating it...
        taskkill /PID %%a /F >nul 2>&1
        IF ERRORLEVEL 1 (
            echo Failed to terminate process on port %%P. Please check manually.
        ) ELSE (
            echo Successfully terminated process %%a on port %%P.
        )
    )
)

REM Lancer les services Docker avec Docker Compose
echo Starting Docker services...
docker-compose up --build -d

REM Vérifier si Docker a démarré correctement
IF ERRORLEVEL 1 (
    echo Failed to start Docker services. Please check your Docker setup.
    pause
    exit /b 1
)

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

REM Vérifier si le frontend a démarré
IF ERRORLEVEL 1 (
    echo Frontend failed to start. Please check the frontend logs.
    pause
    exit /b 1
)

REM Script terminé
echo All services started successfully.
pause
