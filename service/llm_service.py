from groq import Groq

from repository.environment import Environment

class LLMService(object):
    def __init__(self, env: Environment):
        self.client = Groq(api_key=env.API_KEY)
        self.behavior = """
Sos un tutor universitario de programacion y estructuras de datos de primer año en la carrera de Ingenieria y sistemas de informacion.
Tu objetivo es responder a las consultas de los alumnos que están aprendiendo.
Debes responder directamente a la pregunta, de manera clara, concisa, didactica y con ejemplos simples.
No agregues nada extra a la respuesta.
Si los ejemplos son de programación, deberán estar escritos en el lenguaje C++.
Usa un acento argentino formal en la respuesta.
"""
        self.model = env.MODEL

    def simple_prompt(self, context, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.model
                },
                {
                    "role": "user",
                    "content": context + "\n" + prompt
                }
            ],
        )

        return response.choices[0].message.content
