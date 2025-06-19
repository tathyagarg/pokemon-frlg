import re
import json

import httpx
from tortoise import run_async

from . import database
from . import slack_constants
from .client import Client

client = Client()

@client.command('/ping')
async def ping_command(_: dict) -> dict:
    return {
        'text': 'Pong!',
        'response_type': 'in_channel'
    }

@client.command('/start')
async def game_command(data: dict) -> dict:
    payload = data.get('payload', {})

    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(
            f'https://slack.com/api/{slack_constants.EP_USER_PROFILE_GET}?user={payload["user_id"]}',
            headers={
                'Authorization': f'Bearer {client.BOT_TOKEN}',
            }
        )

        data = response.json()
        if not data.get('ok'):
            return {
                'text': 'Failed to retrieve user profile.',
                'response_type': 'ephemeral'
            }

        user_profile = data.get('profile', {})

        user_name = user_profile.get('display_name', user_profile.get('real_name', 'Unknown User'))

    result = await database.create_user(payload['user_id'], user_name)
    if not result:
        return {
            'text': 'Failed to create user.',
            'response_type': 'ephemeral'
        }

    mention = f'<@{payload["user_id"]}>'

    return {
        'text': f'{mention} has started a game!',
        'response_type': 'in_channel'
    }

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

if __name__ == "__main__":
    import asyncio

    run_async(database.initialize_tables())
    asyncio.run(client.connect())
