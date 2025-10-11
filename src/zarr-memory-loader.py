import numpy as np
import os
import psutil
import timeit

from src.ZarrMemorySource import ZarrMemorySource


if __name__ == '__main__':
    filename = 'D:/slides/9838562/9838562.zarr'

    process = psutil.Process(os.getpid())

    used_mem_start = process.memory_info().rss

    source = ZarrMemorySource(filename)
    source.load()
    used_mem_start2 = process.memory_info().rss
    print(f'used mem {used_mem_start2 - used_mem_start:_}')

    root = source.get_root()
    print(root.info)
    total_size = 0
    for key, node in root.items():
        print('node', key)
        for data in node.values():
            print('shape', data.shape)
            size = np.prod(data.shape) * data.itemsize
            print('size', size)
            a = data[0][0][0][0][0]   # access data
            total_size += size
    print(f'total size {total_size:_}')
    used_mem_start3 = process.memory_info().rss
    print(f'used mem {used_mem_start3 - used_mem_start:_}')

    node = root[list(root.keys())[-1]]
    data = node[0]
    shape = data.shape
    tile_size = 256
    print('random read tile size', tile_size, 'in shape', shape)

    def random_read():
        y = np.random.randint(shape[-2] - tile_size)
        x = np.random.randint(shape[-1] - tile_size)
        a = data[0][0][0][y:y+tile_size][x:x+tile_size]   # access data

    print('time', timeit.timeit(lambda: random_read(), number=100))
    used_mem_start4 = process.memory_info().rss
    print(f'mem+ {used_mem_start4 - used_mem_start3:_}')
