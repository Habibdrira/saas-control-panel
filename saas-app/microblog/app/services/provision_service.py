import requests
from flask import current_app

def provision_user_container(username):
    """
    Appel l'API du Control Panel pour créer
    un conteneur Docker pour l'utilisateur.
    """

    url = current_app.config['CONTROL_PANEL_URL']
    api_key = current_app.config['CONTROL_PANEL_API_KEY']

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key
    }

    payload = {
        "username": username
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=5
    )

    if response.status_code != 201:
        raise Exception(
            f"Provision failed {response.status_code}: {response.text}"
        )

    return response.json()
