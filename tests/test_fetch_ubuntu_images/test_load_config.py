'''Test cases for the fetch_ubuntu_images module.'''
import unittest
from unittest.mock import patch, mock_open

import toml

from prox_imager.fetch_ubuntu_images import load_config


class TestLoadConfig(unittest.TestCase):
    '''Test cases for the fetch_ubuntu_images module.'''
    def setUp(self):
        # Setup code to run before each test
        pass

    def tearDown(self):
        # Cleanup code to run after each test
        pass

    @patch("builtins.open",
           new_callable=mock_open,
           read_data='{"urls": {"ubuntu_json_url": "http://example.com"}, \
                       "files": {"output_file": "output.json"}}')
    @patch("toml.load")
    def test_load_config_success(self, mock_toml_load, mock_file_open):
        '''Test load_config function with a valid TOML file.'''
        mock_toml_load.return_value = {"urls": {"ubuntu_json_url": "http://example.com"},
                                       "files": {"output_file": "output.json"}}
        config = load_config("dummy_path")
        self.assertEqual(config, {"urls": {"ubuntu_json_url": "http://example.com"},
                                  "files": {"output_file": "output.json"}})
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")
        mock_toml_load.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file_open):
        '''Test load_config function with a non-existent file.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=PermissionError)
    def test_load_config_permission_error(self, mock_file_open):
        '''Test load_config function with a file that cannot be opened due to permission error.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data='invalid_toml')
    @patch("toml.load", side_effect=toml.TomlDecodeError("Error", "doc", 0))
    def test_load_config_toml_decode_error(self, mock_toml_load, mock_file_open):
        '''Test load_config function with a TOML file that cannot be decoded.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")
        mock_toml_load.assert_called_once()

    @patch("builtins.open", side_effect=IOError)
    def test_load_config_io_error(self, mock_file_open):
        '''Test load_config function with a file that cannot be opened due to an IOError.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")


if __name__ == '__main__':
    unittest.main()
