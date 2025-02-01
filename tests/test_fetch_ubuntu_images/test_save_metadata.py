'''Test cases for the fetch_ubuntu_images module.'''
import unittest
from unittest.mock import patch, mock_open
from prox_imager.fetch_ubuntu_images import save_metadata


class TestSaveMetadata(unittest.TestCase):
    '''Test cases for the save_metadata function.'''
    @patch("builtins.open", new_callable=mock_open)
    def test_save_metadata_success(self, mock_file_open):
        '''Test save_metadata function with valid metadata.'''
        metadata = {"key": "value"}
        mock_file = mock_file_open.return_value
        with self.assertLogs('prox_imager.fetch_ubuntu_images', level='INFO') as log:
            save_metadata(metadata, "dummy_output.json")
            log_match = "INFO:prox_imager.fetch_ubuntu_images:✅ Saved metadata to dummy_output.json"
            self.assertIn(log_match, log.output)
        mock_file_open.assert_called_once_with("dummy_output.json", "w", encoding="utf-8")
        mock_file.write.assert_any_call('{')
        mock_file.write.assert_any_call('"key"')
        mock_file.write.assert_any_call(': ')
        mock_file.write.assert_any_call('"value"')
        mock_file.write.assert_any_call('}')

    @patch("builtins.open", side_effect=IOError("Error"))
    def test_save_metadata_io_error(self, mock_file_open):
        '''Test save_metadata function with an IOError.'''
        metadata = {"key": "value"}
        with self.assertLogs('prox_imager.fetch_ubuntu_images', level='ERROR') as log:
            save_metadata(metadata, "dummy_output.json")
            log_match = ("ERROR:prox_imager.fetch_ubuntu_images:"
                         "❌ Failed to save metadata to dummy_output.json - Unknown: Unknown error")
            self.assertIn(log_match, log.output)
        mock_file_open.assert_called_once_with("dummy_output.json", "w", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump", side_effect=TypeError("Error"))
    def test_save_metadata_type_error(self, mock_json_dump, mock_file_open):
        '''Test save_metadata function with a TypeError during JSON serialization.'''
        metadata = {"key": "value"}
        with self.assertLogs('prox_imager.fetch_ubuntu_images', level='ERROR') as log:
            save_metadata(metadata, "dummy_output.json")
            log_match = ("ERROR:prox_imager.fetch_ubuntu_images:"
                         "❌ Failed to serialize metadata to JSON: Error")
            self.assertIn(log_match, log.output)
        mock_file_open.assert_called_once_with("dummy_output.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(metadata, mock_file_open(), indent=4)

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_save_metadata_permission_error(self, mock_file_open):
        '''Test save_metadata function with a PermissionError.'''
        metadata = {"key": "value"}
        with self.assertLogs('prox_imager.fetch_ubuntu_images', level='ERROR') as log:
            save_metadata(metadata, "dummy_output.json")
            log_match = ("ERROR:prox_imager.fetch_ubuntu_images:"
                         "❌ Permission denied when trying to save metadata to dummy_output.json")
            self.assertIn(log_match, log.output)
        mock_file_open.assert_called_once_with("dummy_output.json", "w", encoding="utf-8")


if __name__ == '__main__':
    unittest.main()
