import numpy as np
import zarr
from zarr import MemoryStore

from src.source_helper import load_source


class CompressedSource:
    def __init__(self, uri, tile_size=256, compression='blosc', **compression_kwargs):
        self.uri = uri
        self.tile_size = tile_size
        self.compression = compression
        self.compression_kwargs = compression_kwargs
        self.data = []

    def init(self):
        self.data = []
        datas, dim_order = load_source(self.uri)
        print(f'Total data size {np.sum([np.prod(data.shape, dtype=np.int64) * data.itemsize for data in datas]):,}')

        compressor = None
        if self.compression:
            if 'xr' in self.compression.lower():
                from imagecodecs.numcodecs import Jpegxr    # Note: Jpegxr from imagecodecs-2024.9.22 spams performance messages
                zarr.register_codec(Jpegxr)
                compressor = zarr.get_codec({'id': Jpegxr.codec_id, **self.compression_kwargs})
                if 'c' in dim_order and not dim_order.endswith('c'):
                    # move channel axis to end for image compression
                    c_index = dim_order.index('c')
                    datas = [np.moveaxis(data, c_index, -1) for data in datas]
                    dim_order = dim_order[:c_index] + dim_order[c_index+1:] + 'c'
                    while dim_order[0] in 'zt' and datas[0].shape[0] == 1:
                        datas = [np.take(data, 0, axis=0) for data in datas]
                        dim_order = dim_order[1:]
            else:
                compressor = zarr.get_codec({'id': self.compression})

        self.dim_order = dim_order

        self.store = MemoryStore()
        dest_root = zarr.open(store=self.store, mode='a')
        self.root = dest_root

        for level, data in enumerate(datas):
            chunks = []
            for dim, size in zip(dim_order, data.shape):
                if size > self.tile_size:
                    chunk_size = self.tile_size
                elif dim in 'yxc':
                    chunk_size = size
                else:
                    chunk_size = 1
                chunks.append(chunk_size)

            dest_data = dest_root.create(name=str(level), shape=data.shape, chunks=chunks, dtype=data.dtype,
                                         compressor=compressor)
            #dest_data[:] = data
            data.to_zarr(dest_data)
            self.data.append(dest_data)
