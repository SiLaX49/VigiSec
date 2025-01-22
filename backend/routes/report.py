from flask import Blueprint, jsonify, current_app
import requests

# Création du blueprint pour les routes liées aux rapports
report_bp = Blueprint('report', __name__)

@report_bp.route('/report/<analysis_id>', methods=['GET'])
def get_report(analysis_id):
    """
    Route pour récupérer le rapport d'analyse d'un fichier via VirusTotal.

    :param analysis_id: ID unique de l'analyse (fourni par la route /scan)
    :return: Rapport JSON complet de VirusTotal ou un message d'erreur
    """
    # URL pour récupérer le rapport sur VirusTotal
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

    # Headers contenant la clé API
    headers = {
        "x-apikey": current_app.config['VIRUSTOTAL_API_KEY']  # Clé API VirusTotal
    }

    try:
        # Envoi de la requête GET à l'API VirusTotal
        response = requests.get(url, headers=headers)

        # Si la requête réussit
        if response.status_code == 200:
            # Retourne le rapport d'analyse complet
            return jsonify(response.json()), 200
        else:
            # En cas d'erreur de la part de VirusTotal
            error_message = {
                "error": {
                    "status_code": response.status_code,
                    "details": response.json()
                }
            }
            return jsonify(error_message), response.status_code

    except requests.RequestException as e:
        # Gestion des erreurs de connexion ou autres problèmes liés à la requête
        error_message = {
            "error": {
                "message": f"Une erreur est survenue lors de la connexion à VirusTotal : {str(e)}"
            }
        }
        return jsonify(error_message), 500
