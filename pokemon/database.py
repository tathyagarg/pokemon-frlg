import os
import enum

import dotenv
from peewee import ForeignKeyField, IntegerField, SqliteDatabase, Model, CharField

dotenv.load_dotenv()

DB_FILENAME = os.getenv('DB_FILENAME', 'slackbot.db')

db = SqliteDatabase(DB_FILENAME)

class EnumField(CharField):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.choices = choices
        self.max_length = 255

    def db_value(self, value):
        return value.value

    def python_value(self, value):
        return self.choices(type(list(self.choices)[0].value)(value))


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'


class TeamPokemon(Model):
    pokedex_id = IntegerField()

    class Meta:
        database = db
        table_name = 'team_pokemon'


class Team(Model):
    slot_1 = ForeignKeyField(TeamPokemon, related_name='team_slot_1', null=True)
    slot_2 = ForeignKeyField(TeamPokemon, related_name='team_slot_2', null=True)
    slot_3 = ForeignKeyField(TeamPokemon, related_name='team_slot_3', null=True)
    slot_4 = ForeignKeyField(TeamPokemon, related_name='team_slot_4', null=True)
    slot_5 = ForeignKeyField(TeamPokemon, related_name='team_slot_5', null=True)
    slot_6 = ForeignKeyField(TeamPokemon, related_name='team_slot_6', null=True)
    
    class Meta:
        database = db
        table_name = 'team'

class User(Model):
    id = CharField(max_length=255, primary_key=True, unique=True)
    gender = EnumField(Gender, default='other')

    name = CharField(max_length=255)
    opponent_name = CharField(max_length=255, default='Gary')

    team = ForeignKeyField(Team, related_name='users', null=True)

    scene = CharField(default='start')
    pos_x = IntegerField(default=0)
    pos_y = IntegerField(default=0)

    class Meta:
        database = db
        table_name = 'user'

def initialize_tables():
    with db:
        db.create_tables([User, Team, TeamPokemon], safe=True)

def create_user(user_id: str, name: str) -> User:
    user = User.create(id=user_id, name=name)
    return user

def get_user(user_id: str) -> User | None:
    user = User.filter(id=user_id).first()
    return user
