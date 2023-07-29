import os
import openai
from typing import Dict, List

class OpenaiController:
    """
    Used to control OpenAI API
    """

    def __init__(self, messages: List[Dict[str, str]], api_key: str = None):
        openai.api_key = os.getenv("OPENAI_API_KEY") if not api_key else api_key
        self.messages = messages

    def answer(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        try:
            return response["choices"][0]["message"]
        except Exception as e:
            print(e)
            return

if __name__ == "__main__":
    o = OpenaiController(messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ])
    print(o.answer())