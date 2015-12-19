import unittest
import tempfile

import nanonispy as nap

class TestNanonisFileBaseClass(unittest.TestCase):
    """
    Testing class for NanonisFile base class.
    """

    def test_is_instance_nanonis_file(self):
        """
        Check for correct instance of NanonisFile object.
        """
        with tempfile.NamedTemporaryFile(suffix='.3ds') as f:
            NF = nap.read.NanonisFile(f.name)
        self.assertIsInstance(NF, nap.read.NanonisFile)

    def test_unsupported_filetype(self):
        """
        Handle unsupported file gracefully.
        """
        with self.assertRaises(nap.read.UnhandledFileError):
            with tempfile.NamedTemporaryFile(suffix='.txt') as f:
                NF = nap.read.NanonisFile(f.name)

    def test_3ds_suffix_parsed(self):
        """
        3ds file recognized.
        """
        with tempfile.NamedTemporaryFile(suffix='.3ds') as f:
            NF = nap.read.NanonisFile(f.name)
            self.assertEquals(NF.filetype, '3ds')

    def test_sxm_suffix_parsed(self):
        """
        Sxm file recognized.
        """
        with tempfile.NamedTemporaryFile(suffix='.sxm') as f:
            NF = nap.read.NanonisFile(f.name)
            self.assertEquals(NF.filetype, 'sxm')

    def test_dat_suffix_parsed(self):
        """
        Dat file recognized.
        """
        with tempfile.NamedTemporaryFile(suffix='.dat') as f:
            NF = nap.read.NanonisFile(f.name)
            self.assertEquals(NF.filetype, 'dat')

    def test_header_found(self):
        with tempfile.NamedTemporaryFile(suffix='.3ds') as f:
            f.write(r'header_entry\nend_tag\n')
            f.seek(0)
            NF = nap.read.NanonisFile(f.name)
            self.assertEquals(NF.header, 'header_entry')



if __name__ == '__main__':
    unittest.main()
