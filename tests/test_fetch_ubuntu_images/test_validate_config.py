'''Test cases for the validate_config function in fetch_ubuntu_images.py.'''
import unittest
from prox_imager.fetch_ubuntu_images import validate_config


class TestValidateConfig(unittest.TestCase):
    '''Test cases for the validate_config function.'''

    def test_all_sections_present(self):
        '''Test validate_config function with a config containing all sections.'''
        config = {
            'urls': {},
            'files': {},
        }
        self.assertTrue(validate_config(config))

    def test_some_sections_missing(self):
        '''Test validate_config function with a config missing some sections.'''
        config = {
            'urls': {},
        }
        self.assertFalse(validate_config(config))

    def test_no_sections_present(self):
        '''Test validate_config function with an empty config.'''
        config = {}
        self.assertFalse(validate_config(config))


if __name__ == '__main__':
    unittest.main()
