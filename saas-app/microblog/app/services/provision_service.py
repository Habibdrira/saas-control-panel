import os
import requests

CONTROL_PANEL_URL = os.environ.get(
    "CONTROL_PANEL_URL",
    "http://127.0.0.1:5000/api/provision"
)

CONTROL_PANEL_API_KEY = os.environ.get(
    "CONTROL_PANEL_API_KEY",
    "super-secret-key"
)


def provision_user_container(username):
    payload = {
        "username": username
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": CONTROL_PANEL_API_KEY
    }

    response = requests.post(
        CONTROL_PANEL_URL,
        json=payload,
        headers=headers,
        timeout=5
    )

    if response.status_code != 201:
        raise Exception(
            f"Provision failed: {response.status_code} {response.text}"
        )

    return response.json()
