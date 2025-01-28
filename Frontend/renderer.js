const { remote } = require('electron');
const axios = require('axios');

document.getElementById('minimize').addEventListener('click', () => {
  const window = remote.getCurrentWindow();
  window.minimize();
});

document.getElementById('close').addEventListener('click', () => {
  const window = remote.getCurrentWindow();
  window.close();
});

const fileInput = document.getElementById('fileInput');
const scanButton = document.getElementById('scanButton');
const fileNameDisplay = document.getElementById('fileName');
const loading = document.getElementById('loading');
const results = document.getElementById('results');

let selectedFile = null;

// Quand un fichier est sélectionné
fileInput.addEventListener('change', (event) => {
  selectedFile = event.target.files[0];
  if (selectedFile) {
    fileNameDisplay.textContent = `Fichier sélectionné : ${selectedFile.name}`;
    scanButton.disabled = false;
  }
});

// Quand l'utilisateur clique sur "Analyser le fichier"
scanButton.addEventListener('click', async () => {
  if (!selectedFile) return alert('Veuillez sélectionner un fichier.');

  scanButton.disabled = true;
  loading.style.display = 'block';
  results.innerHTML = '';

  const formData = new FormData();
  formData.append('file', selectedFile);

  console.log('Fichier sélectionné :', selectedFile);
  console.log('FormData :', formData.get('file'));

  try {
    // Envoyer le fichier pour analyse
    const scanResponse = await axios.post('http://localhost:5000/scan', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    const analysisId = scanResponse.data.data.id;

    // Vérifier périodiquement les résultats
    const intervalId = setInterval(async () => {
      const reportResponse = await axios.get(`http://localhost:5000/report/${analysisId}`);
      const reportData = reportResponse.data.data;

      if (reportData.attributes.status === 'completed') {
        clearInterval(intervalId);
        results.innerHTML = `<pre>${JSON.stringify(reportData, null, 2)}</pre>`;
        loading.style.display = 'none';
      }
    }, 5000);
  } catch (error) {
    results.innerHTML = `<p>Erreur : ${error.message}</p>`;
    loading.style.display = 'none';
    scanButton.disabled = false;
  }
});
