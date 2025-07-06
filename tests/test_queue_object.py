import unittest
from models.queue_object import QueueEntry
from peewee import SqliteDatabase
from db_utils.db import db

class TestQueueEntryModel(unittest.TestCase):
    def test_queue_entry_fields(self):
        self.assertTrue(hasattr(QueueEntry, 'id'))
        self.assertTrue(hasattr(QueueEntry, 'guild'))
        self.assertTrue(hasattr(QueueEntry, 'url'))
        self.assertTrue(hasattr(QueueEntry, 'already_played'))
        self.assertTrue(hasattr(QueueEntry, 'force_play'))

    def test_queue_entry_meta(self):
        self.assertEqual(QueueEntry._meta.table_name, 'queue_entry')
        self.assertIs(QueueEntry._meta.database, db)

if __name__ == '__main__':
    unittest.main()
