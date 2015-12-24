import unittest
import tempfile
import os
import numpy as np

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
        byte_offset = NF.start_byte()

        self.assertEquals(byte_offset, 26)

    def test_no_header_tag_found(self):
        with self.assertRaises(nap.read.FileHeaderNotFoundError):
            f = tempfile.NamedTemporaryFile(mode='wb',
                                            suffix='.3ds',
                                            dir=self.temp_dir.name,
                                            delete=False)
            f.close()
            NF = nap.read.NanonisFile(f.name)

    def test_header_raw_is_str(self):
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'header_entry\n:HEADER_END:\n')
        f.close()

        NF = nap.read.NanonisFile(f.name)
        self.assertIsInstance(NF.header_raw, str)


class TestGridFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_dummy_header(self):
        """
        return tempfile file object with dummy header info
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'Grid dim="230 x 230"\r\nGrid settings=4.026839E-8;-4.295725E-8;1.500000E-7;1.500000E-7;0.000000E+0\r\nSweep Signal="Bias (V)"\r\nFixed parameters="Sweep Start;Sweep End"\r\nExperiment parameters="X (m);Y (m);Z (m);Z offset (m);Settling time (s);Integration time (s);Z-Ctrl hold;Final Z (m)"\r\n# Parameters (4 byte)=10\r\nExperiment size (bytes)=2048\r\nPoints=512\r\nChannels="Input 3 (A)"\r\nDelay before measuring (s)=0.000000E+0\r\nExperiment="Grid Spectroscopy"\r\nStart time="21.10.2014 16:48:06"\r\nEnd time="23.10.2014 10:42:19"\r\nUser=\r\nComment=\r\n:HEADER_END:\r\n')
        f.close()

        return f

    def create_dummy_grid_data(self):
        """
        return tempfile file object with dummy header info
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.3ds',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b'Grid dim="230 x 230"\r\nGrid settings=4.026839E-8;-4.295725E-8;1.500000E-7;1.500000E-7;0.000000E+0\r\nSweep Signal="Bias (V)"\r\nFixed parameters="Sweep Start;Sweep End"\r\nExperiment parameters="X (m);Y (m);Z (m);Z offset (m);Settling time (s);Integration time (s);Z-Ctrl hold;Final Z (m)"\r\n# Parameters (4 byte)=10\r\nExperiment size (bytes)=2048\r\nPoints=512\r\nChannels="Input 3 (A)"\r\nDelay before measuring (s)=0.000000E+0\r\nExperiment="Grid Spectroscopy"\r\nStart time="21.10.2014 16:48:06"\r\nEnd time="23.10.2014 10:42:19"\r\nUser=\r\nComment=\r\n:HEADER_END:\r\n')
        a = np.linspace(0, 100.0, 230*230*(10+512))
        b = np.asarray(a, dtype='>f4')
        b.tofile(f)
        f.close()

        return f

    def test_is_instance_grid_file(self):
        """
        Check for correct instance of Grid object.
        """
        f = self.create_dummy_grid_data()
        GF = nap.read.Grid(f.name)

        self.assertIsInstance(GF, nap.read.Grid)

    def test_header_is_dict(self):
        f = self.create_dummy_grid_data()
        GF = nap.read.Grid(f.name)

        self.assertIsInstance(GF.header, dict)

    def test_data_has_right_shape(self):
        f = self.create_dummy_grid_data()
        GF = nap.read.Grid(f.name)

        self.assertEquals(GF.signals['Input 3 (A)'].shape, (230, 230, 512))

    def test_sweep_signal_calculated(self):
        f = self.create_dummy_grid_data()
        GF = nap.read.Grid(f.name)

        self.assertEquals(GF.signals['sweep_signal'].shape, (512,))


class TestScanFile(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_dummy_scan_data(self):
        """
        return tempfile file object with dummy header info
        """
        f = tempfile.NamedTemporaryFile(mode='wb',
                                        suffix='.sxm',
                                        dir=self.temp_dir.name,
                                        delete=False)
        f.write(b':NANONIS_VERSION:\n2\n:SCANIT_TYPE:\n              FLOAT            MSBFIRST\n:REC_DATE:\n 21.11.2014\n:REC_TIME:\n17:19:32\n:REC_TEMP:\n      290.0000000000\n:ACQ_TIME:\n       470.3\n:SCAN_PIXELS:\n       64       64\n:SCAN_FILE:\nC:\\STM data\\2014-11\\2014-11-21\\ScanAg111_November2014_001.sxm\n:SCAN_TIME:\n             3.533E+0             3.533E+0\n:SCAN_RANGE:\n           1.500000E-7           1.500000E-7\n:SCAN_OFFSET:\n             7.217670E-8         2.414175E-7\n:SCAN_ANGLE:\n            0.000E+0\n:SCAN_DIR:\nup\n:BIAS:\n            -5.000E-2\n:Z-CONTROLLER:\n\tName\ton\tSetpoint\tP-gain\tI-gain\tT-const\n\tCurrent #3\t1\t1.000E-10 A\t7.000E-12 m\t3.500E-9 m/s\t2.000E-3 s\n:COMMENT:\n\n:NanonisMain>Session Path:\nC:\\STM data\\2014-11\\2014-11-21\n:NanonisMain>SW Version:\nGeneric 4\n:NanonisMain>UI Release:\n3180\n:NanonisMain>RT Release:\n3130\n:NanonisMain>RT Frequency (Hz):\n5E+3\n:NanonisMain>Signals Oversampling:\n10\n:NanonisMain>Animations Period (s):\n20E-3\n:NanonisMain>Indicators Period (s):\n300E-3\n:NanonisMain>Measurements Period (s):\n500E-3\n:DATA_INFO:\n\tChannel\tName\tUnit\tDirection\tCalibration\tOffset\n\t14\tZ\tm\tboth\t-3.480E-9\t0.000E+0\n\t2\tInput_3\tA\tboth\t1.000E-9\t0.000E+0\n\t20\tLIX_1_omega\tA\tboth\t1.000E+0\t0.000E+0\n\t21\tLIY_1_omega\tA\tboth\t1.000E+0\t0.000E+0\n\n:SCANIT_END:\n')
        a = np.linspace(0, 100.0, 1+4*2*64*64)
        b = np.asarray(a, dtype='>f4')
        b.tofile(f)
        f.close()

        return f

    def test_header_is_dict(self):
        f = self.create_dummy_scan_data()
        SF = nap.read.Scan(f.name)

        self.assertIsInstance(SF.header, dict)

if __name__ == '__main__':
    unittest.main()
