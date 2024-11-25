const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const axios = require('axios');

let mainWindow;

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'renderer.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    mainWindow.loadFile('index.html');
    mainWindow.setMenu(null);
});

ipcMain.handle('select-file', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
    });

    if (result.canceled) return null;
    return result.filePaths[0];
});

ipcMain.handle('analyze-file', async (event, filePath) => {
    try {
        const formData = new FormData();
        formData.append('file', require('fs').createReadStream(filePath));

        const response = await axios.post('http://localhost:5000/analyze', formData, {
            headers: formData.getHeaders(),
        });

        return response.data;
    } catch (error) {
        return { error: 'Analysis failed. Please try again.' };
    }
});
