import llm.llm as llm

end = False
while (not end):
    prompt = input("Escribi una consulta: ")
    if (prompt == "end"):
        end = True
    else:
        response = llm.simple_prompt(
            "", 
            prompt)
        
        print(response)