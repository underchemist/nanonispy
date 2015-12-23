import os
import numpy as np

class NanonisFile:
    """
    Base class for Nanonis data files (grid, scan, point spectroscopy).
    """

    def __init__(self, fname):
        self.datadir, self.basename = os.path.split(fname)
        self.fname = fname
        self.filetype = self.determine_filetype()
        self.end_tags = dict(grid=':HEADER_END:',
                             scan='SCANIT_END',
                             spec='[DATA]')

        self.byte_offset = self.start_byte()
        self.header_raw = self.read_raw_header(self.byte_offset)

    def determine_filetype(self):
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

    def read_raw_header(self, byte_offset):
        """
        Return header as a raw string.

        Everything before the end tag is considered to be part of the header.
        the parsing will be done later by subclass methods.
        """
        with open(self.fname, 'rb') as f:
            return f.read(byte_offset).decode()

    def start_byte(self):
        """
        Find first byte after end tag signalling end of header info.

        Caveat, I believe this is the first byte after the end of the
        line that the end tag is found on, not strictly the first byte
        directly after the end tag is found.
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
    def __init__(self, fname):
        super().__init__(fname)
        self.header = _parse_3ds_header(self.header_raw)
        self.signals = self._load_data()

    def _load_data(self):
        # load grid params
        nx, ny = self.header['dim_px']
        num_sweep = self.header['num_sweep_signal']
        num_param = self.header['num_parameters']
        num_chan = self.header['num_channels']
        data_dict = dict()

        # open and seek to start of data
        f = open(self.fname, 'rb')
        f.seek(self.byte_offset)
        data_format = '>f4'
        griddata = np.fromfile(f, dtype=data_format)
        f.close()

        # pixel size in bytes
        exp_size_per_pix = num_param + num_sweep*num_chan

        # reshape from 1d to 3d
        griddata_shaped = griddata.reshape((nx, ny, exp_size_per_pix))

        # experimental parameters are first num_param of every pixel
        params = griddata_shaped[:, :, :num_param]
        data_dict['params'] = params

        # extract data for each channel
        for i, chann in enumerate(self.header['channels']):
            start_ind = num_param + i * num_sweep
            stop_ind = num_param + (i+1) * num_sweep
            data_dict[chann] = griddata_shaped[:, :, start_ind:stop_ind]

        return data_dict


class Scan(NanonisFile):
    pass

class Spec(NanonisFile):
    pass

class Signal:

    def __init__(self, name, data, unit):
        self.name = name
        self.data = data
        self.unit = unit

    def change_unit(self, fact, new_unit):
        """
        multiply data by conversion factor and update unit string.
        """
        self.data *= fact
        self.unit = new_unit


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

def _parse_3ds_header(header_raw):
    """
    Parse raw header string.

    Empirically done based on Nanonis header structure. Details can be seen in
    Nanonis help documentation.

    Parameters
    ----------
    header_raw : str
        Raw header string from read_raw_header() method.
    """
    # cleanup string and remove end tag as entry
    header_entries = header_raw.split('\r\n')
    header_entries = header_entries[:-2]

    header_dict = dict()

    # grid dimensions in pixels
    dim_px_str = _split_header_entry(header_entries[0])
    header_dict['dim_px'] = [int(val) for val in dim_px_str.split(' x ')]

    # grid frame center position, size, angle
    grid_str = _split_header_entry(header_entries[1], multiple=True)
    header_dict['pos_xy'] = [float(val) for val in grid_str[:2]]
    header_dict['size_xy'] = [float(val) for val in grid_str[2:4]]
    header_dict['angle'] = float(grid_str[-1])

    # sweep signal
    header_dict['sweep_signal'] = _split_header_entry(header_entries[2])

    # fixed parameters
    header_dict['fixed_parameters'] = _split_header_entry(header_entries[3], multiple=True)

    # experimental parameters
    header_dict['experimental_parameters'] = _split_header_entry(header_entries[4], multiple=True)

    # number of parameters (each 4 bytes)
    header_dict['num_parameters'] = int(_split_header_entry(header_entries[5]))

    # experiment size in bytes
    header_dict['experiment_size'] = int(_split_header_entry(header_entries[6]))

    # number of points of sweep signal
    header_dict['num_sweep_signal'] = int(_split_header_entry(header_entries[7]))

    # channel names
    header_dict['channels'] = _split_header_entry(header_entries[8], multiple=True)
    header_dict['num_channels'] = len(header_dict['channels'])

    # measure delay
    header_dict['measure_delay'] = float(_split_header_entry(header_entries[9]))

    # metadata
    header_dict['experiment_name'] = _split_header_entry(header_entries[10])
    header_dict['start_time'] = _split_header_entry(header_entries[11])
    header_dict['end_time'] = _split_header_entry(header_entries[12])
    header_dict['user'] = _split_header_entry(header_entries[13])
    header_dict['comment'] = _split_header_entry(header_entries[14])

    return header_dict


def _split_header_entry(entry, multiple=False):

        _, val_str = entry.split("=")

        if multiple:
            return val_str.strip('"').split(';')
        else:
            return val_str.strip('"')

