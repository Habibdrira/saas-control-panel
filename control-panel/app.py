from flask import (
    Flask, request, redirect,
    render_template, session, url_for
)
import docker

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

    return render_template(
        "dashboard_admin.html",
        containers=containers_data
    )

# ===============================
# CREATE CONTAINER (MANUAL)
# ===============================
@app.route("/create", methods=["POST"])
def create_container():
    if not session.get("admin"):
        return redirect("/login")

    u = request.form["username"]

    try:
        client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp": None},
            environment={
                "USERNAME": u,
                "EMAIL": "manual@local"
            }
        )
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
        client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp": None},
            environment={
                "USERNAME": u,
                "EMAIL": e
            }
        )
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

    client.containers.get(name).start()
    return redirect("/admin/dashboard")

@app.route("/stop/<name>")
def stop_container(name):
    if not session.get("admin"):
        return redirect("/login")

    client.containers.get(name).stop()
    return redirect("/admin/dashboard")

@app.route("/delete/<name>")
def delete_container(name):
    if not session.get("admin"):
        return redirect("/login")

    client.containers.get(name).remove(force=True)
    return redirect("/admin/dashboard")

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
