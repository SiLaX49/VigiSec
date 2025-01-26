const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1980,
    height: 1080,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  // Charge ton fichier index.html avec le chemin absolu
  mainWindow.loadURL('file:///C:/Users/s4dbu/Desktop/projetperso/vigisec/Frontend/index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
