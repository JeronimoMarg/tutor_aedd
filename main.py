from service.llm_service import LLMService
from repository.environment import Environment
from repository.mongo_user_repository import MongoUserRepository
from service.code_service import CodeService
from service.memory_service import MemoryService
from model.message import Message
from model.conversation import Conversation
from model.user import User

end = False
#while (not end):
    #prompt = input("Escribi una consulta: ")
    #if (prompt == "end"):
        #end = True
    #else:
        #response = llm.simple_prompt(
            #"", 
            #prompt)
        #
        ##print(response)


env = Environment()
code_service = CodeService(env)
llm_service = LLMService(env)
user_repository = MongoUserRepository(env)
memory_service = MemoryService(user_repository)

message = Message("alumno", "Explicame punteros")
conv = Conversation(1, [message])
user = User("franco", [conv])
#memory_service.save_user(user)

print(memory_service.find_user("franco").to_dict())

#success, comp_output = code_service.compile_cpp("tmp/compilation_test.cpp")
#response = llm_service.simple_prompt(
    #comp_output,
    #"Explicame por que falla mi codigo"
#)
#print(response)