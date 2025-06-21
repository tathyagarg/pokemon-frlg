from peewee import DoesNotExist

from . import database
from . import make_command_use_header

def requires_registered(func):
    async def wrapper(**kwargs) -> dict:
        user_id = kwargs['data']['payload'].get('user_id', '')

        try:
            database.User.get(database.User.id == user_id)
        except DoesNotExist:
            return {
                'response_type': 'ephemeral',
                'text': "You need to register before you can use this command. Please use the `/start` command to get started.",
            }

        return await func(**kwargs)

    return wrapper


def requires_unregistered(func):
    async def wrapper(**kwargs) -> dict:
        user_id = kwargs['data']['payload'].get('user_id', '')

        try:
            database.User.get(database.User.id == user_id)
            return {
                'response_type': 'ephemeral',
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': "You are already registered. Please use the `/about` command to view your profile or `/start` to start a new game."
                        }
                    }
                ]
            }
        except DoesNotExist:
            return await func(**kwargs)

    return wrapper
