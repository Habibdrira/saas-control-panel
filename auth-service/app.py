from flask import Flask, request, redirect, render_template, session
import sqlite3, requests

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "auth-admin-secret"

CONTROL_PANEL = "http://control-panel:5001"
DB = "users.db"

def db():
    return sqlite3.connect(DB)

# ===============================
# INIT DB
# ===============================
c = db()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
  username TEXT PRIMARY KEY,
  email TEXT,
  password TEXT,
  role TEXT
)
""")
c.execute(
    "INSERT OR IGNORE INTO users VALUES ('admin','admin@local','admin123','admin')"
)
c.commit()
c.close()

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
        try:
            c = db()
            c.execute("INSERT INTO users VALUES (?,?,?,?)",(u,e,p,"user"))
            c.commit()
            c.close()

            requests.post(
                f"{CONTROL_PANEL}/api/provision",
                json={"username":u,"email":e}
            )
            return redirect("/user/login")
        except:
            return render_template("register.html", error="User already exists")
    return render_template("register.html")

# ===============================
# USER LOGIN
# ===============================
@app.route("/user/login", methods=["GET","POST"])
def user_login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        c = db()
        r = c.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role='user'",
            (u,p)
        ).fetchone()
        c.close()

        if not r:
            return render_template("login.html", error="Invalid login")

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

    c = db()
    users = c.execute(
        "SELECT username,email FROM users WHERE role='user'"
    ).fetchall()
    c.close()

    return render_template(
        "admin_dashboard.html",
        users=users
    )

# ===============================
# DELETE USER (AUTH-SERVICE)
# ===============================
@app.route("/admin/delete/<username>")
def admin_delete_user(username):
    if not session.get("admin"):
        return redirect("/admin/login")

    c = db()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    c.commit()
    c.close()

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
