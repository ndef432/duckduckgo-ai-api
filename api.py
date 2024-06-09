import dataclasses
import io
import json

from http_client import HTTPClient
from request_data import RequestData
from session import Session, UserMessage, Model, AssistantMessage


@dataclasses.dataclass(kw_only=True)
class API(HTTPClient):
    chat_req_data: RequestData
    tok_req_data: RequestData

    async def new_session(self, model: Model) -> Session:
        async with self.get(self.tok_req_data.url,
                            headers=self.tok_req_data.headers) as response:
            return Session(model=model, vqd=response.headers['x-vqd-4'])

    def _parse_sse(self, sse_data: bytes) -> list[dict]:
        result = []
        finished = False
        for line in sse_data.splitlines():
            if not line:
                continue
            if finished:
                raise ValueError('Bad SSE: continuation after [DONE]')
            content = line.removeprefix(b'data: ')
            if content == b'[DONE]':
                finished = True
                continue
            content = json.loads(content)
            result.append(content)
        return result

    def _construct_message(self, response: list[dict]) -> str:
        message = io.StringIO()
        for el in response:
            if el['action'] != 'success':
                raise ValueError(f'Non-successful token generation: {el}')
            # there's no role field in the gpt model's responses
            # if el['role'] != Role.assistant:
            #     raise ValueError(f'Non-assistant role in server response: {el}')
            message.write(el.get('message', ''))
        message.seek(0)
        return message.read()

    async def request_ai(self, session: Session, text: str) -> str:
        history = session.request(UserMessage(text))
        headers = dict(self.chat_req_data.headers)
        headers['x-vqd-4'] = session.vqd
        async with self.post(self.chat_req_data.url,
                             headers=headers,
                             json=history) as response:
            session.vqd = response.headers['x-vqd-4']
            content = self._construct_message(self._parse_sse(await response.read()))
            session.add_message(AssistantMessage(content))
            return content
