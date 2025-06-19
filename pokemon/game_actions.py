import json

from . import database

async def handle_submit_start_game_modal(data: dict) -> None:
    print(json.dumps(data, indent=2))

    user_id = data.get('user', {}).get('id')
    user_name = data.get('user', {}).get('name')

    view = data.get('view', {})

    state = view.get('state', {}).get('values', {})

    gender = state.get('gender', {}).get('gender', {}).get('selected_option', {}).get('value')
    name = state.get('name', {}).get('name', {}).get('value') or user_name
    opponent = state.get('opponent', {}).get('opponent', {}).get('value') or 'Gary'

    await database.User.create(id=user_id, gender=gender, name=name, opponent=opponent)

    return


VIEW_SUBMISSION_HANDLERS = {
    'start_game_modal': handle_submit_start_game_modal,
}
