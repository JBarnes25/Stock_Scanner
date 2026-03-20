import requests


def send_discord(webhook, message):
    if not webhook:
        return
    try:
        requests.post(webhook, json={"content": message})
    except Exception:
        pass
