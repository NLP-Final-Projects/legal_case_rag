from langchain_openai import OpenAI  # pip install langchain_openai
import openai

from config import *
class LLM_API_Call:
    
    def __init__(self, type) -> None:
        
        if type == "openai":
            self.llm = OpenAI_API_Call(api_key = LLM_CONFIG["api_key"],
                                       model = LLM_CONFIG["model"])
        elif type == "gilas":
            self.llm = Gilas_API_Call(api_key = GILAS_CONFIG["api_key"],
                                       model = GILAS_CONFIG["model"],
                                       base_url=GILAS_CONFIG["base_url"])
        else:
            self.llm = OpenAI(
                            **LLM_CONFIG
            )
    
    def get_LLM_response(self, prompt: str) -> str:
        return self.llm.invoke(prompt)



class OpenAI_API_Call:
    
    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        openai.api_key = api_key
        self.model = model
        self.conversation = []

    def add_message(self, role, content):
        """Adds a message to the conversation history."""
        self.conversation.append({"role": role, "content": content})

    def get_response(self):
        """Gets a response from the API based on the conversation history."""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation
        )
        return response['choices'][0]['message']['content']

    def invoke(self, user_input):
        """Handles user input and generates a response."""
        # Add the user's message to the conversation
        self.add_message("user", user_input)

        # Get the AI's response
        response = self.get_response()

        # Add the AI's response to the conversation
        self.add_message("assistant", response)

        return response 
    
    
class Gilas_API_Call:
    
    
    
    
    def __init__(self, api_key, base_url, model="gpt-4"):
        self.client = OpenAI(
                            model = model,
                            api_key = api_key,
                            base_url = base_url
                        )
        self.conversation = []

    def add_message(self, role, content):
        """Adds a message to the conversation history."""
        self.conversation.append({"role": role, "content": content})

    def get_response(self):
        """Gets a response from the API based on the conversation history."""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation
        )
        return response['choices'][0]['message']['content']

    def invoke(self, user_input):
        """Handles user input and generates a response."""
        # Add the user's message to the conversation
        self.add_message("user", user_input)

        # Get the AI's response
        response = self.get_response()

        # Add the AI's response to the conversation
        self.add_message("assistant", response)

        return response    
    



