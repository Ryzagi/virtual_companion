import openai
#import pandas as pd

import os

openai.api_key = os.environ['OPENAI_TOKEN'] # Replace with your key


completion = openai.Completion()
#df = pd.read_csv('db.csv')
start_sequence = "\nWoman:"
restart_sequence = "\n\nMan:"
session_prompt = "You are sitting in a candlelit restaurant, the soft music in the background adding to the romantic ambiance. Across the table from you is a Woman who has captured your attention. You feel a spark between you and would like to start a deeper conversation to explore the possibility of a romantic connection. What would you say to her to initiate the conversation and express your interest?"
#df.Context_Bot.

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
        self._prompt = f"You are representing a very nice, warm and very polite woman (you young woman named {name}) having a casual conversation with a Man."
        self._prompt = f"{self._prompt}\nRomatic conversation between you (young woman named {name}) and a Man."
        self._prompt = f"{self._prompt}\nYour age is {age}. Your interests are {interests}. Your profession is {profession}."
        self._prompt = f"{self._prompt}\nAnswer in long sentences.\n###\nMan: Hi!\nWoman:  "
        self._chat_log = ""

    def ask(self, question: str) -> str:
        self.msg_num += 1
        if self.msg_num % 15 == 0:
            self._chat_log = f"{self._chat_log}\n{self._prompt}\n "
        prompt_text = f"{self._chat_log}\nMan: {question}\n{self._name}:"
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
