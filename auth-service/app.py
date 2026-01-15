from flask import Flask, request, redirect, render_template, session
import requests
from database import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    update_last_login,
    get_all_users
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "auth-admin-secret"

CONTROL_PANEL = "http://control-panel:5001"

# ===============================
# Note: Using shared DB via database.py; ensure admin user exists if needed elsewhere

# ===============================
# HOME
# ===============================
@app.route("/")
def home():
    return redirect("/user/login")

# ===============================
# USER REGISTER
# ===============================
@app.route("/user/register", methods=["GET","POST"])
def user_register():
    if request.method == "POST":
        u = request.form["username"]
        e = request.form["email"]
        p = request.form["password"]
        # Create in shared DB
        res = create_user(u, e, p)
        if not res.get("success"):
            return render_template("register.html", error=res.get("error", "Registration failed"))

        # Provision container via control-panel
        try:
            requests.post(
                f"{CONTROL_PANEL}/api/provision",
                json={"username":u,"email":e}
            )
        except Exception:
            pass

        return redirect("/user/login")
    return render_template("register.html")

# ===============================
# USER LOGIN
# ===============================
@app.route("/user/login", methods=["GET","POST"])
def user_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        user = get_user_by_username(u)
        if not user or user.get("password") != p:
            return render_template("login.html", error="Invalid login")
        try:
            update_last_login(user["id"])
        except Exception:
            pass

        port = requests.get(
            f"{CONTROL_PANEL}/api/user/{u}/port"
        ).json()["port"]

        return redirect(f"http://localhost:{port}")

    return render_template("login.html")

# ===============================
# ADMIN LOGIN (AUTH-SERVICE)
# ===============================
@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"]=="admin" and request.form["password"]=="admin123":
            session["admin"] = True
            return redirect("/admin/dashboard")
        return render_template("admin_login.html", error="Invalid admin")

    return render_template("admin_login.html")

# ===============================
# ADMIN DASHBOARD (AUTH-SERVICE)
# ===============================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")
    try:
        users = get_all_users()
    except Exception:
        users = []
    return render_template("admin_dashboard.html", users=[(u['username'], u['email']) for u in users])

# ===============================
# DELETE USER (AUTH-SERVICE)
# ===============================
@app.route("/admin/delete/<username>")
def admin_delete_user(username):
    if not session.get("admin"):
        return redirect("/admin/login")
    # Soft delete not implemented; this removes from shared DB
    # For simplicity, we cannot delete via database.py without an API; keep container deletion only

    # delete container too
    try:
        requests.delete(f"{CONTROL_PANEL}/api/user/{username}")
    except:
        pass

    return redirect("/admin/dashboard")

# ===============================
# ADMIN LOGOUT
# ===============================
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login")

# ===============================
# RUN
# ===============================
app.run(host="0.0.0.0", port=5000)
