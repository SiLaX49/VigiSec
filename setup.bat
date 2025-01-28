@echo off

REM Spécifie les ports à libérer. Vous pouvez ajouter ou modifier les ports ici.
set PORTS=5000 3000 8000

REM Indique à l'utilisateur que le script va vérifier les ports occupés.
echo Checking for occupied ports...

REM Boucle sur chaque port spécifié dans la variable PORTS.
for %%P in (%PORTS%) do (
    REM Identifie le processus qui utilise le port %%P en recherchant "LISTENING" avec netstat.
    for /f "tokens=5" %%a in ('netstat -ano ^| find "%%P" ^| find "LISTENING"') do (
        REM Si un processus est trouvé, affiche son PID et tente de le terminer.
        echo Found process %%a using port %%P. Terminating it...
        taskkill /PID %%a /F >nul 2>&1
        REM Vérifie si la commande taskkill a réussi.
        IF ERRORLEVEL 1 (
            REM Si l'opération échoue, affiche un message d'erreur.
            echo Failed to terminate process on port %%P. Please check manually.
        ) ELSE (
            REM Sinon, confirme que le processus a été terminé avec succès.
            echo Successfully terminated process %%a on port %%P.
        )
    )
)

REM Informe l'utilisateur que les services Docker vont être démarrés.
echo Starting Docker services...

REM Lance Docker Compose pour démarrer les services définis dans le fichier docker-compose.yml.
docker-compose up --build -d

REM Vérifie si Docker Compose a rencontré une erreur en utilisant la variable ERRORLEVEL.
IF ERRORLEVEL 1 (
    REM Si une erreur s'est produite, affiche un message et arrête le script.
    echo Failed to start Docker services. Please check your Docker setup.
    pause
    exit /b 1
)

REM Passe à l'installation des dépendances du frontend.
echo Installing frontend dependencies...

REM Se déplace dans le répertoire frontend.
cd frontend

REM Installe les dépendances npm nécessaires pour le frontend. Si cela échoue, un message d'erreur est affiché.
npm install >nul 2>&1 || (
    echo Error installing frontend dependencies. Please check your setup.
    pause
    exit /b 1
)

REM Retourne au répertoire précédent.
cd ..

REM Confirme que le script s'est exécuté correctement.
echo Setup completed successfully.

REM Met le script en pause pour permettre à l'utilisateur de voir les messages finaux avant qu'il ne se ferme.
pause
