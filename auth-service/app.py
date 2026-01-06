from flask import Flask, render_template, request, redirect
import sqlite3, requests

app = Flask(__name__)
DB = "users.db"
CONTROL_PANEL = "http://control-panel:5001"  # IMPORTANT en docker

def db():
    return sqlite3.connect(DB, timeout=5)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        d = db()
        if d.execute("SELECT 1 FROM users WHERE username=?", (u,)).fetchone():
            d.close()
            return "User already exists"

        requests.post(f"{CONTROL_PANEL}/api/provision", json={"username": u})

        d.execute("INSERT INTO users(username,password) VALUES (?,?)", (u, p))
        d.commit()
        d.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        d = db()
        ok = d.execute(
            "SELECT 1 FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()
        d.close()

        if not ok:
            return "Invalid credentials"

        r = requests.post(f"{CONTROL_PANEL}/api/resolve", json={"username": u})
        return redirect(r.json()["url"])

    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
