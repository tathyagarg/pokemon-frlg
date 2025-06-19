import re

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
async def start_command(data: dict) -> dict:
    payload = data.get('payload', {})
    
    async with httpx.AsyncClient() as http_client:
        await http_client.post(
            f'https://slack.com/api/{slack_constants.EP_VIEW_OPEN}',
            headers={
                'Authorization': f'Bearer {client.BOT_TOKEN}',
            },
            json={
                'trigger_id': payload.get('trigger_id'),
                'view': {
                    'type': 'modal',
                    'title': {
                        'type': 'plain_text',
                        'text': 'Start your journey!',
                    },
                    'blocks': [
                        {
                            'type': 'input',
                            'block_id': 'gender',
                            'label': {
                                'type': 'plain_text',
                                'text': 'Gender'
                            },
                            'element': {
                                'type': 'static_select',
                                'placeholder': {
                                    'type': 'plain_text',
                                    'text': 'Select your gender'
                                },
                                'options': [
                                    {
                                        'text': {
                                            'type': 'plain_text',
                                            'text': 'Male'
                                        },
                                        'value': 'male'
                                    },
                                    {
                                        'text': {
                                            'type': 'plain_text',
                                            'text': 'Female'
                                        },
                                        'value': 'female'
                                    },
                                    {
                                        'text': {
                                            'type': 'plain_text',
                                            'text': 'Other'
                                        },
                                        'value': 'other'
                                    },
                                ],
                                'action_id': 'gender'
                            }
                        },
                        {
                            'type': 'input',
                            'block_id': 'name',
                            'label': {
                                'type': 'plain_text',
                                'text': 'Your Name (your Slack name will be used if you leave this blank)',
                            },
                            'element': {
                                'type': 'plain_text_input',
                                'action_id': 'name',
                                'placeholder': {
                                    'type': 'plain_text',
                                    'text': 'Enter your name'
                                },
                                'multiline': False,
                            },
                            'optional': True
                        },
                        {
                            'type': 'input',
                            'block_id': 'opponent',
                            'label': {
                                'type': 'plain_text',
                                'text': 'Opponent Name (optional, defaults to Gary)',
                            },
                            'element': {
                                'type': 'plain_text_input',
                                'action_id': 'opponent',
                                'placeholder': {
                                    'type': 'plain_text',
                                    'text': 'Enter your opponent\'s name'
                                },
                                'multiline': False,
                            },
                            'optional': True
                        }
                    ],
                    'close': {
                        'type': 'plain_text',
                        'text': 'Cancel'
                    },
                    'submit': {
                        "type": "plain_text",
                        "text": "Start!"
                    },
                    'callback_id': 'start_game_modal',
                }
            }
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
