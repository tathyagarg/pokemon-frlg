import json

from httpx import AsyncClient

from pokemon.internals.movement import as_movement_tuple
from pokemon.slack import payloads

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

async def handle_left_button_press(*, data: dict) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [as_movement_tuple('a')])

    return {}

async def handle_right_button_press(*, data: dict) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [as_movement_tuple('d')])

    return {}

async def handle_up_button_press(*, data: dict) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [as_movement_tuple('w')])

    return {}

async def handle_down_button_press(*, data: dict) -> dict:
    user_id = data.get('user', {}).get('id')

    user = database.get_user(user_id)
    internals.movement.move_compound(user, [as_movement_tuple('s')])

    return {}


BUTTON_PRESS_HANDLERS = {
    'left': handle_left_button_press,
    'right': handle_right_button_press,
    'up': handle_up_button_press,
    'down': handle_down_button_press,
}

# ====================================================================================================
#                                       Plain Text Input Handlers
# ====================================================================================================

async def handle_mass_movement_input(*, data: dict) -> dict:
    state = data.get('state', {})

    movement = list(state.get('values', {}).get('mass_input', {}).get('mass_input', {}).get('value', '').replace(' ', ''))
    user_id = data.get('user', {}).get('id')

    movement_commands = []

    repeat_count = 0

    while movement:
        command = movement.pop(0)

        if command in ('w', 'a', 's', 'd'):
            dx, dy = as_movement_tuple(command)
            movement_commands.append((dx * max(repeat_count, 1), dy * max(repeat_count, 1)))
            repeat_count = 0

        elif command in '1234567890':
            repeat_count *= 10
            repeat_count += int(command)

    user = database.get_user(user_id)
    res = internals.movement.move_compound(user, movement_commands)

    if user:
        pos_x, pos_y, direction = res or (user.pos_x, user.pos_y, user.direction)
        print(pos_x, pos_y, direction)

        fname = internals.images.make_scene_image(user.scene, pos_x, pos_y, direction)  # pyright: ignore

        return {
            'replace_original': True,
            **payloads.GAME_BLOCKS(f'https://pokemon.arson.dev/{fname}'),
        }

    return {}

PLAIN_TEXT_INPUT_HANDLERS = {
    'mass_input': handle_mass_movement_input,
}
