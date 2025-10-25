import numpy as np
import os
import psutil
import time
import timeit

from src.CompressedSource import CompressedSource
from src.ZarrMemorySource import ZarrMemorySource


def read_memory_source(filename):
    process = psutil.Process(os.getpid())

    used_mem_start = process.memory_info().rss

    start_time = time.time()
    source = ZarrMemorySource(filename)
    #source.load()
    source.load_and_compress(compression='jpegxr', compression_level=75, swap_axes=True)
    dtime = time.time() - start_time
    print(f'init time {dtime:.1f} s')
    used_mem_start2 = process.memory_info().rss
    print(f'used mem {used_mem_start2 - used_mem_start:,}')

    root = source.get_root()
    print(root.info)
    total_size = 0
    for key, node in root.items():
        print('node', key)
        for data in node.values():
            print('shape', data.shape)
            size = np.prod(data.shape, dtype=np.int64) * data.itemsize
            print('size', size)
            a = np.array(data[..., 0, 0, 0])
            total_size += size
    print(f'total size {total_size:,}')
    used_mem_start3 = process.memory_info().rss
    print(f'used mem {used_mem_start3 - used_mem_start:,}')

    node = root[list(root.keys())[-1]]
    data = node[0]
    shape = data.shape
    tile_size = 256
    n = 1000
    print('random read tile size', tile_size, 'in shape', shape)
    dimy, dimx = None, None
    for i0 in range(len(shape), 0, -1):
        i = i0 - 1
        if shape[i] > 4:
            if dimx is None:
                dimx = i
            elif dimy is None:
                dimy = i

    print(f'time / read {timeit.timeit(lambda: random_read(data, dimx, dimy, tile_size), number=n) / n:.6f} s')
    used_mem_start4 = process.memory_info().rss
    print(f'used mem+ {used_mem_start4 - used_mem_start3:,}')


def read_compressed_source(filename):
    process = psutil.Process(os.getpid())

    used_mem_start = process.memory_info().rss

    start_time = time.time()

    source = CompressedSource(filename, compression='jpegxr', level=75)
    source.init()

    dtime = time.time() - start_time
    print(f'init time {dtime:.1f} s')
    used_mem_start2 = process.memory_info().rss
    print(f'used mem {used_mem_start2 - used_mem_start:,}')

    data = source.data[0]
    shape = data.shape
    tile_size = 256
    n = 1000
    print('random read tile size', tile_size, 'in shape', shape)
    dimy, dimx = None, None
    for i0 in range(len(shape), 0, -1):
        i = i0 - 1
        if shape[i] > 4:
            if dimx is None:
                dimx = i
            elif dimy is None:
                dimy = i

    print(f'time / read {timeit.timeit(lambda: random_read(data, dimx, dimy, tile_size), number=n) / n:.6f} s')
    used_mem_start3 = process.memory_info().rss
    print(f'used mem+ {used_mem_start3 - used_mem_start2:,}')



def random_read(data, dimx, dimy, tile_size=256):
    y = np.random.randint(data.shape[dimy] / tile_size) * tile_size
    x = np.random.randint(data.shape[dimx] / tile_size) * tile_size
    if dimx > 0:    # assume c axis at end
        a = np.array(data[..., y:y + tile_size, x:x + tile_size, :])
    else:
        a = np.array(data[..., y:y + tile_size, x:x + tile_size])


if __name__ == '__main__':
    #filename = 'D:/slides/9838562/9838562.zarr'
    filename = 'E:/Personal/Crick/slides/tracerx/K021_PR001.ome.tiff'   # large
    #filename = 'E:/Personal/Crick/slides/tracerx/K130_PR003.ome.tiff'   # small
    #read_memory_source(filename)
    read_compressed_source(filename)
