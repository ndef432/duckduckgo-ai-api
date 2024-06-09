import dataclasses
import enum


class Model(enum.StrEnum):
    gpt_35_turbo = 'gpt-3.5-turbo-0125'
    claude = 'claude-3-haiku-20240307'
    llama = 'meta-llama/Llama-3-70b-chat-hf'
    mixtral = 'mistralai/Mixtral-8x7B-Instruct-v0.1'


class Role(enum.StrEnum):
    user = 'user'
    assistant = 'assistant'


@dataclasses.dataclass
class Message:
    content: str
    role: Role


@dataclasses.dataclass
class UserMessage(Message):
    role: Role = Role.user


@dataclasses.dataclass
class AssistantMessage(Message):
    role: Role = Role.assistant


@dataclasses.dataclass
class Session:
    model: Model
    vqd: str
    message_history: list[dict[str, str]] = dataclasses.field(default_factory=list)

    def add_message(self, message: Message) -> None:
        self.message_history.append({'role': message.role.value, 'content': message.content})

    def request(self, message: Message) -> dict:
        self.add_message(message)
        return {'model': self.model.value, 'messages': self.message_history}
