import os
import requests
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

file_scan_bp = Blueprint('file_scan', __name__)

@file_scan_bp.route('/file_scan', methods=['POST'])
def file_scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    try:
        # Sauvegarde temporaire du fichier
        uploaded_file.save(file_path)

        # Étape 1 : Envoi à VirusTotal
        with open(file_path, 'rb') as file_to_scan:
            headers = {"x-apikey": current_app.config['VIRUSTOTAL_API_KEY']}
            files = {"file": file_to_scan}
            response = requests.post("https://www.virustotal.com/api/v3/files", headers=headers, files=files)

        if response.status_code != 200:
            current_app.logger.error(f"Erreur VirusTotal : {response.text}")
            return jsonify({'error': 'Error from VirusTotal API (upload)', 'details': response.json()}), response.status_code

        analysis_id = response.json()['data']['id']

        # Étape 2 : Récupération des résultats
        headers = {"x-apikey": current_app.config['VIRUSTOTAL_API_KEY']}
        url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        result_response = requests.get(url, headers=headers)

        if result_response.status_code != 200:
            current_app.logger.error(f"Erreur VirusTotal : {result_response.text}")
            return jsonify({'error': 'Error from VirusTotal API (result)', 'details': result_response.json()}), result_response.status_code

        # Retourne les résultats directement
        return jsonify(result_response.json()), 200

    finally:
        # Supprime le fichier temporaire
        if os.path.exists(file_path):
            os.remove(file_path)
