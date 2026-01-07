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
