# boxdist

Cythonized geodetic and planar distance functions for R-Trees. The implementation is adapted from [Tile38](https://github.com/tidwall/tile38/blob/f24c251ee61e9c7a3cea50df82f1ebdc7be2bb64/internal/collection/geodesic.go), which is based on the paper [Geodetic Distance Queries on R-Trees for Indexing Geographic Data](https://dl.acm.org/doi/10.5555/2960717.2960729).

## Geodetic

```python
from boxdist import geodetic_box_dist

targetlon = -72.946472
targetlat = 45.154927

minlon = -74.19342
minlat = 45.265222
maxlon = -73.157959
maxlat = 45.704261

meters = geodetic_box_dist(
    targetlon,
    targetlat,
    minlon,
    minlat,
    maxlon,
    maxlat,
)

meters #=> 20612.892322138163
```

## Planar

```python
from boxdist import planar_box_dist

targetx = 0
targety = 0

minx = 1
miny = 1
maxx = 2
maxy = 2

squared_dist = planar_box_dist(
    targetx,
    targety,
    minx,
    miny,
    maxx,
    maxy,
)

squared_dist #=> 2
```
