const { ipcRenderer } = require('electron');

const { ipcRenderer } = require('electron');

// Sélectionner un fichier
document.getElementById('selectFileBtn').addEventListener('click', async () => {
    try {
        const filePath = await ipcRenderer.invoke('select-file');
        if (filePath) {
            document.getElementById('filePath').innerText = filePath; // Affiche le chemin
        } else {
            alert('No file selected');
        }
    } catch (error) {
        console.error('Error selecting file:', error);
        alert('An error occurred while selecting a file.');
    }
});


document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const filePath = document.getElementById('filePath').innerText;
    if (!filePath) {
        alert('Please select a file first.');
        return;
    }

    const result = await ipcRenderer.invoke('analyze-file', filePath);
    document.getElementById('result').innerText = JSON.stringify(result, null, 2);
});
