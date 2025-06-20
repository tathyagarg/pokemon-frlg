import re

import httpx
from tortoise import run_async

from . import database
from . import slack
from .client import Client

client = Client()

@client.command('/ping')
async def ping_command(_: dict) -> dict:
    return {
        'text': 'Pong!',
        'response_type': 'in_channel'
    }


@client.command('/start')
async def start_command(data: dict) -> dict:
    payload = data.get('payload', {})

    channel_id = payload.get('channel_id')
    user_id = payload.get('user_id')

    async with httpx.AsyncClient() as http_client:
        await http_client.post(
            f'https://slack.com/api/{slack.constants.EP_VIEW_OPEN}',
            headers={
                'Authorization': f'Bearer {client.BOT_TOKEN}',
            },
            json=slack.payloads.START_GAME_MODAL(payload.get('trigger_id'), f'{channel_id}|{user_id}')
        )

    return {}


@client.command('/about')
async def about_command(data: dict) -> dict:
    payload = data.get('payload', {})
    command_text = payload.get('text', '').strip()

    user_id = payload.get('user_id')
    if command_text:
        if (m := re.match(r'^<@([a-zA-Z0-9]+)|.*>', command_text)):
            user_id = m.group(1)

    user = await database.get_user(user_id)
    if not user:
        return {
            'text': 'User not found.',
            'response_type': 'ephemeral'
        }

    return {
	    "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"About {user.name if user else 'Unknown User'}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"Position: {user.position.scene if user and user.position else 'Unknown'}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"Team: {user.team.slot_1.pokedex_id if user and user.team and user.team.slot_1 else 'Unknown'}"
                    }
                ]
            }
	    ],
        'response_type': 'in_channel'
    }


@client.command('/game')
async def game_command(data: dict) -> dict:
    ...


if __name__ == "__main__":
    import asyncio

    run_async(database.initialize_tables())
    asyncio.run(client.connect())
