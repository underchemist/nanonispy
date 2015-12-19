import os

class NanonisFile:
    """
    Base class for Nanonis data files (grid, scan, point spectroscopy).
    """

    def __init__(self, fname):
        self.datadir, self.fname = os.path.split(fname)
        self.filetype = self._determine_filetype()

    def _determine_filetype(self):
        if self.fname[-3:] not in ('3ds', 'sxm', 'dat'):
            raise UnhandledFileError('{} is not a supported filetype or does not exist'.format(self.fname))
        else:
            return self.fname[-3:]

class UnhandledFileError(Exception):
    """
    To be raised when unknown file extension is passed.
    """
    pass
