import openai
import sys
import os
import requests
import time
from json import JSONDecodeError
from langchain_openai import ChatOpenAI  # pip install langchain_openai
from langchain.schema import AIMessage, HumanMessage, SystemMessage


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config import *


class LLM_API_Call:

    def __init__(self, type) -> None:
        if type == "openai":
            self.llm = OpenAI_API_Call(api_key = LLM_CONFIG[""],
                                       model = LLM_CONFIG["model"])
        elif type == "gilas":
            self.llm = Gilas_API_Call(api_key = GILAS_CONFIG["api_key"],
                                       model = GILAS_CONFIG["model"],
                                       base_url=GILAS_CONFIG["base_url"])
        elif type == "avalai":
          self.llm = AvalAI(api_key = aval_ai["api_key"],
                                       model = aval_ai["model"],
                                       base_url=aval_ai["base_url"])

    def get_LLM_response(self, prompt: str) -> str:
        return self.llm.get_LLM_response(prompt, " ")

class AvalAI:
    
    def __init__(self, model: str, base_url: str, api_key: str) -> None:
        self.model_name = model
        self.base_url = base_url
        self.api_key = api_key
        self.conversation = []
        self._model = ChatOpenAI(
                model=model,
                # temperature=0,
                # max_tokens=None,
                # timeout=None,
                # max_retries=2,
                api_key=api_key,  # if you prefer to pass api key in directly instaed of using env vars
                base_url=base_url,
            )
        
    def get_LLM_response(self, prompt: str, status: str) -> str:
        
        # Extend the conversation history with the new prompt
        self.conversation.append(HumanMessage(content=prompt))
        
        # Combine all conversation history into a single input
        
        full_conversation = [SystemMessage(content="status")] + self.conversation
        
        # Get the model's response based on the full conversation history
        response = self._model(full_conversation)
        
        # Since the response is likely an object, access its content directly
        assistant_response = response.content  # Accessing the content directly
        
        # Add the assistant's response to the conversation history
        self.conversation.append(AIMessage(content=assistant_response))
        return  assistant_response
        


class OpenAI_API_Call:

    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        openai.api_key = api_key
        self.model = model
        self.conversation = []

    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def get_response(self):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.conversation
        )
        return response['choices'][0]['message']['content']

    def invoke(self, user_input):
        self.add_message("user", user_input)

        response = self.get_response()

        self.add_message("assistant", response)

        return response


class Gilas_API_Call:
    def __init__(self, api_key, base_url, model="gpt-4o-mini"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.conversation = []

    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def get_response(self):
        data = {
            "model": self.model,
            "messages": self.conversation
        }

        response = requests.post(
            url=f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:
            try:
                return response.json()['choices'][0]['message']['content']
            except (KeyError, IndexError, ValueError) as e:
                raise Exception(f"Unexpected API response format: {e}")
        else:
            raise Exception(f"Gilas API call failed: {response.status_code} - {response.text}")

    def invoke(self, user_input, max_retries=3, initial_wait=30):
        self.add_message("user", user_input)

        retries = 0
        wait_time = initial_wait
        while retries < max_retries:
            try:
                response = self.get_response()
                self.add_message("assistant", response)
                return response
            except (JSONDecodeError, Exception) as e:
                print(f"Error encountered: {e}. Retrying in {wait_time} seconds...")
                retries += 1
                time.sleep(wait_time)
                wait_time += 30
        raise Exception(f"Failed to get a valid response after {max_retries} retries.")