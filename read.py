import os

class NanonisFile:
    """
    Base class for Nanonis data files (grid, scan, point spectroscopy).
    """

    def __init__(self, fname):
        self.datadir, self.basename = os.path.split(fname)
        self.fname = fname
        self.filetype = self._determine_filetype()
        self.end_tags = dict(grid=':HEADER_END:',
                             scan='SCANIT_END',
                             spec='[DATA]')

        self.byte_offset = self.find_data_start_byte()
        self.header_raw = self.gen_raw_header(self.byte_offset)

    def _determine_filetype(self):
        """
        Check last three characters for appropriate file extension,
        raise error if not.
        """

        if self.fname[-3:] == '3ds':
            return 'grid'
        elif self.fname[-3:] == 'sxm':
            return 'scan'
        elif self.fname[-3:] == 'dat':
            return 'spec'
        else:
            raise UnhandledFileError('{} is not a supported filetype or does not exist'.format(self.basename))

    def gen_raw_header(self, byte_offset):
        """
        Return header as a raw string. Everything before
        the end tag is considered to be part of the header.
        the parsing will be done by each subclass of file.
        """
        with open(self.fname, 'rb') as f:
            return f.read(byte_offset)

    def find_data_start_byte(self):
        """
        Find first byte after end tag signalling end of header info.
        """
        with open(self.fname, 'rb') as f:
            tag = self.end_tags[self.filetype]

            # Set to a default value to know if end_tag wasn't found
            byte_offset = -1

            for line in f:
                # Convert from bytes to str
                entry = line.strip().decode()
                if tag in entry:
                    byte_offset = f.tell()
                    break

            if byte_offset == -1:
                raise FileHeaderNotFoundError(
                        'Could not find the {} end tag in {}'.format(tag, self.basename)
                        )

        return byte_offset

class Grid(NanonisFile):
    pass

class Scan(NanonisFile):
    pass

class Spec(NanonisFile):
    pass

class Signal:
    pass


class UnhandledFileError(Exception):
    """
    To be raised when unknown file extension is passed.
    """
    pass

class FileHeaderNotFoundError(Exception):
    """
    To be raised when no header information could be determined.
    """
    pass
