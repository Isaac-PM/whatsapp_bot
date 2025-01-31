import os
import json
import time
import requests
import asyncio
import aiohttp
import enum
from datetime import datetime, date
from dotenv import load_dotenv
from persistence import session, Reservation


# ------------------------------------------------------------
# Misceláneo / Miscellaneous
def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------
# Configuración / Configuration
load_dotenv("../config.env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GLITCH_SERVER_URL = os.getenv("GLITCH_SERVER_URL") + "/messages"
VERSION = os.getenv("VERSION")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


def log_config():
    print("Configuración / Configuration:")
    print(f"\tACCESS_TOKEN: '{ACCESS_TOKEN[:9]}...{ACCESS_TOKEN[-9:]}'")
    print(f"\t{PHONE_NUMBER_ID=}")
    print(f"\t{GLITCH_SERVER_URL=}")
    print(f"\t{VERSION=}")
    print(f"\t{APP_ID=}")
    print(f"\t{APP_SECRET=}")


log_config()


# ------------------------------------------------------------
# Manejo de sesiones / Session handling
class SessionState(enum.Enum):
    WELCOME = 1
    PROVIDING_NAME = 2
    RESERVING = 3
    PROVIDING_PEOPLE = 4
    PROVIDING_TIME = 5


class SessionData:
    def __init__(self, user_name="", last_state=None):
        self.user_name = user_name
        self.last_state = last_state


user_sessions = {}


def update_session(user_id, user_name=None, state=None):
    if user_id not in user_sessions:
        user_sessions[user_id] = SessionData()
    if user_name:
        user_sessions[user_id].user_name = user_name
    if state:
        user_sessions[user_id].last_state = state


def end_session(user_id):
    send_message(user_id, MessageType.TEXT, "Esta conversación ha finalizado.")
    user_sessions.pop(user_id, None)


# ------------------------------------------------------------
# Envío y recepción de mensajes / Sending and receiving messages
class MessageType(enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    PDF = "document"


def send_message(recipient, message_type, content, filename=None):
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": message_type.value,
    }

    if message_type == MessageType.TEXT:
        data["text"] = {"body": content}
    elif message_type == MessageType.IMAGE:
        data["image"] = {"link": content}
    elif message_type == MessageType.PDF:
        data["document"] = {"link": content, "filename": filename or "document.pdf"}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
    return response


def fetch_pending_messages():
    try:
        response = requests.get(GLITCH_SERVER_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching messages: {e}")
        return []


# ------------------------------------------------------------
# Procesamiento de mensajes / Message Processing
def handle_welcome(sender):
    send_message(
        sender,
        MessageType.IMAGE,
        "https://cdn.glitch.global/d2fadd1f-132e-4618-a65f-af2f9d498989/Banner.png?v=1738078324920",
    )
    send_message(
        sender,
        MessageType.TEXT,
        "¡Hola! Bienvenid@ al *Restaurante Sabor Alegre*. ¿Podría brindarnos su *nombre completo* para darle una mejor atención?",
    )
    update_session(sender, state=SessionState.PROVIDING_NAME)


def handle_name(sender, name):
    update_session(sender, user_name=name, state=SessionState.RESERVING)
    send_message(
        sender,
        MessageType.TEXT,
        f"¡Gracias, {name}! Le adjuntamos nuestro menú para que pueda revisarlo.\n¿Desea hacer una reserva? *(Sí/No)*",
    )
    send_message(
        sender,
        MessageType.PDF,
        "https://cdn.glitch.global/d2fadd1f-132e-4618-a65f-af2f9d498989/Men%C3%BA%20Sabor%20Alegre.pdf?v=1738078432110",
        "Menú Sabor Alegre.pdf",
    )


def handle_people(sender, people_count):
    try:
        num_people = int(people_count)
    except ValueError:
        send_message(sender, MessageType.TEXT, "Por favor, ingrese un número válido.")
        return

    reservation = Reservation(
        client_name=user_sessions[sender].user_name,
        client_phone=sender,
        number_of_people=num_people,
    )
    session.add(reservation)
    session.commit()
    send_message(
        sender,
        MessageType.TEXT,
        "¡Excelente! Atendemos desde las 12:00 a las 22:00 horas.\n¿A qué hora le gustaría su reserva para *hoy*? *(Ejemplo: 14:30)*",
    )
    update_session(sender, state=SessionState.PROVIDING_TIME)


def handle_time(sender, time_str):
    try:
        time_obj = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        send_message(sender, MessageType.TEXT, "Formato de hora inválido. Use HH:MM.")
        return

    reservation = (
        session.query(Reservation)
        .filter_by(
            client_name=user_sessions[sender].user_name,
            client_phone=sender,
            arriving_at=None,
        )
        .first()
    )
    if reservation:
        reservation.arriving_at = datetime.combine(date.today(), time_obj)
        session.commit()
        send_message(
            sender,
            MessageType.TEXT,
            f"¡Listo! Su reserva ha sido confirmada para *hoy a las {time_str} horas*. ¡Nos vemos pronto!",
        )
        end_session(sender)


def process_message(sender, text):
    state = user_sessions.get(sender, SessionData()).last_state
    if state == SessionState.PROVIDING_NAME:
        handle_name(sender, text)
    elif state == SessionState.RESERVING:
        if text.lower() in ("sí", "si"):
            send_message(
                sender,
                MessageType.TEXT,
                "¿Para cuántas personas sería la reserva? *(Ejemplo: 2)*",
            )
            update_session(sender, state=SessionState.PROVIDING_PEOPLE)
        else:
            send_message(
                sender,
                MessageType.TEXT,
                "¡Entendido! Si cambia de opinión, no dude en escribirnos. ¡Buen día!",
            )
            end_session(sender)
    elif state == SessionState.PROVIDING_PEOPLE:
        handle_people(sender, text)
    elif state == SessionState.PROVIDING_TIME:
        handle_time(sender, text)
    else:
        handle_welcome(sender)


# ------------------------------------------------------------
# Loop principal / Main Loop
def process_messages():
    try:
        print(
            "\nEscuchando mensajes. Presiona Ctrl+C para salir. / Listening for messages. Press Ctrl+C to exit.\n"
        )
        while True:
            messages = fetch_pending_messages()
            if messages:
                print(
                    f"\n{current_datetime()} Procesando {len(messages)} mensaje(s) / Processing {len(messages)} message(s)"
                )
                for message in messages:
                    message_id = message.get("id")
                    sender = message.get("from")
                    text_body = message.get("text", {}).get("body")
                    print(
                        f"ID: {message_id}, De / From: {sender}, Mensaje / Message: {text_body}"
                    )
                    process_message(sender, text_body)
                    print()
            else:
                print(
                    f"{current_datetime()} No hay mensajes nuevos en la lista. Esperando... / No new messages in the list. Waiting..."
                )
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSaliendo... / Exiting...")


if __name__ == "__main__":
    process_messages()
