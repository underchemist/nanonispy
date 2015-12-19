__author__ = 'Yann-Sebastien'

import unittest
import os

import nanonispy as nap

class TestNanonisFileBaseClass(unittest.TestCase):
    def setUp(self, ext='3ds'):
        self.test_filename = 'tests_nanonis_file.' + ext
        f = open(self.test_filename, 'w')
        f.close()

    def tearDown(self):
        os.remove(self.test_filename)

    def test_is_instance_nanonis_file(self):
        self.NF = nap.read.NanonisFile(self.test_filename)
        self.assertIsInstance(self.NF, nap.read.NanonisFile)

    def test_unsupported_filetype(self):
        exception = nap.read.UnhandledFileError
        with self.assertRaises(exception):
            self.NF = nap.read.NanonisFile('not_a_file.txt')


if __name__ == '__main__':
    unittest.main()
