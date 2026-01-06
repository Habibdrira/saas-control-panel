import os
from flask import Blueprint, request, jsonify
from app.services.docker_service import (
    create_microblog_container,
    generate_credentials,
    save_credentials
)

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/provision", methods=["POST"])
def provision():
    expected_key = os.environ.get("CONTROL_PANEL_API_KEY")
    received_key = request.headers.get("X-API-KEY")

    if received_key != expected_key:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    username = data.get("username")

    container, port = create_microblog_container(username)

    app_user, app_pass = generate_credentials()

    save_credentials(
        container.name,
        port,
        app_user,
        app_pass
    )

    return jsonify({
        "container": container.name,
        "port": port,
        "login": app_user,
        "password": app_pass
    }), 201
