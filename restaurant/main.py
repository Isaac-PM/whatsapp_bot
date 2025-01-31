from dotenv import load_dotenv
import aiohttp
import asyncio
import json
import os
import requests
import time

load_dotenv("../config.env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GLITCH_SERVER_URL = os.getenv("GLITCH_SERVER_URL") + "/messages"
VERSION = os.getenv("VERSION")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

print("Configuración / Configuration:")
print(f"\tACCESS_TOKEN: '{ACCESS_TOKEN[:9]}...{ACCESS_TOKEN[-9:]}'")
print(f"\t{PHONE_NUMBER_ID=}")
print(f"\t{GLITCH_SERVER_URL=}")
print(f"\t{VERSION=}")
print(f"\t{APP_ID=}")
print(f"\t{APP_SECRET=}")


def send_message(recipient, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": message},
        }
    )
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Mensaje enviado exitosamente / Message sent successfully")
    else:
        print(
            f"Error al enviar mensaje / Error sending message: {response.status_code}"
        )
        print(response.text)
    return response


def get_pending_messages():
    try:
        response = requests.get(GLITCH_SERVER_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener mensajes / Error fetching messages: {e}")
        return []


def process_messages():
    try:
        print(
            "\nEscuchando mensajes. Presiona Ctrl+C para salir. / Listening for messages. Press Ctrl+C to exit.\n"
        )
        while True:
            messages = get_pending_messages()
            if messages:
                print(
                    f"Procesando {len(messages)} mensaje(s) / Processing {len(messages)} message(s)"
                )
                for message in messages:
                    sender = message.get("from")
                    text_body = message.get("text", {}).get("body")
                    message_id = message.get("id")
                    print(
                        f"ID: {message_id}, De / From: {sender}, Mensaje / Message: {text_body}"
                    )
                    send_message(sender, f"Echo: {text_body}")
            else:
                print(
                    "No hay mensajes nuevos en la lista. Esperando... / No new messages in the list. Waiting..."
                )
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSaliendo... / Exiting...")


if __name__ == "__main__":
    process_messages()
