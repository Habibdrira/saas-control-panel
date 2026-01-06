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
