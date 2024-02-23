import os
import sys
import unittest
from unittest.mock import patch, MagicMock

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from scheduler import fetch_last_traded_price

class TestFetchLastTradedPrice(unittest.TestCase):
    @patch('scheduler.requests.get')
    def test_fetch_last_traded_price_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 203
        mock_response.json.return_value = {'last': [180.89]}
        mock_get.return_value = mock_response
        
        result = fetch_last_traded_price()
        self.assertEqual(result, 180.89)

    @patch('scheduler.requests.get')
    def test_fetch_last_traded_price_failed_request(self, mock_get):
        with self.assertRaises(Exception):
            mock_response = mock_get.return_value
            mock_response.status_code = 404

            fetch_last_traded_price()

    @patch('scheduler.requests.get')
    def test_fetch_last_traded_price_invalid_response_format(self, mock_get):
        with self.assertRaises(Exception):
            mock_response = mock_get.return_value
            mock_response.status_code = 203
            mock_response.json.return_value = {'invalid_key': 180.89}

            fetch_last_traded_price()

if __name__ == '__main__':
    unittest.main()