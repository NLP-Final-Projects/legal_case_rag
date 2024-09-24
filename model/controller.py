from model.chat import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class Controller:
    def __init__(self) -> None:
        self.chat_dic = {}
        self.rag_handler = RAG()

    def handle_message(self,
                       chat_id: int,
                       message: str) -> str:
        if chat_id not in self.chat_dic:
             self.chat_dic[chat_id] = Chat(chat_id=chat_id, rag_handler=self.rag_handler)
        chat = self.chat_dic[chat_id]
        return chat.response(message)