import os
import dotenv
from groq import Groq

dotenv.load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL")

client = Groq(api_key=API_KEY)

# LLM Config
BEHAVIOR = """
Sos un tutor universitario de programacion y estructuras de datos de primer año en la carrera de Ingenieria y sistemas de informacion.
Tu objetivo es responder a las consultas de los alumnos que están aprendiendo.
Debes responder directamente a la pregunta, de manera clara, concisa, didactica y con ejemplos simples.
No agregues nada extra a la respuesta.
Si los ejemplos son de programación, deberán estar escritos en el lenguaje C++.
"""
MAX_TOKENS = 150

historial = [
    {
        "role":"system",
        "content":BEHAVIOR
    }
]

def simple_prompt(context, prompt):

    historial.append({
        "role":"user",
        "content":context+"\n"+prompt
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=historial,
    )

    respuesta = response.choices[0].message.content
    historial.append({
        "role": "assistant",
        "content": respuesta
    })

    return respuesta