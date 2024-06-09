Usage:
```py
model = Model.gpt_35_turbo
text = "Hello!"
async with API(base_url='https://duckduckgo.com', headers=headers,
               chat_req_data=chat, tok_req_data=vqd) as cli:
    session = await cli.new_session(model)
    response = await cli.request_ai(session, text)
```
