import unittest
import tempfile
import os

import nanonispy as nap

class TestNanonisFileBaseClass(unittest.TestCase):
    """
    Testing class for NanonisFile base class.
    """
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_is_instance_nanonis_file(self):
        """
        Check for correct instance of NanonisFile object.
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b':HEADER_END:')
        f.close()
        NF = nap.read.NanonisFile(f.name)

        self.assertIsInstance(NF, nap.read.NanonisFile)


    def test_unsupported_filetype(self):
        """
        Handle unsupported file gracefully.
        """
        with self.assertRaises(nap.read.UnhandledFileError):
            f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.txt',
                                        dir=self.temp_dir.name,
                                        delete=False)
            f.close()
            NF = nap.read.NanonisFile(f.name)

    def test_3ds_suffix_parsed(self):
        """
        3ds file recognized.
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b':HEADER_END:')
        f.close()
        NF = nap.read.NanonisFile(f.name)
        self.assertEquals(NF.filetype, 'grid')

    def test_sxm_suffix_parsed(self):
        """
        Sxm file recognized.
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.sxm',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'SCANIT_END')
        f.close()
        NF = nap.read.NanonisFile(f.name)
        self.assertEquals(NF.filetype, 'scan')

    def test_dat_suffix_parsed(self):
        """
        Dat file recognized.
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.dat',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'[DATA]')
        f.close()
        NF = nap.read.NanonisFile(f.name)
        self.assertEquals(NF.filetype, 'spec')

    def test_find_start_byte(self):
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'header_entry\n:HEADER_END:\n')
        f.close()

        NF = nap.read.NanonisFile(f.name)
        byte_offset = NF.find_data_start_byte()

        self.assertEquals(byte_offset, 26)


if __name__ == '__main__':
    unittest.main()
