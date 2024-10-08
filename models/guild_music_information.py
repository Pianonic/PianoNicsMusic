from peewee import Model, IntegerField, BooleanField
from db_utils.db import db

class Guild(Model):
    id = IntegerField(primary_key=True)
    loop_queue = BooleanField(null=False)
    shuffle_queue = BooleanField(null=False)

    class Meta:
        database = db
        table_name = 'guilds'