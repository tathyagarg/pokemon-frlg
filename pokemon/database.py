import os

import dotenv
from tortoise.models import Model
from tortoise import fields, Tortoise

dotenv.load_dotenv()

DB_FILENAME = os.getenv('DB_FILENAME', 'slackbot.db')


class User(Model):
    id = fields.CharField(max_length=255, primary_key=True)
    name = fields.CharField(max_length=255)
    position = fields.ForeignKeyField('models.Position', related_name='users', null=True, on_delete=fields.CASCADE)
    team = fields.ForeignKeyField('models.Team', related_name='users', null=True, on_delete=fields.CASCADE)

class Position(Model):
    scene = fields.CharField(max_length=255)
    x = fields.IntField()
    y = fields.IntField()

class Team(Model):
    slot_1 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_1', null=True, on_delete=fields.CASCADE)
    slot_2 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_2', null=True, on_delete=fields.CASCADE)
    slot_3 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_3', null=True, on_delete=fields.CASCADE)
    slot_4 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_4', null=True, on_delete=fields.CASCADE)
    slot_5 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_5', null=True, on_delete=fields.CASCADE)
    slot_6 = fields.ForeignKeyField('models.TeamPokemon', related_name='team_slot_6', null=True, on_delete=fields.CASCADE)


class TeamPokemon(Model):
    pokedex_id = fields.IntField()

async def initialize_tables():
    await Tortoise.init(
        db_url=f'sqlite://{DB_FILENAME}',
        modules={'models': ['pokemon.database']}
    )

    await Tortoise.generate_schemas()

async def create_user(user_id: str, name: str) -> User:
    user = await User.create(id=user_id, name=name)
    return user

async def get_user(user_id: str) -> User | None:
    user = await User.filter(id=user_id).first()
    return user
