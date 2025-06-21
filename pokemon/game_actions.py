from httpx import AsyncClient

from . import database, make_command_use_header
from . import slack
from . import make_command_use_header
from . import internals

async def handle_submit_start_game_modal(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')
    user_name = data.get('user', {}).get('name')

    view = data.get('view', {})

    state = view.get('state', {}).get('values', {})

    gender_raw = state.get('gender', {}).get('gender', {}).get('selected_option', {}).get('value')
    name = state.get('name', {}).get('name', {}).get('value') or user_name
    opponent = state.get('opponent', {}).get('opponent', {}).get('value') or 'Gary'
    
    gender = database.Gender(gender_raw)

    database.User.create(id=user_id, gender=gender, name=name, opponent=opponent)

    private_metadata = data.get('view', {}).get('private_metadata')
    if private_metadata:
        channel_id, user_id = private_metadata.split('|', 1)

        await client.post(
            f'https://slack.com/api/{slack.constants.EP_CHAT_POST_MESSAGE}',
            headers={
                'Authorization': f'Bearer {bot_token}',
                'Content-Type': 'application/json; charset=utf-8'
            },
            json={
                'channel': channel_id,
                'blocks': [
                    make_command_use_header(user_id, '/start'),
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

async def handle_left_button_press(data: dict, _client: AsyncClient, _app_token: str, _bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [(-1, 0)])

    return {}

async def handle_right_button_press(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [(1, 0)])

    return {}

async def handle_up_button_press(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [(0, -1)])

    return {}

async def handle_down_button_press(data: dict, client: AsyncClient, _: str, bot_token: str) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [(0, 1)])

    return {}


BUTTON_PRESS_HANDLERS = {
    'left': handle_left_button_press,
    'right': handle_right_button_press,
    'up': handle_up_button_press,
    'down': handle_down_button_press,
}

