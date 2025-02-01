'''Test cases for the fetch_ubuntu_images module.'''
import unittest
from unittest.mock import patch, mock_open

import os
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

    @patch("os.path.exists", return_value=False)
    def test_load_config_file_not_found(self, mock_exists):
        '''Test load_config function with a non-existent file.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_exists.assert_called_once_with("dummy_path")

    @patch("os.path.exists", return_value=True)
    @patch("os.access", return_value=False)
    def test_load_config_permission_denied(self, mock_access, mock_exists):
        '''Test load_config function with a file that cannot be accessed.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_exists.assert_called_once_with("dummy_path")
        mock_access.assert_called_once_with("dummy_path", os.R_OK)

    @patch("os.path.exists", return_value=True)
    @patch("os.access", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid_toml')
    @patch("toml.load", side_effect=toml.TomlDecodeError("Error", "doc", 0))
    def test_load_config_toml_decode_error(self,
                                           mock_toml_load,
                                           mock_file_open,
                                           mock_access,
                                           mock_exists):
        '''Test load_config function with a TOML file that cannot be decoded.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {})
        mock_exists.assert_called_once_with("dummy_path")
        mock_access.assert_called_once_with("dummy_path", os.R_OK)
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")
        mock_toml_load.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("os.access", return_value=True)
    @patch("builtins.open",
           new_callable=mock_open,
           read_data='[files]\noutput_file = "test_output.json"')
    def test_load_config_success(self, mock_file_open, mock_access, mock_exists):
        '''Test load_config function with a valid TOML file.'''
        config = load_config("dummy_path")
        self.assertEqual(config, {"files": {"output_file": "test_output.json"}})
        mock_exists.assert_called_once_with("dummy_path")
        mock_access.assert_called_once_with("dummy_path", os.R_OK)
        mock_file_open.assert_called_once_with("dummy_path", "r", encoding="utf-8")


if __name__ == '__main__':
    unittest.main()
