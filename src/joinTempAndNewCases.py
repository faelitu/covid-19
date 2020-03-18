import pandas as pd
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point

path = "../data/localData/"

nc = pd.read_csv(path+"newCases.csv") # to gen run convertDataTo...
tempt = pd.read_csv(path+"temperature.csv") # to gen run joinTempCsv...

proj_wgs84 = pyproj.Proj(init='epsg:4326')


def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return transform(project, buf).exterior.coords[:]

# Example
#b = geodesic_point_buffer(45.4, -75.7, 100.0)
#print(b)