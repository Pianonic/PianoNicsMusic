import unittest
from models.guild_music_information import Guild
from peewee import SqliteDatabase
from db_utils.db import db

class TestGuildModel(unittest.TestCase):
    def test_guild_fields(self):
        self.assertTrue(hasattr(Guild, 'id'))
        self.assertTrue(hasattr(Guild, 'loop_queue'))
        self.assertTrue(hasattr(Guild, 'shuffle_queue'))

    def test_guild_meta(self):
        self.assertEqual(Guild._meta.table_name, 'guilds')
        self.assertIs(Guild._meta.database, db)

if __name__ == '__main__':
    unittest.main()
