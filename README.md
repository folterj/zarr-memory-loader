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
time / read 2.982362002512673e-05
```

### Compressed memory store (Blosc)
```
init time 0.9 s
used mem 782,999,552
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time / read 2.9866785000194796e-05
```

### Recompress in memory store (Blosc)
```
init time 17.5 s
used mem 770,895,872
random read tile size 256 in shape (1, 3, 1, 10880, 9920)
time / read 3.079371999774594e-05
```

### Re-compressed in memory store (Jpeg XR lossless)
```
init time 18.5 s
used mem 244,330,496
random read tile size 256 in shape (10880, 9920, 3)
time / read 0.011478627169999527
```

### Re-compressed in memory store (Jpeg XR lossy 75%)
```
init time 13.1 s
used mem 53,534,720
random read tile size 256 in shape (10880, 9920, 3)
time / read 0.007241663605000213
```
