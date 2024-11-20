from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        connection = psycopg2.connect(
            host="database",
            database="vigisec",
            user="admin",
            password="admin"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        connection.close()
        return jsonify({"status": "Database connected!"}), 200
    except Exception as e:
        return jsonify({"status": "Database connection failed!", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
