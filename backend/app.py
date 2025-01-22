from flask import Flask
from flask_cors import CORS
import os

# Initialiser l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['VIRUSTOTAL_API_KEY'] = "c64913fc441957697aca08d33856e0a7cdd31dc2085be37030c9fc85155dcd7c"

# Créer le dossier d'uploads s'il n'existe pas
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Importer et enregistrer les routes
from routes.file_scan import file_scan_bp
from routes.report import report_bp
app.register_blueprint(file_scan_bp)
app.register_blueprint(report_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
