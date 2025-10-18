import numpy as np
from ome_zarr.io import parse_url
import zarr
from zarr import MemoryStore, copy_store


class ZarrMemorySource:
    def __init__(self, uri):
        self.uri = uri
        self.store = None

    def load(self):
        self.store = MemoryStore()
        file_store = parse_url(self.uri).store
        copy_store(file_store, self.store)  # not yet implemented in zarr v3
        file_store.close()

    def load_and_compress(self, compression='blosc', swap_axes=False):
        if compression and 'xr' in compression.lower():
            from imagecodecs.numcodecs import Jpegxr    # Note: Jpegxr from imagecodecs-2024.9.22 spams performance messages
            zarr.register_codec(Jpegxr)
            compressor = zarr.get_codec({'id': Jpegxr.codec_id, 'level': 75})    # , 'level': 5
        else:
            compressor = zarr.get_codec({'id': compression})

        self.store = MemoryStore()
        store = parse_url(self.uri).store
        root = zarr.open(store=store, mode='r')
        dest_root = zarr.open(store=self.store, mode='a')
        for group_key, node in root.items():
            dest_group = dest_root.create_group(name=group_key)
            for array_key, data in node.items():
                if swap_axes:
                    shape = (data.shape[-2], data.shape[-1], data.shape[1])
                    chunks = (256, 256, data.shape[1])
                else:
                    shape = data.shape
                    chunks = (1, data.shape[1], 1, 256, 256)
                dest_data = dest_group.create(name=array_key, shape=shape, chunks=chunks,
                                               dtype=data.dtype, compressor=compressor)
                if swap_axes:
                    data2 = np.moveaxis(data[:].squeeze(), 0, -1)
                else:
                    data2 = data
                dest_data[:] = data2

    def get_root(self):
        if self.store is None:
            # if not loaded into memory, revert to normal file store
            self.store = parse_url(self.uri).store
        root = zarr.open(store=self.store, mode='r')
        return root
