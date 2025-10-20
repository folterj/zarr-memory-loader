import numpy as np
import zarr
from zarr import MemoryStore

from src.source_helper import load_source


class CompressedSource:
    def __init__(self, uri, tile_size=256, compression='jpegxr'):
        self.uri = uri
        self.tile_size = tile_size
        self.compression = compression

    def init(self, level=0):
        data, dim_order = load_source(self.uri, level)

        compressor = None
        if self.compression:
            if 'xr' in self.compression.lower():
                from imagecodecs.numcodecs import Jpegxr    # Note: Jpegxr from imagecodecs-2024.9.22 spams performance messages
                zarr.register_codec(Jpegxr)
                compressor = zarr.get_codec({'id': Jpegxr.codec_id, 'level': 75})    # , 'level': 5
                if 'c' in dim_order and not dim_order.endswith('c'):
                    # move channel axis to end for image compression
                    c_index = dim_order.index('c')
                    data = np.moveaxis(data, c_index, -1)
                    dim_order = dim_order[:c_index] + dim_order[c_index+1:] + 'c'
                    while dim_order[0] in 'zt' and data.shape[0] == 1:
                        data = np.take(data, 0, axis=0)
                        dim_order = dim_order[1:]
            else:
                compressor = zarr.get_codec({'id': self.compression})

        chunks = []
        for dim, size in zip(dim_order, data.shape):
            if size > self.tile_size:
                chunk_size = self.tile_size
            elif dim in 'yxc':
                chunk_size = size
            else:
                chunk_size = 1
            chunks.append(chunk_size)

        self.store = MemoryStore()
        dest_root = zarr.open(store=self.store, mode='a')
        dest_data = dest_root.create(name=str(level), shape=data.shape, chunks=chunks, dtype=data.dtype,
                                     compressor=compressor)
        dest_data[:] = data
