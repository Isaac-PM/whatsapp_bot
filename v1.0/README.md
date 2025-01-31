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

Primeramente, vamos a definir diferentes _states_ para las sesiones de los usuarios. Estos estados permitirán llevar un control del momento en la interacción en el que se encuentra el usuario, ya sea "bienvenida", "reservando", etc., y así poder realizar acciones específicas dependiendo del estado en el que se encuentre el usuario. Esta definición se hará con un enumerador, además de un diccionario que contendrá el número del usuario y el estado en el que se encuentra:

```python
import enum
class SessionState(enum.Enum):
    WELCOME = 1
    RESERVING = 2

user_session_states = {}

def update_user_state(user_phone_number, state):
    user_session_states[user_phone_number] = state
```



