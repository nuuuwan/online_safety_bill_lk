import math
import os
import time
from functools import cached_property

import openai
from utils import Log

from osb_lk.ChatGPTRole import ChatGPTRole

MODEL = "gpt-4"
TEMPERATURE = 0.5
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

PREAMBLE_CONTEXT = 'The following is a part from a document:'
POSTAMBLE_CONTEXT = 'You will be asked a set of questions about the part.'

CHARS_PER_BULLET = 1_000
T_SLEEP_AFTER_RESPONSE = 2

log = Log("ChatGPT")


class ChatGPT:
    @staticmethod
    def build_message(role: ChatGPTRole, content: str) -> dict:
        return {
            "role": role,
            "content": content,
        }

    def __init__(self, story_lines: list[str]):
        self.n_lines = len(story_lines)
        self.n_chars = sum([len(line) for line in story_lines])
        self.n_bullets = math.ceil(self.n_chars / CHARS_PER_BULLET)
        log.debug(
            f'ChatGPT({self.n_lines=:,}, {self.n_chars=:,}, '
            + f'{self.n_bullets=:,})'
        )

        self.story_lines = story_lines
        story = '\n'.join(story_lines)
        self.messages = [
            ChatGPT.build_message(ChatGPTRole.system, PREAMBLE_CONTEXT),
            ChatGPT.build_message(ChatGPTRole.user, story),
            ChatGPT.build_message(ChatGPTRole.system, POSTAMBLE_CONTEXT),
        ]

    def send(self, message_lines: list[str]) -> str:
        new_message = ChatGPT.build_message(
            ChatGPTRole.user,
            '\n'.join(message_lines),
        )
        self.messages.append(new_message)
        n_messages = len(self.messages)
        log.debug(f'ChatGPT().send({n_messages=})')

        response = openai.ChatCompletion.create(
            model=MODEL,
            temperature=TEMPERATURE,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
            messages=self.messages,
        )
        time.sleep(T_SLEEP_AFTER_RESPONSE)
        raw_response_msg = response.choices[0]['message']['content']
        self.messages.append(
            ChatGPT.build_message(ChatGPTRole.assistant, raw_response_msg)
        )
        return raw_response_msg

    @cached_property
    def title(self):
        return self.send(['Suggest an appropriate title for this part.'])

    @cached_property
    def short_summary(self):
        return self.send(
            [
                'Summarize the part in one brief sentence.',
            ]
        )

    @cached_property
    def summary(self):
        self.send(
            [
                f'Summarize into {self.n_bullets} numbered bullet points',
            ]
        )
        return self.send(
            [
                'In summary, add emojis next to words, '
                + 'and replace words with hashtags and handles '
                + 'where appropriate.',
            ]
        )

    @cached_property
    def improvements(self):
        return self.send(
            [
                'Briefly list 2-5 ways this legislation might be improved.',
            ]
        )
