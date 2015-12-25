import os
import re
import numpy as np

_end_tags = dict(grid=':HEADER_END:', scan='SCANIT_END', spec='[DATA]')

class NanonisFile:
    """
    Base class for Nanonis data files (grid, scan, point spectroscopy).
    """

    def __init__(self, fname):
        self.datadir, self.basename = os.path.split(fname)
        self.fname = fname
        self.filetype = self.determine_filetype()
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
            tag = _end_tags[self.filetype]

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
        self.signals['sweep_signal'] = self._derive_sweep_signal()
        self.signals['topo'] = self._extract_topo()

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

    def _derive_sweep_signal(self):
        name = self.header['sweep_signal']
        # find sweep signal start and end from a given pixel value
        sweep_start, sweep_end = self.signals['params'][0, 0, :2]
        num_sweep_signal = self.header['num_sweep_signal']

        return np.linspace(sweep_start, sweep_end, num_sweep_signal, dtype=np.float32)

    def _extract_topo(self):
        return self.signals['params'][:, :, 4]


class Scan(NanonisFile):

    def __init__(self, fname):
        super().__init__(fname)
        self.header = _parse_sxm_header(self.header_raw)

        # data begins with 4 byte code, add 4 bytes to offset instead
        self.byte_offset += 4

        # load data
        self.signals = self._load_data()

    def _load_data(self):
        channs = list(self.header['data_info']['Name'])
        nchanns = len(channs)
        nx, ny = self.header['scan_pixels']

        # assume both directions for now
        ndir = 2

        data_dict = dict()

        # open and seek to start of data
        f = open(self.fname, 'rb')
        f.seek(self.byte_offset)
        data_format = '>f4'
        scandata = np.fromfile(f, dtype=data_format)
        f.close()

        # reshape
        scandata_shaped = scandata.reshape(nchanns, ndir, nx, ny)

        # extract data for each channel
        for i, chann in enumerate(channs):
            chann_dict = dict(forward=scandata_shaped[i, 0, :, :],
                              backward=scandata_shaped[i, 1, :, :])
            data_dict[chann] = chann_dict

        return data_dict


class Spec(NanonisFile):
    def __init__(self, fname):
        super().__init__(fname)
        self.header = _parse_dat_header(self.header_raw)

    def _load_data(self):
        # done differently since data is ascii, not binary
        f = open(self.fname, 'r')
        f.seek(self.byte_offset)
        data_dict = dict()

        column_names = f.readline().strip('\n').split('\t')
        f.close()
        header_lines = len(self.header) + 4
        specdata = np.genfromtxt(self.fname, delimiter='\t', skip_header=header_lines)

        for i, name in enumerate(column_names):
            data_dict[name] = specdata[:, i]

        return data_dict


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

def _parse_sxm_header(header_raw):
    """
    Parse raw header string.

    Empirically done based on Nanonis header structure. Details can be seen in
    Nanonis help documentation.

    Parameters
    ----------
    header_raw : str
        Raw header string from read_raw_header() method.
    """
    header_entries = header_raw.split('\n')
    header_entries = header_entries[:-3]

    header_dict = dict()
    entries_to_be_split = ['scan_offset',
                           'scan_pixels',
                           'scan_range',
                           'scan_time']

    entries_to_be_floated = ['acq_time',
                             'bias',
                             *entries_to_be_split]

    for i, entry in enumerate(header_entries):
        if entry == ':DATA_INFO:' or entry == ':Z-CONTROLLER:':
            count = 1
            for j in range(i+1, len(header_entries)):
                if header_entries[j].startswith(':'):
                    break
                if header_entries[j][0] == '\t':
                    count += 1
            header_dict[entry.strip(':').lower()] = _parse_scan_header_table(header_entries[i+1:i+count])
            continue
        if entry.startswith(':'):
            header_dict[entry.strip(':').lower()] = header_entries[i+1].strip()

    for key in entries_to_be_split:
        header_dict[key] = header_dict[key].split()

    for key in entries_to_be_floated:
        if isinstance(header_dict[key], list):
            header_dict[key] = np.asarray(header_dict[key], dtype=np.float)
        else:
            header_dict[key] = np.float(header_dict[key])

    return header_dict


def _parse_dat_header(header_raw):
    header_entries = header_raw.split('\r\n')
    header_entries = header_entries[:-3]
    header_dict = dict()
    for entry in header_entries:
        key, val, _ = entry.split('\t')
        header_dict[key] = val

    return header_dict

def _split_header_entry(entry, multiple=False):

        _, val_str = entry.split("=")

        if multiple:
            return val_str.strip('"').split(';')
        else:
            return val_str.strip('"')


def _parse_scan_header_table(table_list):
    table_processed = []
    for row in table_list:
        # strip leading \t, split by \t
        table_processed.append(row.strip('\t').split('\t'))

    # column names are first row
    keys = table_processed[0]
    values = table_processed[1:]

    zip_vals = zip(*values)

    return dict(zip(keys, zip_vals))
