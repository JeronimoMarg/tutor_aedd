from groq import Groq

from repository.environment import Environment
from model.conversation import Conversation
from model.message import Message
from model.user import User
from service.memory_service import MemoryService
from service.chunk_service import ChunkService

class LLMService(object):
    def __init__(self, env: Environment, memory_service: MemoryService, chunk_service: ChunkService):
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
        self.memory_service = memory_service
        self.chunk_service = chunk_service

    def simple_prompt(self, context, prompt):
        print("Contexto: " + context)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.behavior
                },
                {
                    "role": "user",
                    "content": "Contexto:\n" + context + "\nConsulta:\n" + prompt
                }
            ],
        )

        return response.choices[0].message.content

    def conversation_prompt(self, user: User, conv_id: int, prompt: str) -> str:
        for c in user.conversations:
            if c.id == conv_id:
                conv = c
                break
        else:
            conv = self.memory_service.create_conversation(user)
        
        memory = "Mensajes recientes:\n" + conv.__str__()
        related_chunks = "Material relacionado:\n" + "\n".join(self.chunk_service.find_chunks(prompt))
        context = "\n".join([memory, related_chunks])

        response = self.simple_prompt(context, prompt)
        self.memory_service.add_message(conv, Message("alumno", prompt, None))
        self.memory_service.add_message(conv, Message("tutor", response, None))
        self.memory_service.save_user(user)

        return response


