from flask import Flask, request, redirect
import sqlite3, requests

app = Flask(__name__)
CONTROL_PANEL = "http://control-panel:5001"
DB = "users.db"

def db():
    return sqlite3.connect(DB)

# INIT DB (SAFE)
c = db()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
  username TEXT PRIMARY KEY,
  email TEXT,
  password TEXT,
  role TEXT
)
""")
c.execute("INSERT OR IGNORE INTO users VALUES ('admin','admin@local','admin123','admin')")
c.commit()
c.close()

@app.route("/")
def home():
    return redirect("/user/login")

################ USER REGISTER ################
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
            return "User already exists"

    return """
    <h2>User Register</h2>
    <form method="post">
      <input name="username" required>
      <input name="email" required>
      <input name="password" required>
      <button>Register</button>
    </form>
    """

################ USER LOGIN ################
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
            return "Invalid login"

        port = requests.get(
            f"{CONTROL_PANEL}/api/user/{u}/port"
        ).json()["port"]

        return redirect(f"http://localhost:{port}")

    return """
    <h2>User Login</h2>
    <form method="post">
      <input name="username">
      <input name="password">
      <button>Login</button>
    </form>
    """

################ ADMIN AUTH ################
@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        if request.form["username"]=="admin" and request.form["password"]=="admin123":
            return redirect("/admin/dashboard")
        return "Invalid admin"

    return """
    <h2>Admin Login</h2>
    <form method="post">
      <input name="username">
      <input name="password">
      <button>Login</button>
    </form>
    """

@app.route("/admin/dashboard")
def admin_dashboard():
    c = db()
    users = c.execute(
        "SELECT username,email FROM users WHERE role='user'"
    ).fetchall()
    c.close()

    html = "<h1>Users</h1><table border=1>"
    html += "<tr><th>User</th><th>Email</th><th>Port</th><th>Action</th></tr>"

    for u,e in users:
        try:
            port = requests.get(
                f"{CONTROL_PANEL}/api/user/{u}/port"
            ).json()["port"]
        except:
            port = "-"
        html += f"<tr><td>{u}</td><td>{e}</td><td>{port}</td><td><a href='/admin/delete/{u}'>Delete</a></td></tr>"

    html += "</table>"
    return html

@app.route("/admin/delete/<u>")
def delete_user(u):
    c = db()
    c.execute("DELETE FROM users WHERE username=?", (u,))
    c.commit()
    c.close()
    requests.delete(f"{CONTROL_PANEL}/api/user/{u}")
    return redirect("/admin/dashboard")

app.run(host="0.0.0.0", port=5000)
