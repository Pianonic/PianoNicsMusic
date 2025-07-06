import unittest
from db_utils.db import db, setup_db
from peewee import SqliteDatabase

class TestDB(unittest.TestCase):
    def test_db_is_sqlite_memory(self):
        self.assertIsInstance(db, SqliteDatabase)
        self.assertEqual(str(db.database), ':memory:')

    def test_setup_db_runs(self):
        # Patch models and db methods
        import types
        db.is_connection_usable = lambda: False
        db.connect = lambda: None
        db.create_tables = lambda tables, safe: None
        # Patch import
        sys_modules_backup = dict(__import__('sys').modules)
        import sys
        sys.modules['models.guild_music_information'] = types.SimpleNamespace(Guild='Guild')
        sys.modules['models.queue_object'] = types.SimpleNamespace(QueueEntry='QueueEntry')
        try:
            import asyncio
            asyncio.run(setup_db())
        finally:
            __import__('sys').modules.clear()
            __import__('sys').modules.update(sys_modules_backup)

if __name__ == '__main__':
    unittest.main()
