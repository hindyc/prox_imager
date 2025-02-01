'''Test cases for the fetch_ubuntu_images module.'''
import unittest
from unittest.mock import patch, Mock
import requests
from prox_imager.fetch_ubuntu_images import fetch_ubuntu_metadata


class TestFetchUbuntuMetadata(unittest.TestCase):
    '''Test cases for the fetch_ubuntu_images module.'''
    def setUp(self):
        # Setup code to run before each test
        pass

    def tearDown(self):
        # Cleanup code to run after each test
        pass

    @patch("requests.get")
    def test_fetch_ubuntu_metadata_success(self, mock_get):
        '''Test fetch_ubuntu_metadata function with a successful response.'''
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"products": {}}
        mock_get.return_value = mock_response

        metadata = fetch_ubuntu_metadata("http://example.com")
        self.assertEqual(metadata, {"products": {}})
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("requests.get")
    def test_fetch_ubuntu_metadata_failure(self, mock_get):
        '''Test fetch_ubuntu_metadata function with a failed response.'''
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        metadata = fetch_ubuntu_metadata("http://example.com")
        self.assertEqual(metadata, {})
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("requests.get", side_effect=requests.exceptions.Timeout)
    def test_fetch_ubuntu_metadata_timeout(self, mock_get):
        '''Test fetch_ubuntu_metadata function with a timeout exception.'''
        metadata = fetch_ubuntu_metadata("http://example.com")
        self.assertEqual(metadata, {})
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("requests.get", side_effect=requests.exceptions.RequestException)
    def test_fetch_ubuntu_metadata_request_exception(self, mock_get):
        '''Test fetch_ubuntu_metadata function with a generic request exception.'''
        metadata = fetch_ubuntu_metadata("http://example.com")
        self.assertEqual(metadata, {})
        mock_get.assert_called_once_with("http://example.com", timeout=10)


if __name__ == '__main__':
    unittest.main()
