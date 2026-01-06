from flask import Blueprint, render_template, redirect, url_for, session
from app.services.docker_service import (
    get_all_containers,
    start_container,
    stop_container,
    remove_container,
    load_credentials
)

dashboard_bp = Blueprint("dashboard", __name__)

def login_required():
    return session.get("logged_in")

@dashboard_bp.route("/")
def dashboard():
    if not login_required():
        return redirect(url_for("auth.login"))

    containers = get_all_containers()
    credentials = load_credentials()

    return render_template(
        "dashboard.html",
        containers=containers,
        credentials=credentials
    )

@dashboard_bp.route("/start/<id>")
def start(id):
    if not login_required():
        return redirect(url_for("auth.login"))
    start_container(id)
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/stop/<id>")
def stop(id):
    if not login_required():
        return redirect(url_for("auth.login"))
    stop_container(id)
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/delete/<id>")
def delete(id):
    if not login_required():
        return redirect(url_for("auth.login"))
    remove_container(id)
    return redirect(url_for("dashboard.dashboard"))
