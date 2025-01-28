// Récupérer les éléments HTML nécessaires
const fileInput = document.getElementById('file-input');
const analyseButton = document.querySelector('.uiverse-button-analyse');
const statusElement = document.getElementById('status');

// Vérifier si le backend est actif lors du chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/');
        if (response.ok) {
            const data = await response.json();
            console.log("Backend response:", data);
            statusElement.innerText = `Backend Status: ${data.message}`;
        } else {
            console.error("Failed to connect to the backend:", response.statusText);
            statusElement.innerText = "Backend inaccessible.";
        }
    } catch (error) {
        console.error("Error connecting to the backend:", error.message);
        statusElement.innerText = "Impossible de se connecter au backend.";
    }
});

// Gérer l'envoi du fichier vers /file_scan
analyseButton.addEventListener('click', async () => {
    const file = fileInput.files[0]; // Récupérer le fichier sélectionné

    if (!file) {
        alert("Veuillez sélectionner un fichier avant de lancer l'analyse.");
        return;
    }

    // Créer un objet FormData pour envoyer le fichier
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Mettre à jour le statut
        statusElement.innerText = "Analyse en cours...";

        // Envoyer le fichier au backend
        const response = await fetch('http://127.0.0.1:5000/file_scan', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Réponse du backend :", data);

            // Afficher les résultats
            statusElement.innerText = `Analyse terminée : ${JSON.stringify(data, null, 2)}`;

        } else {
            const errorData = await response.json();
            console.error("Erreur :", errorData);
            statusElement.innerText = `Erreur pendant l'analyse : ${errorData.error}`;
        }
    } catch (error) {
        console.error("Erreur lors de l'envoi du fichier :", error.message);
        statusElement.innerText = "Une erreur est survenue lors de l'envoi du fichier.";
    }
});
