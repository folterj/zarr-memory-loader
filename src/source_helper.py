import dask
import dask.array as da
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
import os.path
from tifffile import imread, TiffFile
import zarr


def load_zarr_source(uri, level=0):
    data = None
    dim_order = None

    location = parse_url(uri)
    nodes = zarr.open(store=location.store, mode='r')
    if nodes:
        node0 = nodes[0]
        data = node0[level]
        metadata = dict(data.attrs) or dict(node0.attrs)
        axes = metadata.get('axes', [])
        dim_order = ''.join([axis.get('name') for axis in axes])
        if not dim_order:
            dim_order = 'tczyx'
    return data, dim_order


def load_ome_zarr_source(uri, level=0):
    data = None
    dim_order = None

    location = parse_url(uri)
    if location is None:
        raise FileNotFoundError(f'Error parsing ome-zarr file {uri}')
    reader = Reader(location)
    nodes = list(reader())
    if not nodes and 'bioformats2raw.layout' in reader.zarr.root_attrs:
        # try 0 subdirectory
        location = parse_url(uri + '/0')
        if location is not None:
            reader = Reader(location)
            nodes = list(reader())
    if nodes:
        node0 = nodes[0]
        data = node0.data[level]
        metadata = node0.metadata
        axes = metadata.get('axes', [])
        dim_order = ''.join([axis.get('name') for axis in axes])
    return data, dim_order


def load_tiff_source(uri, level=0):
    with TiffFile(uri) as tiff:
        if tiff.series:
            page = tiff.series[0]
        else:
            page = tiff.pages.first
        if level > 0:
            page = page.levels[level]
        shape = page.shape
        dtype = page.dtype
        dim_order = page.axes.lower().replace('s', 'c').replace('r', '')

        lazy_array = dask.delayed(imread)(uri)
        data = da.from_delayed(lazy_array, shape=shape, dtype=dtype)

    return data, dim_order


def load_source(uri, level=0):
    ext = os.path.splitext(uri)[1].lower()
    if 'zarr' in ext:
        return load_ome_zarr_source(uri, level)
    if 'tif' in ext:
        return load_tiff_source(uri, level)
    else:
        raise NotImplementedError(f'Extension {ext} not supported')
