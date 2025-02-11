# https://ollama.com/download
# ollama run deepseek-r1:8b

from ollama import chat
from ollama import ChatResponse
import fitz
import re


def read_pdf(file_path):
    with fitz.open(file_path) as pdf:
        content = "\n".join([page.get_text() for page in pdf])
    return content


def ask_menu_question(question, filter_answer=True):
    menu_path = r"../assets/Menú Sabor Alegre.pdf"
    menu_content = read_pdf(menu_path)

    support_phone = "+506 8888-8888"

    query = f"""
    You are an assistant specialized in answering questions about a restaurant's menu.  
    Your only source of information is the menu provided below. Do not answer questions unrelated to this content.  

    ### **Response Instructions:**  
    - Do not answer questions that are not related to the restaurant menu.  
    - Do not use prior context or recall previous questions.  
    - Do not mention that you are an AI assistant.  
    - Your answer should be brief, clear, and in Spanish.  
    - Do not repeat the customer's question in your answer.  
    - If the question is unrelated to the menu, respond with:  
    **"Lo siento, no puedo responder a esa pregunta. Puedes consultar directamente llamando a este número: {support_phone}."**
    - Reason your answer well and be as precise as possible.  
    - Use a friendly and personal tone.  
    - Do not consider birds, fish, or seafood as vegetarian options.
    - Do not repeat the question in the answer.
    - Respond only in Spanish.
    - Do not format the answer in markdown or any other format, just plain text.

    ### **Restaurant Menu:**  
    {menu_content}  

    ### **Customer's Question:**  
    {question}  
    """

    answer: ChatResponse = chat(
        model="deepseek-r1:8b",
        messages=[{"role": "user", "content": query}],
    )

    filtered_answer = answer.message.content
    if filter_answer:
        filtered_answer = re.sub(
            r"<think>.*?</think>", "", answer.message.content, flags=re.DOTALL
        ).strip()

    return (
        "🤖 "
        + filtered_answer
        + "\n\nEsta respuesta fue generada por un asistente de inteligencia artificial y podría contener errores."
    )
