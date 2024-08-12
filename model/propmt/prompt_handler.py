from typing import List

class Prompt:
    
    def __init__(self) -> None:
        pass
    
    def get_prompt(self, message:str, info_list: List[str]) -> str:
        return message