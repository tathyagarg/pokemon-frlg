import json

from . client import Client

client = Client()

@client.command('/ping')
async def ping_command(data: dict) -> dict:
    return {
        'text': 'pong',
        'response_type': 'in_channel'
    }

if __name__ == "__main__":
    import asyncio

    asyncio.run(client.connect())
