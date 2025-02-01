'''Test cases for the extract_image_data function in fetch_ubuntu_images module.'''
import unittest
import json
from pathlib import Path
from prox_imager.fetch_ubuntu_images import extract_image_data


class TestExtractImageData(unittest.TestCase):
    '''Test cases for the extract_image_data function.'''

    @classmethod
    def setUpClass(cls):
        '''Load metadata from JSON file.'''
        metadata_file = Path(__file__).parent / "metadata_extract_image_data.json"
        with open(metadata_file, "r", encoding="utf-8") as f:
            cls.metadata = json.load(f)

    def test_extract_image_data_success(self):
        '''Test extract_image_data function with valid metadata.'''
        metadata = self.metadata["valid_metadata"]
        base_url = "https://cloud-images.ubuntu.com"
        expected_output = {
            "com.ubuntu.cloud.daily:minimal:16.04:amd64": {
                "release": "xenial",
                "version": "16.04",
                "build_date": "20210929",
                "image_url": (
                    "https://cloud-images.ubuntu.com/minimal/daily/xenial/20210929/"
                    "xenial-minimal-cloudimg-amd64-disk1.img"
                ),
                "sha256": (
                    "7658ec30373e7ad1a1858744f395a89713d333721d7d1986ee8b71680b81a0a9"
                )
            }
        }
        self.assertEqual(extract_image_data(metadata, base_url), expected_output)

    def test_extract_image_data_missing_fields(self):
        '''Test extract_image_data function with metadata missing some fields.'''
        metadata = self.metadata["missing_fields_metadata"]
        base_url = "http://example.com"
        expected_output = {}
        self.assertEqual(extract_image_data(metadata, base_url), expected_output)

    def test_extract_image_data_empty_metadata(self):
        '''Test extract_image_data function with empty metadata.'''
        metadata = self.metadata["empty_metadata"]
        base_url = "http://example.com"
        expected_output = {}
        self.assertEqual(extract_image_data(metadata, base_url), expected_output)

    def test_extract_image_data_no_products(self):
        '''Test extract_image_data function with metadata having no products.'''
        metadata = self.metadata["no_products_metadata"]
        base_url = "http://example.com"
        expected_output = {}
        self.assertEqual(extract_image_data(metadata, base_url), expected_output)

    def test_extract_image_data_unknown_fields(self):
        '''Test extract_image_data function with metadata having unknown fields.'''
        metadata = self.metadata["unknown_fields_metadata"]
        base_url = "http://example.com"
        expected_output = {
            "product1": {
                "release": "unknown",
                "version": "unknown",
                "build_date": "unknown",
                "image_url": "http://example.com/unknown/path.img",
                "sha256": "unknown"
            }
        }
        self.assertEqual(extract_image_data(metadata, base_url), expected_output)


if __name__ == '__main__':
    unittest.main()
