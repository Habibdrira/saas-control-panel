import os
from flask import Blueprint, request, jsonify
from app.services.docker_service import create_microblog_container

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/provision", methods=["POST"])
def provision():
    expected_key = os.environ.get("CONTROL_PANEL_API_KEY")
    received_key = request.headers.get("X-API-KEY")

    print("EXPECTED KEY =", expected_key)
    print("RECEIVED KEY =", received_key)

    if not expected_key or received_key != expected_key:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "username required"}), 400

    username = data["username"]

    container, port = create_microblog_container(username)

    return jsonify({
        "container": container.name,
        "port": port,
        "status": "created"
    }), 201
