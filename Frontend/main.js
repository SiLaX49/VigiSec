const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'renderer.js'),
            nodeIntegration: true,
            contextIsolation: false,
        },
        frame: false, // Supprime la barre supérieure
        titleBarStyle: 'hidden', // Ajoute un style moderne
    });

    mainWindow.loadFile('index.html');
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        mainWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                preload: path.join(__dirname, 'renderer.js'),
                nodeIntegration: true,
                contextIsolation: false,
            },
            frame: false,
            titleBarStyle: 'hidden',
        });

        mainWindow.loadFile('index.html');
    }
});
