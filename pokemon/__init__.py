def make_command_use_header(user_id: str, command: str) -> dict:
    return {
        'type': 'context',
        'elements': [
            {
                'type': 'mrkdwn',
                'text': f'> {command} used by <@{user_id}>'
            }
        ]
    }
