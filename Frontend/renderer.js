const { ipcRenderer } = require('electron');

document.getElementById('selectFile').addEventListener('click', async () => {
    const filePath = await ipcRenderer.invoke('select-file');
    document.getElementById('filePath').innerText = `Fichier sélectionné : ${filePath}`;

    // Appel à l'API backend pour vérifier le fichier
    const response = await fetch('http://127.0.0.1:5000/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filePath })
    });
    const result = await response.json();
    document.getElementById('scanResult').innerText = `Résultat : ${result.message}`;
});
