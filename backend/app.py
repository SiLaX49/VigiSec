from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

# Configuration de base
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer le dossier d'uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Vérifie si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route pour analyser un fichier
@app.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Aucun fichier fourni dans la requête.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Aucun fichier sélectionné.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Analyse fictive (remplacez par une analyse réelle)
        result = {
            "file_name": filename,
            "status": "safe",  # Remplacez par une logique réelle
            "details": "Aucune menace détectée."
        }

        # Supprime le fichier après l'analyse
        os.remove(file_path)

        return jsonify({'success': True, 'data': result}), 200

    return jsonify({'success': False, 'message': 'Type de fichier non autorisé.'}), 400

# Démarre l'application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
