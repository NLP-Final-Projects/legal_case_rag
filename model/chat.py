from model.propmt.prompt_handler import *
from model.llm.llm import *
from model.rag.rag_handler import *
from config import *

class Chat:
    def __init__(self, chat_id, rag_handler) -> None:
        self.chat_id = chat_id
        self.message_history = []
        self.response_history = []
        self.prompt_handler = Prompt()
        self.llm = LLM_API_Call("gilas")
        self.rag_handler = rag_handler

    def response(self, message: str) -> str:
        self.message_history.append(message)

        info_list = self.rag_handler.get_information(message)
        prompt = self.prompt_handler.get_prompt(message, info_list)
        response = self.llm.get_LLM_response(prompt=prompt)

        self.response_history.append(response)
        return response

 



    

    