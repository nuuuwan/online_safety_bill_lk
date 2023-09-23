from enum import Enum


class ChatGPTRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    function = "function"
