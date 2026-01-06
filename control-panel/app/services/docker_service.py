import docker

client = docker.from_env()

def list_containers():
    return client.containers.list(all=True)

def create_microblog_container(username):
    port = 8000 + len(list_containers()) + 1

    container = client.containers.run(
        image="microblog-crm",
        name=f"microblog_{username}",
        ports={"5000/tcp": port},
        detach=True
    )

    return container, port

# ===== Dashboard functions =====

def get_all_containers():
    return client.containers.list(all=True)

def start_container(container_id):
    container = client.containers.get(container_id)
    container.start()

def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()

def remove_container(container_id):
    container = client.containers.get(container_id)
    container.remove(force=True)

import json
import os
import secrets

CREDENTIALS_FILE = "containers.json"

def save_credentials(container_name, port, username, password):
    data = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE) as f:
            data = json.load(f)

    data[container_name] = {
        "port": port,
        "username": username,
        "password": password
    }

    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return {}
    with open(CREDENTIALS_FILE) as f:
        return json.load(f)

def generate_credentials():
    username = "user_" + secrets.token_hex(2)
    password = secrets.token_hex(4)
    return username, password
