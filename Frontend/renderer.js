const { ipcRenderer } = require('electron');
const axios = require('axios');

// Sélectionne les fichiers
document.getElementById('uploadFiles').addEventListener('change', async (event) => {
    const files = event.target.files;
    if (files.length === 0) {
        alert('Aucun fichier sélectionné.');
        return;
    }

    const formData = new FormData();
    for (const file of files) {
        formData.append('files[]', file);
    }

    try {
        const response = await axios.post('http://localhost:5000/analyze-multiple', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        // Affiche les résultats
        displayResults(response.data.results);
    } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue pendant l\'analyse.');
    }
});

// Affiche les résultats dans l'interface
function displayResults(results) {
    const resultContainer = document.getElementById('results');
    resultContainer.innerHTML = '';

    results.forEach((result) => {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result');
        if (result.status === 'success') {
            resultDiv.innerHTML = `
                <strong>${result.file}</strong>: Analyse réussie.<br>
                Détails: ${JSON.stringify(result.data)}
            `;
        } else {
            resultDiv.innerHTML = `
                <strong>${result.file || 'Fichier inconnu'}</strong>: Échec de l'analyse.<br>
                Message: ${result.message}
            `;
        }
        resultContainer.appendChild(resultDiv);
    });
}
