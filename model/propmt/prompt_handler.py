from typing import List

class Prompt:

    def get_prompt(self, message:str, info_list: List) -> str:
        prompt = f"As a user, I want to ask you the following legal question:\n{message}\n\n"

        if info_list:
            prompt += "Here are some relevant legal cases and information you should consider:\n"
            for i, info in enumerate(info_list):
                prompt += f"case {i+1}:\n{info['title']}\n{info['text']}\n"

        prompt += "\nBased on the provided information, please respond in Persian(Farsi) with a concise legal analysis.\
                    Ensure that your response is as summarized and clear as possible. (one paragraph)"

        return prompt