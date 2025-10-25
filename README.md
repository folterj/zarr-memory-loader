# zarr-memory-loader
Zarr in-memory compressed and re-compressed data loader
- Loads all compressed data into memory
- Re-compress data into different compression into memory
- Access like regular zarr store
- Decompressing data on-the-fly

Test using compressed zarr data (Blosc): 777,096,071, uncompressed: 878,276,274

### Regular zarr file store (Blosc)
```
init time 0.0 s
used mem 4,509,696
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time / read 0.000923 s
```

### Compressed memory store (Blosc)
```
init time 0.9 s
used mem 782,999,552
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time / read 0.000662 s
```

### Recompress in memory store (Blosc)
```
init time 17.5 s
used mem 770,895,872
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time / read 0.000300 s
```

### Re-compressed in memory store (Jpeg XR lossless)
```
init time 18.5 s
used mem 244,330,496
random read tile size 256 in shape (10880, 9920, 3)
time / read 0.002468 s
```

### Re-compressed in memory store (Jpeg XR lossy 75%)
```
init time 13.1 s
used mem 53,534,720
random read tile size 256 in shape (10880, 9920, 3)
time / read 0.001314 s
```


### CompressedSource using zarr memory store (Jpeg XR lossy 75%)
Data: H&E 8-bit RGB (from compressed Ome-Tiff)

```
data size 16,073,485,848

init time 205.4 s *
used mem 746,586,112
random read tile size 256 in shape (44093, 121512, 3)
time / read 0.001204 s

* longer init time due to data size larger than available RAM
```
