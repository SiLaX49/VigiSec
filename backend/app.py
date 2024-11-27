from flask import Flask, request, jsonify
import os
import logging
import requests
from werkzeug.utils import secure_filename

# Configuration de base
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
API_KEY = "votre_cle_api"  # Remplace par ta clé API
API_URL = "https://www.virustotal.com/api/v3/files"  # URL de l'API cible

# Configuration des logs
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Initialisation de l'application Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crée le dossier d'uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route pour la racine
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Bienvenue sur l'API VigiSec. Utilisez /analyze-multiple pour analyser vos fichiers."
    }), 200

# Vérifie si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Analyse un fichier via l'API publique
def analyze_with_api(file_path):
    try:
        with open(file_path, 'rb') as f:
            headers = {"x-apikey": API_KEY}
            files = {"file": f}
            response = requests.post(API_URL, headers=headers, files=files)

        if response.status_code == 200:
            logging.info(f"Analyse API réussie pour {file_path}.")
            return response.json()
        else:
            error_msg = f"Échec de la communication avec l'API. Code: {response.status_code}"
            logging.error(error_msg)
            return {"error": error_msg}
    except Exception as e:
        logging.error(f"Erreur lors de l'analyse API: {str(e)}")
        return {"error": str(e)}

# Route pour analyser plusieurs fichiers
@app.route('/analyze-multiple', methods=['POST'])
def analyze_multiple_files():
    logging.info("Requête reçue pour l'analyse de plusieurs fichiers.")
    if 'files[]' not in request.files:
        logging.warning("Aucun fichier fourni dans la requête.")
        return jsonify({'success': False, 'message': 'Aucun fichier fourni.'}), 400

    files = request.files.getlist('files[]')
    results = []

    for file in files:
        if file.filename == '':
            logging.warning("Un fichier vide a été reçu.")
            results.append({'file': None, 'status': 'failed', 'message': 'Aucun fichier sélectionné.'})
            continue

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logging.info(f"Fichier reçu et sauvegardé : {filename}.")

            # Analyse via l'API publique
            api_result = analyze_with_api(file_path)

            # Supprime le fichier après l'analyse
            os.remove(file_path)
            logging.info(f"Fichier supprimé après analyse : {filename}.")

            if "error" in api_result:
                results.append({'file': filename, 'status': 'failed', 'message': api_result['error']})
            else:
                results.append({'file': filename, 'status': 'success', 'data': api_result})
        else:
            logging.warning(f"Type de fichier non autorisé : {file.filename}.")
            results.append({'file': file.filename, 'status': 'failed', 'message': 'Type de fichier non autorisé.'})

    logging.info("Analyse terminée, retour des résultats.")
    return jsonify({'success': True, 'results': results}), 200

# Démarre l'application
if __name__ == '__main__':
    logging.info("Démarrage du serveur Flask.")
    app.run(debug=True, host='0.0.0.0', port=5000)
