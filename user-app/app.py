from flask import Flask, render_template, redirect
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        username=os.getenv("USERNAME"),
        email=os.getenv("EMAIL")
    )

@app.route("/logout")
def logout():
    return redirect("http://localhost:5000/user/login")

app.run(host="0.0.0.0", port=80)
