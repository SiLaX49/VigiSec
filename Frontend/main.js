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

  const indexPath = path.join(__dirname, 'index.html');
  mainWindow.loadFile(indexPath);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
