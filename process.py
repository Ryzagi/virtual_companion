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
        data = read_json_file('config.json')
        self._prompt = data['prompt']
        self._prompt = self._prompt.format(age=age, name=name, profession=profession, interests=interests)
        self._chat_log = self._prompt

        self._model_name = data['model']
        self._temperature = data['temperature']
        self._max_tokens = data['max_tokens']
        self._top_p = data['top_p']
        self._frequency_penalty = data['frequency_penalty']
        self._presence_penalty = data['presence_penalty']
        self._stop = data['stop']

    def ask(self, question: str) -> str:
        self.msg_num += 1
        if self.msg_num % 15 == 0:
            self._chat_log = f"{self._chat_log}\n{self._prompt}\n "
        prompt_text = f"{self._chat_log}\nMan: {question}\nWoman:"

        response = openai.Completion.create(
            engine=self._model_name,
            prompt=prompt_text,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            frequency_penalty=self._frequency_penalty,
            presence_penalty=self._presence_penalty,
            stop=self._stop,
        )
        response = response['choices'][0]['text']
        self._chat_log = f"{prompt_text}{response}"
        return response


def read_json_file(file_path):
    # Open the file
    with open(file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)
        # return the data
        return data


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
