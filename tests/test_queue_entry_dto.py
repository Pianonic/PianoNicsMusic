import unittest
from models.dtos.QueueEntryDto import QueueEntryDto

class TestQueueEntryDto(unittest.TestCase):
    def test_queue_entry_dto_fields(self):
        dto = QueueEntryDto(url='test_url', already_played=True)
        self.assertEqual(dto.url, 'test_url')
        self.assertTrue(dto.already_played)

if __name__ == '__main__':
    unittest.main()
