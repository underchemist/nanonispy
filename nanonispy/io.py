from abc import ABC, abstractmethod
from functools import partial
from pathlib import Path
from dataclasses import dataclass
import numpy as np

from nanonispy.constants import end_tags, suffix_map
from nanonispy.formats import clean_metadata, metadata_to_dtypes, pop_op


def get_header_tag_for_filetype(reader):
    suffix = reader.path.suffix
    return end_tags[suffix_map[suffix]]


def get_filetype(reader):
    return suffix_map[reader.path.suffix]


class NanonisBinaryReader(ABC):
    def __init__(self, path, mode="rb", dtype=">f4", extra_metadata=None):
        if isinstance(path, str):
            path = Path(path)
        if mode not in ("rb", "r"):
            raise TypeError(f"valid mode is rb or r, not {mode}")

        self.path = path
        self.mode = mode
        self.dtype = dtype
        self.extra_metadata = extra_metadata
        self.fp = path.open(mode=self.mode)
        self.closed = self.fp.closed

        self._filetype = get_filetype(self)
        self._end_tag = get_header_tag_for_filetype(self)

    def _byte_offset(self, end_tag=None, append=0):
        if not end_tag:
            end_tag = self._end_tag
        end_tag = end_tag.encode()

        byte_offset = -1
        self.fp.seek(0)
        for chunk in self.fp:
            if end_tag in chunk:
                byte_offset = self.fp.tell()
                break

        if byte_offset == -1:
            raise ValueError

        return byte_offset + append

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def _parse(self):
        pass

    def close(self):
        if not self.closed:
            self.fp.close()
            self.closed = self.fp.closed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self):
        return "<{} {} name='{}' mode='{}'>".format(
            self.closed and "closed" or "open",
            self.__class__.__name__,
            self.path.name,
            self.mode,
        )


class NanonisGrid(NanonisBinaryReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._offset = self._byte_offset()
        self._parse()
        self.params, self.data = self.read()

    def read(self):
        nx, ny = self.metadata["Grid dim"]
        num_sweep = self.metadata["Points"]
        num_params = self.metadata["# Parameters (4 byte)"]
        num_chan = len(self.metadata["Channels"])

        self.fp.seek(self._offset)
        data = np.fromfile(self.fp, dtype=self.dtype)

        exp_size_per_pix_per_chan = num_params + num_sweep * num_chan
        data = data.reshape((nx, ny, exp_size_per_pix_per_chan, num_chan))
        data = np.moveaxis(data, -1, 0)
        params = data[:, :, :, :num_params]
        data = data[:, :, :, num_params:]
        return params, data

    def _parse(self):
        self.fp.seek(0)
        offset = self._offset - len(self._end_tag)  # exclude end tag from read
        raw = self.fp.read(offset)
        metadata = clean_metadata(raw)
        for key, f in metadata_to_dtypes[self._filetype].items():
            metadata[key] = f(metadata[key])
        leftovers = set(metadata.keys()) - set(
            metadata_to_dtypes[self._filetype].keys()
        )
        for key in leftovers:
            if self.extra_metadata:
                val = metadata[key]
                try:
                    f = self.extra_metadata[key]
                    metadata[key] = f(val)
                except KeyError:
                    pass
            metadata[key] = pop_op(metadata[key])

        self.metadata = metadata


class NanonisScan(NanonisBinaryReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._offset = self._byte_offset(append=2)

    def read(self):
        pass

    def _parse(self):
        pass


class NanonisSpec:
    def __init__self(self):
        raise NotImplementedError
