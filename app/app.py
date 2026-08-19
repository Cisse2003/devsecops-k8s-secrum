from flask import Flask, jsonify   # framework
import os

app = Flask(__name__)  # Instanciation de l'app web


# Endpoint de santé pour Kubernetes (Liveness/Readiness probes)
@app.route('/healthz')
def health():
    return jsonify(status="ok"), 200


# Endpoint principal qui tente de lire le secret injecté par Vault
@app.route('/')
def index():
    secret_path = "/vault/secrets/database-config.txt"
    db_password = "Non configuré"

    # Vérification si le fichier de secret injecté existe
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            db_password = f.read().strip()

    return jsonify({
        "message": "API DevSecOps opérationnelle",
        "database_status": "Connecté",
        "secret_vault_detecte": db_password != "Non configuré"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)