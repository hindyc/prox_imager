'''Test cases for the lazy_ic_import function in fetch_ubuntu_images.py.'''
import unittest
from prox_imager.fetch_ubuntu_images import lazy_ic_import


class TestLazyIcImport(unittest.TestCase):
    '''Test cases for the lazy_ic_import function.'''

    def test_lazy_ic_import(self):
        '''Test lazy_ic_import function to ensure icecream is imported and configured correctly.'''
        ic = lazy_ic_import()
        self.assertTrue(callable(ic), "The returned object should be callable.")
        ic("Test message")  # This should print a message if icecream is correctly imported and configured

    def test_lazy_ic_import_called_once(self):
        '''Test lazy_ic_import function to ensure icecream is imported only once.'''
        ic1 = lazy_ic_import()
        ic2 = lazy_ic_import()
        self.assertIs(ic1, ic2, "The same ic instance should be returned on subsequent calls.")


if __name__ == '__main__':
    unittest.main()
