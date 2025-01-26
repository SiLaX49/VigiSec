from flask import Blueprint, request, jsonify, current_app
import os
import requests
from werkzeug.utils import secure_filename

file_scan_bp = Blueprint('file_scan', __name__)

@file_scan_bp.route('/scan', methods=['POST'])
def scan_file():
    current_app.logger.info("Requête reçue pour analyser un fichier")

    if 'file' not in request.files:
        current_app.logger.error("Aucun fichier fourni dans la requête")
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    current_app.logger.info(f"Nom du fichier reçu : {filename}")
    try:
        uploaded_file.save(file_path)
        current_app.logger.info(f"Fichier sauvegardé temporairement à : {file_path}")
    except Exception as e:
        current_app.logger.error(f"Erreur lors de la sauvegarde du fichier : {e}")
        return jsonify({'error': 'Failed to save file'}), 500

    # Envoi du fichier à VirusTotal
    try:
        with open(file_path, 'rb') as file_to_scan:
            headers = {"x-apikey": current_app.config['VIRUSTOTAL_API_KEY']}
            files = {"file": file_to_scan}
            current_app.logger.info("Envoi du fichier à VirusTotal...")
            response = requests.post("https://www.virustotal.com/api/v3/files", headers=headers, files=files)
            current_app.logger.info(f"Réponse de VirusTotal : {response.status_code}")
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi à VirusTotal : {e}")
        return jsonify({'error': 'Failed to send file to VirusTotal'}), 500

    # Supprimer le fichier après envoi
    try:
        os.remove(file_path)
        current_app.logger.info(f"Fichier temporaire supprimé : {file_path}")
    except Exception as e:
        current_app.logger.warning(f"Impossible de supprimer le fichier temporaire : {e}")

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        current_app.logger.error(f"Erreur de VirusTotal : {response.text}")
        return jsonify({'error': response.text}), response.status_code
