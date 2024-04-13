import uuid
import asyncio
import logging
from ray import serve
from urllib.parse import parse_qs

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from model import vLLM_Engine
from logic import Router
LINE= ''.join('-' for _ in range(140))

logger= logging.getLogger('ray.serve')
app= FastAPI()

# Setup CORS exceptions
origins = [
    'http://localhost:8000',
    'http://localhost:3000',
    '*'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)

@serve.deployment(
    num_replicas=1,
    ray_actor_options={"num_cpus": 0, 'num_gpus': 1},
    max_concurrent_queries=100
)

@serve.ingress(app)
class LLMServe:
    def __init__(self):
        engine= vLLM_Engine()
        self.logic=Router(engine)

        self.connections= {}
        logger.info('Setup Complete')

    @app.websocket("/")
    async def handle_request(self, websocket: WebSocket) -> None:

        await websocket.accept()
        query_params= parse_qs(websocket.url.query)
        username= query_params.get('username')[0]

        if username is None:
            await websocket.close()

        _uuid= await self.register(websocket, username)
        for text in f'Hello {username}, how can I assist you?'.split():
            await asyncio.sleep(0.07)
            await websocket.send_text(text + ' ')

        try:
            while True:
                prompt = await websocket.receive_text()
                if prompt.strip() != '':
                    output= await self.logic.invoke_chat(prompt, self.connections[_uuid]['state']['conversation'], _uuid, 5)
                    response= ''
                    async for text in output:
                        await websocket.send_text(text)
                        response+= text
                    await websocket.send_text('<<Response Finished>>')
                    self.connections[_uuid]['state']['conversation'].append({'role': 'assistant', 'content': response})

        except WebSocketDisconnect:
            await self.unregister(_uuid)

    async def register(self, websocket, username):
        _uuid= str(uuid.uuid4())

        self.connections[_uuid] = {
            'connection':websocket,
            'username': username,
            'state': {
                'conversation': []
            }
        }

        logger.info(f"\n{LINE}\nRegistered:\nUsername: {username}\nUUID: {_uuid}\n{LINE}")
        return _uuid


    async def unregister(self, _uuid):
        logger.info(f"\n{LINE}\nUnregistered\nUsername: {self.connections[_uuid]['username']}\nUUID: {_uuid}\n{LINE}")
        del self.connections[_uuid]
    
    async def broadcast(self):
        for _, connection in self.connections.items():
            _dict= self.users
            await connection.send_json(_dict)

deployment = LLMServe.bind()