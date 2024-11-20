from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Exemple : Vérification d'un fichier
@app.route('/scan', methods=['POST'])
def scan_file():
    data = request.get_json()
    file_path = data.get('filePath')

    if not os.path.exists(file_path):
        return jsonify({"message": "Fichier introuvable"}), 404

    # Logique pour vérifier si le fichier est dangereux
    # Exemple : On considère les fichiers .exe comme dangereux
    if file_path.endswith('.exe'):
        return jsonify({"message": "Fichier potentiellement dangereux !"}), 200
    else:
        return jsonify({"message": "Fichier sûr"}), 200

if __name__ == '__main__':
    app.run(debug=True)
