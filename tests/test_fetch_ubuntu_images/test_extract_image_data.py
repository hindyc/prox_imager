'''Test cases for the extract_image_data function in fetch_ubuntu_images module.'''
import unittest
from prox_imager.fetch_ubuntu_images import extract_image_data


class TestExtractImageData(unittest.TestCase):
    '''Test cases for the extract_image_data function.'''
    def test_extract_image_data_success(self):
        '''Test extract_image_data function with valid metadata.'''
        metadata = {
            "products": {
                "product1": {
                    "release": "20.04",
                    "arch": "amd64",
                    "version": "20201026",
                    "url": "http://example.com/image.img",
                    "sha256": "http://example.com/image.img.sha256"
                }
            }
        }
        expected_output = {
            "product1": {
                "release": "20.04",
                "arch": "amd64",
                "version": "20201026",
                "image_url": "http://example.com/image.img",
                "sha256_url": "http://example.com/image.img.sha256"
            }
        }
        self.assertEqual(extract_image_data(metadata), expected_output)

    def test_extract_image_data_missing_fields(self):
        '''Test extract_image_data function with metadata missing some fields.'''
        metadata = {
            "products": {
                "product1": {
                    "release": "20.04",
                    "arch": "amd64",
                    "version": "20201026",
                    "url": "http://example.com/image.img"
                }
            }
        }
        expected_output = {}
        self.assertEqual(extract_image_data(metadata), expected_output)

    def test_extract_image_data_empty_metadata(self):
        '''Test extract_image_data function with empty metadata.'''
        metadata = {}
        expected_output = {}
        self.assertEqual(extract_image_data(metadata), expected_output)

    def test_extract_image_data_no_products(self):
        '''Test extract_image_data function with metadata having no products.'''
        metadata = {"products": {}}
        expected_output = {}
        self.assertEqual(extract_image_data(metadata), expected_output)

    def test_extract_image_data_unknown_fields(self):
        '''Test extract_image_data function with metadata having unknown fields.'''
        metadata = {
            "products": {
                "product1": {
                    "unknown_field": "unknown_value",
                    "url": "http://example.com/image.img",
                    "sha256": "http://example.com/image.img.sha256"
                }
            }
        }
        expected_output = {
            "product1": {
                "release": "unknown",
                "arch": "unknown",
                "version": "unknown",
                "image_url": "http://example.com/image.img",
                "sha256_url": "http://example.com/image.img.sha256"
            }
        }
        self.assertEqual(extract_image_data(metadata), expected_output)


if __name__ == '__main__':
    unittest.main()
