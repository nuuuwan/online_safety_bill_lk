import math
import os
from functools import cached_property

import openai
from utils import Log

from osb_lk.ChatGPTRole import ChatGPTRole

MODEL = "gpt-4"
TEMPERATURE = 0.5
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

PREAMBLE_CONTEXT = 'The following is an excerpt from a document:'
POSTAMBLE_CONTEXT = 'You will be asked a set of questions about the document.'

CHARS_PER_BULLET = 1_000

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
        raw_response_msg = response.choices[0]['message']['content']
        self.messages.append(
            ChatGPT.build_message(ChatGPTRole.assistant, raw_response_msg)
        )
        return raw_response_msg

    @cached_property
    def title(self):
        return self.send(
            [
                'State the part number and title of the excerpt'
                + ' in the format PART <number>: <title>.'
            ]
        )

    @cached_property
    def summary(self):
        self.send(
            [
                f'Summarize into {self.n_bullets} bullet points',
            ]
        )
        return self.send(
            [
                'Add emojis, hashtags and handles to the summary.',
            ]
        )
