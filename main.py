from service.llm_service import LLMService
from repository.environment import Environment
from repository.mongo_user_repository import MongoUserRepository
from repository.mongo_chunk_repository import MongoChunkRepository
from service.code_service import CodeService
from service.memory_service import MemoryService
from service.chunk_service import ChunkService
from service.document_service import DocumentService
from model.message import Message
from model.conversation import Conversation
from model.user import User
from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)
env = Environment()
code_service = CodeService(env)
user_repository = MongoUserRepository(env)
memory_service = MemoryService(user_repository)
chunk_service = ChunkService(env, MongoChunkRepository(env))
llm_service = LLMService(env, memory_service, chunk_service)
document_service = DocumentService()
code_service = CodeService(env)


# Create a default user for the web interface
#default_user = User("web_user", [])

# Use the default user 
default_user = user_repository.find("web_user")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Extraer el bloque de código C++ del mensaje usando regex
    match = re.search(r'```(?:cpp|c\+\+)?\n([\s\S]*?)```', user_message)
    if match:
        codigo_cpp = match.group(1)
        # Compilador
        success, output = code_service.compile_code_from_text(codigo_cpp)
        if success:
            success_message = "(success) "
        else:
            success_message = "(error) "
        user_message = user_message + 'resultado compilador: ' + success_message + output
    
    if not user_message:
        return jsonify({'error': 'No se indico un prompt'}), 400

    response = llm_service.conversation_prompt(default_user, 1, user_message)
    return jsonify({'response': response})

@app.route('/pdf')
def pdf():
    text_list = document_service.load_pdf_files(env.PDF_DIR)
    for text in text_list:

        chunks = chunk_service.chunk_text(text)
        chunk_service.save_chunks(chunks)
    return "Archivos pdf leidos"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


