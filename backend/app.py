from flask import Flask, jsonify
from flask_cors import CORS
import os
from routes.file_scan import file_scan_bp  # Importer le Blueprint

# Initialiser l'application Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['VIRUSTOTAL_API_KEY'] = "c64913fc441957697aca08d33856e0a7cdd31dc2085be37030c9fc85155dcd7c"

# Créer le dossier d'uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Route de santé pour vérifier si le backend fonctionne
@app.route('/', methods=['GET'])
def accueil():
    return jsonify({"status": "success", "message": "Backend is running"}), 200

# Enregistrer le Blueprint
app.register_blueprint(file_scan_bp)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
