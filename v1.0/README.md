# WhatsApp Bot v1.0 - Caso Restaurante "Sabor Alegre"

## Objetivos

1. Que el bot dé la bienvenida al cliente y envíe una imagen donde se visualice el nombre del restaurante (`Banner.png`) y su menú (`Menú\ Sabor\ Alegre.pdf`).
2. Que el bot ofrezca la opción de hacer una reservación, permitiendo al cliente brindar su nombre, la hora de llegada y la cantidad de personas a servir.

## Antecedentes

Actualmente, la versión del bot disponible en el archivo `main.py` de este repositorio tiene la capacidad básica de recibir mensajes, conocer su contenido y contestarlos. Sin embargo, no realiza ningún tipo de procesamiento adicional sobre los mensajes entrantes.

Como ejemplo práctico, nos colocaremos en el contexto de un restaurante llamado "Sabor Alegre". Usted puede elegir el nombre de su restaurante si lo desea, además de diseñar los menús y otros recursos. No obstante, en esta carpeta se adjunta material de ejemplo por si quisiera utilizarlo. Si decide crear su propio menú, asegúrese de cumplir con el siguiente formato para cada alimento, ya que esto será de utilidad más adelante:

| ID  | Nombre         | Descripción detallada                                                                                                             | Precio (en USD) | Categoría (entrada, plato fuerte, bebida, postre) |
| --- | -------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------- |
| 1   | Ensalada César | Crujientes hojas de lechuga romana, aderezo César cremoso, crotones dorados y queso parmesano rallado. Ideal como entrada fresca. | 7.99            | Entrada                                           |

> Importante, de momento se trabajará una versión totalmente secuencial para el procesamiento de mensajes. Esto podría hacer que las respuestas a los usuarios tarden más, pero simplifica el proceso de aprendizaje de la lógica general. Una implementación más eficiente se suministrará en la versión final.

---

## Bienvenida (envío del menú y banner)

Primeramente, vamos a definir diferentes _states_ para las sesiones de los usuarios. Estos estados permitirán llevar un control del momento en la interacción en el que se encuentra el usuario, ya sea "bienvenida", "reservando", etc., y así poder realizar acciones específicas dependiendo del estado en el que se encuentre el usuario. Esta definición se hará con un enumerador, además de una clase que contendrá el número del usuario y el estado en el que se encuentra:

```python
import enum
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
```

Además, se ampliará la función `send_message` para que pueda enviar texto, imágenes y documentos PDF:

```python
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
```

El orden de desarrollo de las funciones complementarias será el siguiente:

1. `process_message`, que se encargará de procesar los mensajes entrantes y responder a ellos, esta función será llamada desde el bucle principal del bot.
2. `handle_welcome`, que se encargará de dar la bienvenida al usuario además de solicitar su nombre.
3. `handle_name`, que se encargará de recibir el nombre del usuario y enviar el menú y el banner del restaurante.
4. `handle_people`, que se encargará de recibir la cantidad de personas a servir.
5. `handle_time`, que se encargará de recibir la hora de llegada del cliente.

La explicación detallada de esta nueva iteración del bot se encuentra en el siguiente [enlace](https://www.youtube.com/watch?v=js6zXgxk0cQ).
