# zarr-memory-loader
Zarr in-memory compressed data loader
- Loads all compressed data into memory
- Access like regular zarr store
- Decompressing data on-the-fly

Test using compressed zarr data: 777,096,071, uncompressed: 878,276,274
```
used mem 6_803_456
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time 60.84220291999918
used mem+ 93_655_040

used mem 783_552_512
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time 38.00651500399999
used mem+ 86_016
```