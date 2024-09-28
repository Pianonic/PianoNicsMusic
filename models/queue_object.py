from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField
from db_utils.db import db
from models.guild_music_information import Guild

class QueueEntry(Model):
    id = IntegerField(primary_key=True)
    guild = ForeignKeyField(Guild, backref='queue', on_delete='CASCADE')
    url = CharField(null=False)
    already_played = BooleanField(null=False)
    force_play = BooleanField(null=False)

    class Meta:
        database = db
        table_name = 'queue_entry'