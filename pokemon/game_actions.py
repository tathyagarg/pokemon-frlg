from httpx import AsyncClient

from . import database
from . import slack
from . import checks

async def handle_submit_start_game_modal(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')
    user_name = data.get('user', {}).get('name')

    view = data.get('view', {})

    state = view.get('state', {}).get('values', {})

    gender = state.get('gender', {}).get('gender', {}).get('selected_option', {}).get('value')
    name = state.get('name', {}).get('name', {}).get('value') or user_name
    opponent = state.get('opponent', {}).get('opponent', {}).get('value') or 'Gary'

    await database.User.create(id=user_id, gender=gender, name=name, opponent=opponent)

    private_metadata = data.get('view', {}).get('private_metadata')
    if private_metadata:
        channel_id, user_id = private_metadata.split('|', 1)

        resp = await client.post(
            f'https://slack.com/api/{slack.constants.EP_CHAT_POST_MESSAGE}',
            headers={
                'Authorization': f'Bearer {bot_token}',
                'Content-Type': 'application/json; charset=utf-8'
            },
            json={
                'channel': channel_id,
                'blocks': [
                    {
                        'type': 'context',
                        'elements': [
                            {
                                'type': 'mrkdwn',
                                'text': f'> /start used by <@{user_id}>'
                            }
                        ]
                    },
                    {
                        'type': 'header',
                        'text': {
                            'type': 'plain_text',
                            'text': f'{name} has started a game!',
                        }
                    },
                ],
                'response_type': 'in_channel'
            }
        )

    return {}


VIEW_SUBMISSION_HANDLERS = {
    'start_game_modal': handle_submit_start_game_modal,
}

# ====================================================================================================

# @checks.requires_registered
async def handle_left_button_press(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    return {}

BUTTON_PRESS_HANDLERS = {
    'left': handle_left_button_press,
}

