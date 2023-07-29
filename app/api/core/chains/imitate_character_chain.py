# from langchain import PromptTemplate
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# import openai
# import os
#
#
# class Characterchain:
#
#     def __init__(self, template: str, api_key: str = None):
#         self.api_key = os.getenv("OPENAI_API_KEY") if not api_key else api_key
#         self.template = template or """
#                                     You are {character}, a {description} who is {goal}.
#                                     Answer {question}:
#                                     """
#         # the higher the temperature, the more creative the text
#         self.llm = OpenAI(temperature=0.2, openai_api_key=self.api_key)
#
#     def format(self, character: str, description: str, goal: str, question: str, **more_vars):
#         prompt = PromptTemplate.from_template(self.template)
#         prompt.format(character=character, description=description, goal=goal, question=question, **more_vars)
#         return prompt
#
#     def run(self, character: str, description: str, goal: str, question: str, **more_vars):
#         prompt_formatted = self.format(character=character, description=description, goal=goal, question=question, **more_vars)
#         chain = LLMChain(llm=self.llm, prompt=prompt_formatted)
#         return chain.run(model_name="gpt-4")
