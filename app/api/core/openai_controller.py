import os
import openai
from typing import Dict, List
import json
import uuid


class OpenaiController:
    """
    Used to control OpenAI API
    """

    def __init__(self, messages: List[Dict[str, str]], api_key: str = None):
        openai.api_key = os.getenv("OPENAI_API_KEY") if not api_key else api_key
        self.messages = messages
        self.messages = [json.loads(message.json()) for message in messages]

    def answer(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        try:
            # save for lipsync
            file_path = f"{os.path.abspath(os.getcwd())}/app/api/core/assets/txt/{uuid.uuid4()}.txt"
            with open(f"{file_path}", "w") as f:
                f.write(response["choices"][0]["message"]["content"])
                f.close()
            return response["choices"][0]["message"], file_path
        except Exception as e:
            print(e)
            return

if __name__ == "__main__":
    o = OpenaiController(messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ])
    print(o.answer())