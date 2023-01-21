import openai
#import pandas as pd

import os

openai.api_key = os.environ['OPENAI_TOKEN'] # Replace with your key

completion = openai.Completion()
start_sequence = "\nWoman:"
restart_sequence = "\n\nMan:"


class GPT3Conversation:
    def __init__(
            self,
            name: str = "Alisa",
            age: str = "25",
            interests: str = "Nothing",
            profession: str = "Singer"
    ) -> None:
        self._name = name
        self.msg_num = 0
        self._prompt = "The following is a romantic conversation between an Woman and a Man. "
        self._prompt += f"Woman is very nice, warm and polite. Woman's profession is {profession}, she loves to talk about it."
        self._prompt += f"Woman's age is {age}, and she acts as average woman of her age. She is very interested at {interests}. "
        self._prompt += f"Her name is {name}."
        self._chat_log = self._prompt

    def ask(self, question: str) -> str:
        self.msg_num += 1
        if self.msg_num % 15 == 0:
            self._chat_log = f"{self._chat_log}\n{self._prompt}\n "
        prompt_text = f"{self._chat_log}\nMan: {question}\nWoman:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            temperature=0.95,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\nMan:"],
        )
        response = response['choices'][0]['text']
        self._chat_log = f"{prompt_text}{response}"
        return response

def ask(question, chat_log= None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    #print(pro)
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.95,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
