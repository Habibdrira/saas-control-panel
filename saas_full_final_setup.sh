#!/bin/bash
set -e

echo "==============================="
echo "  SaaS FINAL STABLE SETUP"
echo "==============================="

############################
# CLEAN PROJECT FILES
############################
rm -rf auth-service control-panel user-app docker-compose.yml

############################
# CREATE STRUCTURE
############################
mkdir -p auth-service control-panel user-app

############################
# docker-compose.yml
############################
cat << 'EOF2' > docker-compose.yml
version: "3.9"

services:
  auth-service:
    build: ./auth-service
    ports:
      - "5000:5000"
    depends_on:
      - control-panel

  control-panel:
    build: ./control-panel
    ports:
      - "5001:5001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
EOF2

############################
# AUTH-SERVICE (STABLE)
############################
cat << 'EOF2' > auth-service/app.py
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
EOF2

cat << 'EOF2' > auth-service/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask requests
EXPOSE 5000
CMD ["python","app.py"]
EOF2

############################
# CONTROL-PANEL (STABLE)
############################
cat << 'EOF2' > control-panel/app.py
from flask import Flask, request, redirect
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"]=="admin" and request.form["password"]=="admin123":
            return redirect("/admin")
        return "Invalid admin"
    return """
    <h2>Docker Admin</h2>
    <form method="post">
      <input name="username">
      <input name="password">
      <button>Login</button>
    </form>
    """

@app.route("/admin")
def admin():
    html = """
    <h1>Containers</h1>
    <form method="post" action="/create">
      <input name="username" placeholder="username">
      <button>Create Container</button>
    </form>
    <table border=1>
    <tr><th>Name</th><th>Status</th><th>Port</th><th>Actions</th></tr>
    """
    for c in client.containers.list(all=True):
        ports = c.attrs["NetworkSettings"]["Ports"]
        port = ports["80/tcp"][0]["HostPort"] if ports.get("80/tcp") else "-"
        html += f"""
        <tr>
          <td>{c.name}</td>
          <td>{c.status}</td>
          <td>{port}</td>
          <td>
            <a href='/open/{c.name}'>Open</a> |
            <a href='/start/{c.name}'>Start</a> |
            <a href='/stop/{c.name}'>Stop</a> |
            <a href='/delete/{c.name}'>Delete</a>
          </td>
        </tr>
        """
    html += "</table>"
    return html

@app.route("/create", methods=["POST"])
def create():
    u = request.form["username"]
    try:
        client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp":None},
            environment={"USERNAME":u,"EMAIL":"manual@local"}
        )
    except:
        pass
    return redirect("/admin")

@app.route("/api/provision", methods=["POST"])
def provision():
    u = request.json["username"]
    e = request.json.get("email","")
    try:
        client.containers.run(
            "user-app",
            name=f"user-{u}",
            detach=True,
            ports={"80/tcp":None},
            environment={"USERNAME":u,"EMAIL":e}
        )
    except:
        pass
    return {"status":"ok"}

@app.route("/api/user/<u>/port")
def get_port(u):
    c = client.containers.get(f"user-{u}")
    port = c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return {"port":port}

@app.route("/api/user/<u>", methods=["DELETE"])
def delete_user(u):
    try:
        client.containers.get(f"user-{u}").remove(force=True)
    except:
        pass
    return {"status":"deleted"}

@app.route("/open/<name>")
def open_c(name):
    c = client.containers.get(name)
    port = c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return redirect(f"http://localhost:{port}")

@app.route("/start/<name>")
def start(name):
    client.containers.get(name).start()
    return redirect("/admin")

@app.route("/stop/<name>")
def stop(name):
    client.containers.get(name).stop()
    return redirect("/admin")

@app.route("/delete/<name>")
def delete(name):
    client.containers.get(name).remove(force=True)
    return redirect("/admin")

app.run(host="0.0.0.0", port=5001)
EOF2

cat << 'EOF2' > control-panel/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask docker
EXPOSE 5001
CMD ["python","app.py"]
EOF2

############################
# USER-APP (STABLE)
############################
cat << 'EOF2' > user-app/app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    return f"""
    <h1>User Dashboard</h1>
    <p>Username: {os.getenv('USERNAME')}</p>
    <p>Email: {os.getenv('EMAIL')}</p>
    """

app.run(host="0.0.0.0", port=80)
EOF2

cat << 'EOF2' > user-app/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 80
CMD ["python","app.py"]
EOF2

echo "✅ SaaS FINAL STABLE VERSION READY"
