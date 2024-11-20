from flask import Flask, request, jsonify
import os
import request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to VigiSec API! Use the /analyze endpoint to analyze files."

# Endpoint pour analyser un fichier
@app.route('/analyze', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Simuler une analyse avec une API publique (comme VirusTotal)
    analysis_result = fake_analyze_file(file_path)

    # Supprimer le fichier après analyse
    os.remove(file_path)

    return jsonify(analysis_result)

def fake_analyze_file(file_path):
    # Simulation d'une analyse
    return {
        "filename": os.path.basename(file_path),
        "status": "safe",
        "details": "No threats detected"
    }

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
