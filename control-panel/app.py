from flask import (
    Flask, request, redirect,
    render_template, session, url_for
)
import docker
import os
from database import (
    get_admin_stats,
    get_all_users,
    get_all_containers,
    get_all_activity_logs,
    get_user_by_username,
    get_container_by_name,
    create_user as db_create_user,
    create_container as db_create_container,
    update_container_status as db_update_container_status,
    delete_container as db_delete_container,
    delete_all_users as db_delete_all_users,
    log_activity,
    init_db,
    DB_PATH
)

# ===============================
# APP CONFIG
# ===============================
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.secret_key = "super-secret-admin-key"

client = docker.from_env()

# ===============================
# AUTH ADMIN
# ===============================
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["username"] == "admin"
            and request.form["password"] == "admin123"
        ):
            session["admin"] = True
            return redirect("/admin/dashboard")

        return render_template(
            "admin_login.html",
            error="Invalid admin credentials"
        )

    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ===============================
# ADMIN DASHBOARD
# ===============================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/login")

    containers_data = []

    for c in client.containers.list(all=True):
        ports = c.attrs["NetworkSettings"]["Ports"]
        port = "-"
        if ports and ports.get("80/tcp"):
            port = ports["80/tcp"][0]["HostPort"]

        containers_data.append({
            "name": c.name,
            "status": c.status,
            "port": port
        })

    stats = get_admin_stats() or {}
    recent_logs = get_all_activity_logs(limit=10) or []
    users = get_all_users() or []
    return render_template(
        "dashboard_admin.html",
        containers=containers_data,
        stats=stats,
        logs=recent_logs,
        users=users
    )

# ===============================
# ADMIN API ENDPOINTS (DB-BACKED)
# ===============================
@app.route("/api/admin/stats")
def api_admin_stats():
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    return get_admin_stats()

@app.route("/api/admin/users")
def api_admin_users():
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    return {"users": get_all_users()}

@app.route("/api/admin/containers")
def api_admin_containers():
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    return {"containers": get_all_containers()}

@app.route("/api/admin/activity-logs")
def api_admin_activity_logs():
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    return {"logs": get_all_activity_logs()}

# ===============================
# CREATE CONTAINER (MANUAL)
# ===============================
@app.route("/create", methods=["POST"])
def create_container():
    if not session.get("admin"):
        return redirect("/login")

    u = request.form["username"]

    try:
        # Ensure user exists in DB
        user = get_user_by_username(u)
        if not user:
            res = db_create_user(u, "manual@local", "")
            if not res.get("success"):
                return redirect("/admin/dashboard")
            user_id = res["user_id"]
            user = get_user_by_username(u)
        else:
            user_id = user["id"]

        # Create container
        cont = client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp": None},
            environment={
                "USERNAME": u,
                "EMAIL": user.get("email", "manual@local")
            }
        )
        cont.reload()
        ports = cont.attrs.get("NetworkSettings", {}).get("Ports", {})
        port = None
        if ports and ports.get("80/tcp"):
            port = int(ports["80/tcp"][0]["HostPort"]) if ports["80/tcp"][0].get("HostPort") else None

        # Persist to DB
        res = db_create_container(user_id, cont.id, cont.name, port or 0)
        if res.get('success'):
            container_pk = res['container_id']
            db_update_container_status(container_pk, 'running')
            log_activity(user_id, container_pk, 'container_created', f'Container {cont.name} created')
    except Exception:
        pass

    return redirect("/admin/dashboard")

# ===============================
# API – PROVISION USER (FROM AUTH)
# ===============================
@app.route("/api/provision", methods=["POST"])
def api_provision():
    u = request.json["username"]
    e = request.json.get("email", "")

    try:
        # Ensure user exists in DB
        user = get_user_by_username(u)
        if not user:
            res = db_create_user(u, e or "", "")
            if not res.get("success"):
                return {"status": "error", "error": res.get("error")}, 400
            user_id = res["user_id"]
            user = get_user_by_username(u)
        else:
            user_id = user["id"]

        # Create container
        cont = client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp": None},
            environment={
                "USERNAME": u,
                "EMAIL": user.get("email", e or "")
            }
        )
        cont.reload()
        ports = cont.attrs.get("NetworkSettings", {}).get("Ports", {})
        port = None
        if ports and ports.get("80/tcp"):
            port = int(ports["80/tcp"][0]["HostPort"]) if ports["80/tcp"][0].get("HostPort") else None

        # Persist to DB
        res = db_create_container(user_id, cont.id, cont.name, port or 0)
        if res.get('success'):
            container_pk = res['container_id']
            db_update_container_status(container_pk, 'running')
            log_activity(user_id, container_pk, 'container_created', f'Container {cont.name} provisioned')
    except Exception:
        pass

    return {"status": "ok"}

# ===============================
# API – GET USER PORT
# ===============================
@app.route("/api/user/<username>/port")
def get_user_port(username):
    c = client.containers.get(f"user-{username}")
    port = c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return {"port": port}

# ===============================
# API – DELETE USER CONTAINER
# ===============================
@app.route("/api/user/<username>", methods=["DELETE"])
def delete_user_container(username):
    try:
        client.containers.get(f"user-{username}").remove(force=True)
    except Exception:
        pass
    return {"status": "deleted"}

# ===============================
# ADMIN ACTIONS
# ===============================
@app.route("/open/<name>")
def open_container(name):
    if not session.get("admin"):
        return redirect("/login")

    c = client.containers.get(name)
    port = c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return redirect(f"http://localhost:{port}")

@app.route("/start/<name>")
def start_container(name):
    if not session.get("admin"):
        return redirect("/login")

    cont = client.containers.get(name)
    cont.start()
    try:
        rec = get_container_by_name(name)
        if rec:
            db_update_container_status(rec['id'], 'running')
            log_activity(rec['user_id'], rec['id'], 'container_started', f'{name} started')
    except Exception:
        pass
    return redirect("/admin/dashboard")

@app.route("/stop/<name>")
def stop_container(name):
    if not session.get("admin"):
        return redirect("/login")

    cont = client.containers.get(name)
    cont.stop()
    try:
        rec = get_container_by_name(name)
        if rec:
            db_update_container_status(rec['id'], 'stopped')
            log_activity(rec['user_id'], rec['id'], 'container_stopped', f'{name} stopped')
    except Exception:
        pass
    return redirect("/admin/dashboard")

@app.route("/delete/<name>")
def delete_container(name):
    if not session.get("admin"):
        return redirect("/login")

    cont = client.containers.get(name)
    try:
        rec = get_container_by_name(name)
        if rec:
            log_activity(rec['user_id'], rec['id'], 'container_deleted', f'{name} deleted')
            db_delete_container(rec['id'])
    except Exception:
        pass
    cont.remove(force=True)
    return redirect("/admin/dashboard")

# ===============================
# RESET DATABASE
# ===============================
@app.route("/api/admin/reset-database", methods=["POST"])
def reset_database():
    """Supprimer et réinitialiser la base de données"""
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    
    try:
        # Supprimer le fichier de base de données
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        # Réinitialiser avec une nouvelle base vide
        init_db()
        
        return {"success": True, "message": "Base de données réinitialisée"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/admin/delete-all-users", methods=["POST"])
def delete_all_users():
    """Supprimer tous les utilisateurs de la base de données"""
    if not session.get("admin"):
        return {"error": "unauthorized"}, 401
    
    result = db_delete_all_users()
    if result.get('success'):
        return result
    else:
        return result, 500

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
