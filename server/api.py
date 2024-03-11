import uuid
import asyncio
import logging
from ray import serve
from queue import Empty
from urllib.parse import parse_qs

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_core.messages import AIMessage, HumanMessage

from app_model import Model
from app_logic import Logic

LINE= ''.join('-' for _ in range(140))
logger = logging.getLogger('ray.serve')
app = FastAPI()

@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 0, 'num_gpus': 1})
@serve.ingress(app)
class LLMServe:
    def __init__(self):

        self.loop = asyncio.get_running_loop()

        llm= Model()
        logic = Logic(llm())

        self.streamer = llm.streamer
        self.chain=logic.chain

        self.connections= {}
        self.users = {}

    @app.websocket("/")
    async def handle_request(self, websocket: WebSocket) -> None:

        await websocket.accept()

        query_params= parse_qs(websocket.url.query)
        username= query_params.get('username')[0]
        _uuid = str(uuid.uuid4())

        if username is None:
            await websocket.close()

        await self.register(websocket, _uuid, username)
        for text in f'Hello {username}, how can I assist you?'.split():
            await asyncio.sleep(0.07)
            await websocket.send_text(text + ' ')

        try:
            while True:

                prompt = await websocket.receive_text()

                if prompt.strip() != '':
                    logger.info(f'Got prompt: {prompt}')
                    convo= self.users[_uuid]['state']['conversation']
                    if len(convo)> 6:
                        convo = convo[-6:]
                    self.loop.run_in_executor(None, self.chain.invoke, {'question':prompt, 'chat_history':convo})
                    convo.append(HumanMessage(content= prompt))
                    response= ''
                    async for text in self._stream():
                        await websocket.send_text(text)
                        response += text
                    await websocket.send_text('<<Response Finished>>')
                    convo.append(AIMessage(content= response))
                    #await self.broadcast()
                    logger.info(f"\n{LINE}\n{username} sent a message, new history:\n{self.users[_uuid]['state']}\n{LINE}")

        except WebSocketDisconnect:
            await self.unregister(_uuid)

    async def register(self, websocket, _uuid, username):

        self.connections[_uuid]= websocket
        self.users[_uuid] = {
            'username': username,
            'state': {
                'conversation': []
            }
        }

        logger.info(f"\n{LINE}\nRegistered:\nUsername: {username}\nUUID: {_uuid}\n{LINE}")

    async def unregister(self, _uuid):

        logger.info(f"\n{LINE}\nUnregistered\nUsername: {self.users[_uuid]['username']}\nUUID: {_uuid}\n{LINE}")
        del self.users[_uuid]
    
    async def broadcast(self):
        for _, connection in self.connections.items():
            _dict= self.users
            await connection.send_json(_dict)


    async def _stream(self):

        while True:
            try:
                for chunk in self.streamer:
                    logger.info(f'Yielding token: "{chunk}"')
                    yield chunk
                break
            except Empty:
                await asyncio.sleep(0.001)

deployment = LLMServe.bind()
