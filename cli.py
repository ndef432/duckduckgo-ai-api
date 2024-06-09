import asyncio
import json

from api import API
from request_data import RequestData
from session import Model

with open('request_vqd.json') as file:
    vqd = RequestData.from_dict(json.load(file))
with open('request.json') as file:
    chat = RequestData.from_dict(json.load(file))
with open('headers.json') as file:
    headers = json.load(file)


async def ai_chat(model: Model):
    async with API(base_url='https://duckduckgo.com', headers=headers,
                   chat_req_data=chat, tok_req_data=vqd) as cli:
        session = await cli.new_session(model)
        while True:
            req = await asyncio.to_thread(input, '>>>')
            if not req:
                continue
            res = await cli.request_ai(session, req)
            print(f'AI response: {res}')


def main():
    models = {str(i): el for i, el in enumerate(Model, start=1)}
    print('Choose AI model:')
    for i, model in models.items():
        print(f'{i}) {model}')
    chosen_model = None
    while not chosen_model:
        model_idx = input()
        try:
            chosen_model = Model(models[model_idx])
        except KeyError:
            print(f'Model not found')
            continue
    print(f'Chosen model: {chosen_model}')
    asyncio.run(ai_chat(chosen_model))


if __name__ == '__main__':
    main()
