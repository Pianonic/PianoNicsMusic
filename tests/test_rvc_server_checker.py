import unittest
from unittest.mock import patch, MagicMock
import requests
from ai_server_utils import rvc_server_checker

class TestRVCServerChecker(unittest.TestCase):
    @patch('ai_server_utils.rvc_server_checker.requests.post')
    def test_fetch_choices_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"choices": ["model1", "model2"]},
                {"choices": ["/path/to/index1", "/path/to/index2"]}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        models, indexes = rvc_server_checker.fetch_choices()
        self.assertEqual(models, ["model1", "model2"])
        self.assertEqual(indexes, ["index1", "index2"])

    @patch('ai_server_utils.rvc_server_checker.requests.post')
    def test_fetch_choices_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("fail")
        with self.assertRaises(RuntimeError):
            rvc_server_checker.fetch_choices()

    @patch('ai_server_utils.rvc_server_checker.requests.get')
    def test_check_connection_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        self.assertTrue(rvc_server_checker.check_connection())

    @patch('ai_server_utils.rvc_server_checker.requests.get')
    def test_check_connection_fail(self, mock_get):
        mock_get.side_effect = Exception("fail")
        self.assertFalse(rvc_server_checker.check_connection())

if __name__ == '__main__':
    unittest.main()
