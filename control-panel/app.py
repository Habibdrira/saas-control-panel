from flask import Flask, render_template, request, redirect, jsonify
import docker, time

app = Flask(__name__)
client = docker.from_env()

IMAGE = "user-dashboard:adminlte-user"

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    containers=[]
    for c in client.containers.list(all=True):
        c.reload()
        ports=c.attrs["NetworkSettings"]["Ports"]
        port=ports["80/tcp"][0]["HostPort"] if ports.get("80/tcp") else ""
        containers.append({"name":c.name,"status":c.status,"port":port})
    return render_template("dashboard.html", containers=containers)

@app.route("/api/provision", methods=["POST"])
def provision():
    u=request.json["username"]
    name=f"user_{u}"

    try:
        c=client.containers.get(name)
        c.reload()
    except docker.errors.NotFound:
        c=client.containers.run(
            IMAGE,
            name=name,
            environment={"USERNAME":u},
            ports={"80/tcp":None},
            detach=True
        )
        time.sleep(0.5)
        c.reload()

    p=c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return jsonify({"url":f"http://localhost:{p}"})

@app.route("/api/resolve", methods=["POST"])
def resolve():
    u=request.json["username"]
    c=client.containers.get(f"user_{u}")
    c.reload()
    p=c.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
    return jsonify({"url":f"http://localhost:{p}"})

@app.route("/delete/<name>")
def delete(name):
    c=client.containers.get(name)
    c.stop()
    c.remove()
    return redirect("/dashboard")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

# ==================================================
# USER DASHBOARD CONTAINER INTEGRATION (DOCKER)
# ==================================================

import docker

docker_client = docker.from_env()

def create_user_dashboard_container(username, email):
    """
    Create a dedicated user-dashboard container for a user
    """
    container_name = f"user-dashboard-{username}"

    container = docker_client.containers.run(
        "user-dashboard",
        name=container_name,
        environment={
            "USERNAME": username,
            "EMAIL": email,
            "PLAN": "Free",
            "CONTAINER_NAME": container_name
        },
        ports={"80/tcp": None},
        detach=True
    )

    return container

@app.route("/test/create/<username>")
def test_create_container(username):
    email = f"{username}@example.com"
    create_user_dashboard_container(username, email)
    return f"User dashboard container created for {username}"
