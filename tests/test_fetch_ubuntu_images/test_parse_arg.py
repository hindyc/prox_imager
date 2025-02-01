'''Test cases for the fetch_ubuntu_images module.'''
import unittest
from unittest.mock import patch

import argparse

from prox_imager.fetch_ubuntu_images import parse_args


class TestParseArgs(unittest.TestCase):
    '''Test cases for the fetch_ubuntu_images module.'''
    def setUp(self):
        # Setup code to run before each test
        pass

    def tearDown(self):
        # Cleanup code to run after each test
        pass

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(config="./etc/config.toml"))
    def test_parse_args_default(self, mock_parse_args):
        '''Test parse_args function with default arguments.'''
        args = parse_args()
        self.assertEqual(args.config, "./etc/config.toml")
        mock_parse_args.assert_called_once()

    @patch("argparse.ArgumentParser.parse_args",
           return_value=argparse.Namespace(config="/custom/path/config.toml"))
    def test_parse_args_custom(self, mock_parse_args):
        '''Test parse_args function with custom arguments.'''
        args = parse_args()
        self.assertEqual(args.config, "/custom/path/config.toml")
        mock_parse_args.assert_called_once()


if __name__ == '__main__':
    unittest.main()
