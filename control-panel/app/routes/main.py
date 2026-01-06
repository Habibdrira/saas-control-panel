from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Control Panel SaaS - OK"

from app.services.docker_service import create_microblog_container, list_containers

@bp.route('/create/<username>')
def create_container(username):
    port = 8000 + len(list_containers())
    container = create_microblog_container(username, port)
    return {
        "container": container.name,
        "port": port,
        "status": "created"
    }
