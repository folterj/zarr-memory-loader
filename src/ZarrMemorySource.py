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

    def get_root(self):
        if self.store is None:
            # if not loaded into memory, revert to normal file store
            self.store = parse_url(self.uri).store
        root = zarr.open(store=self.store, mode='r')
        return root
