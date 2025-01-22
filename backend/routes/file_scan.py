from flask import Blueprint, request, jsonify, current_app
import os
import requests
from werkzeug.utils import secure_filename

file_scan_bp = Blueprint('file_scan', __name__)

@file_scan_bp.route('/scan', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(file_path)

    # Envoi du fichier à VirusTotal
    with open(file_path, 'rb') as file_to_scan:
        headers = {"x-apikey": current_app.config['VIRUSTOTAL_API_KEY']}
        files = {"file": file_to_scan}
        response = requests.post("https://www.virustotal.com/api/v3/files", headers=headers, files=files)

    # Supprimer le fichier après envoi
    os.remove(file_path)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': response.text}), response.status_code
