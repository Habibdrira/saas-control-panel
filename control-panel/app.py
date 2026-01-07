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
