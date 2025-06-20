import os
import json
from typing import Callable

import httpx
import dotenv
import websockets

from .slack import constants
from . import game_actions

class Client:
    def __init__(self):
        dotenv.load_dotenv()

        self.APP_TOKEN: str = os.getenv('SLACK_APP_TOKEN', '')
        self.BOT_TOKEN: str = os.getenv('SLACK_BOT_TOKEN', '')

        self.commands: dict[str, Callable] = {}

        self.ws: websockets.ClientConnection | None = None
        self.client: httpx.AsyncClient | None = None

        self._interactive_handlers_map = {
            'view_submission': self._view_submission_handler,
            'block_actions': self._block_actions_handler,
        }

    async def connect(self) -> None:
        async with httpx.AsyncClient() as client:
            self.client = client

            data = await client.post(
                f"https://slack.com/api/{constants.EP_APP_OPEN_CONNECTION}",
                headers={
                    'Content-Type': 'application/w-www-form-urlencoded',
                    'Authorization': f'Bearer {self.APP_TOKEN}'
                }
            )

            if data.status_code != 200:
                raise Exception(f"Failed to connect: {data.text}")

            response = data.json()
            if not response.get('ok'):
                raise Exception(f"Connection failed: {response.get('error', 'Unknown error')}")

            print("Connection established successfully.")

            await self.run(response['url'])

    async def run(self, url: str) -> None:
        async with websockets.connect(url) as ws:
            self.ws = ws

            hello = await ws.recv()
            self._handle_hello(json.loads(hello))
            
            print("Hello event received, starting to listen for events...")

            async for message in ws:
                data = json.loads(message)
                await self._handle_event(data)

    def command(self, command: str):
        """
            Decorator to register a command handler.
        """
        def decorator(func):
            self.commands[command] = func

            return func

        return decorator

    def _handle_hello(self, data: dict) -> None:
        """
            https://api.slack.com/events/hello
        """
        assert data.get('type') == 'hello', "Expected 'hello' type message"

    async def _handle_event(self, data: dict) -> None:
        if data['type'] == constants.EVENT_SLASH_COMMAND:
            payload = data.get('payload', {})

            command = payload.get('command')
            if command in self.commands:
                envelope_id = data.get('envelope_id')
                if envelope_id:
                    await self.acknowledge(envelope_id)

                response = await self.commands[command](data=data)

                if response:
                    response_url = payload.get('response_url')
                    if response_url and self.client:
                        _ = await self.client.post(
                            response_url,
                            json=response,
                            headers= {
                                'Content-Type': 'application/json',
                                'Authorization': f'Bearer {self.APP_TOKEN}'
                            }
                        )

            else:
                print(f"No handler registered for command '{command}'")
        elif data['type'] == constants.EVENT_INTERACTIVE:
            await self._interactive_handler(data)
        else:
            print(f"Unhandled event type: {data['type']} with:")
            print(json.dumps(data, indent=2))

    async def acknowledge(self, envelope_id: str) -> None:
        """
            Acknowledge the command to Slack.
        """
        if self.ws is None:
            raise Exception("WebSocket connection is not established.")

        print(f"Acknowledging envelope ID: {envelope_id}")

        await self.ws.send(json.dumps({
            'envelope_id': envelope_id,
        }))

    async def _interactive_handler(self, data: dict) -> None:
        payload = data.get('payload', {})

        handler = self._interactive_handlers_map.get(payload.get('type'))
        if handler:
            await self.acknowledge(data.get('envelope_id', ''))
            await handler(payload)
        else:
            print(f"No handler registered for interactive type '{payload.get('type')}'")

    async def _view_submission_handler(self, payload: dict) -> None:
        view = payload.get('view', {})
        calback_id = view.get('callback_id')

        if (handler := game_actions.VIEW_SUBMISSION_HANDLERS.get(calback_id)):
            await handler(payload, self.client or httpx.AsyncClient(), self.APP_TOKEN, self.BOT_TOKEN)
        else:
            print(f"No handler registered for view submission with callback ID '{calback_id}'")

    async def _block_actions_handler(self, payload: dict) -> None:
        actions = payload.get('actions', [])
        for action in actions:
            action_type = action.get('type')

            if action_type == 'button':
                if (handler := game_actions.BUTTON_PRESS_HANDLERS.get(action.get('value'))):
                    resp = await handler(payload, self.client or httpx.AsyncClient(), self.APP_TOKEN, self.BOT_TOKEN)

                    if resp:
                        response_url = payload.get('response_url')
                        if response_url and self.client:
                            await self.client.post(
                                response_url,
                                json=resp,
                                headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {self.APP_TOKEN}'
                                }
                            )
            else:
                print(f"Unhandled action type: {action_type} in block actions with payload: {json.dumps(payload, indent=2)}")

