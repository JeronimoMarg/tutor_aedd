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
        A continuación recibirás una consulta del usuario junto con un conjunto de documentos recuperados. Tu tarea es responder usando únicamente la información contenida en los documentos recuperados.
        No uses tu conocimiento previo si la respuesta no está respaldada por los documentos.
        Si la información no está presente en los documentos, responde con: “No hay suficiente información disponible en los documentos para responder con certeza.”
        Sé preciso, conciso y mantén un tono profesional.
        Si los ejemplos son de programación, deberán estar escritos en el lenguaje C++.
        Si hay múltiples interpretaciones posibles, indica la más probable con base en el contenido.
        Incluye referencias al documento si están disponibles (por ejemplo, título, ID o URL).
        No asumas ni inventes información.
        Usa un acento argentino formal en la respuesta.
        """
        self.model = env.MODEL
        self.memory_service = memory_service
        self.chunk_service = chunk_service

    def simple_prompt(self, context, prompt):
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
        chunks = self.chunk_service.find_chunks(prompt)
        for c in chunks:
            print(c)
            print("\n")
        related_chunks = "Material relacionado:\n" + "\n".join(chunks)
        context = "\n".join([memory, related_chunks])

        response = self.simple_prompt(context, prompt)
        self.memory_service.add_message(conv, Message("alumno", prompt, None))
        self.memory_service.add_message(conv, Message("tutor", response, None))
        self.memory_service.save_user(user)

        return response


