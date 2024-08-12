from model.chat import *

class Controller:
    
    
    def __init__(self) -> None:
        self.chat_dic = {}
    
    def handle_message(self, 
                       chat_id: int,
                       message: str) -> str:
        if chat_id not in self.chat_dic:
             self.chat_dic[chat_id] = Chat(chat_id=chat_id)
        chat = self.chat_dic[chat_id]
        return chat.response(message)
        
      
