from ome_zarr.io import parse_url
import zarr


class ZarrSource:
    def __init__(self, uri):
        self.uri = uri
        self.store = None

    def get_root(self):
        self.store = parse_url(self.uri).store
        root = zarr.open(store=self.store, mode='r')
        return root
