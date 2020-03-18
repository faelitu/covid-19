import pandas as pd
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
import geopandas
import matplotlib.pyplot as plt

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


path = "../data/localData/"

nc = pd.read_csv(path+"newCases.csv") # to gen run convertDataTo...
tempt = pd.read_csv(path+"temperature.csv") # to gen run joinTempCsv...

# ---------- CALCULATING RADIUS FOR NEW CASES ----------

countries = nc["Unnamed: 0"]
latlong = pd.DataFrame()
latlong["lat"] = nc["lat"]
latlong["long"] = nc["long"]
nc = nc.drop(["lat", "long"], axis=1)
nc["Total"] = nc.sum(axis=1).astype(int)

cases = 0
radius = []
for c in range(0, len(nc)):
    cases = nc["Total"].iloc[c]
    if (cases == 0):
        radius.append(0.0)
    elif (cases <= 5):
        radius.append(4.0)
    elif (cases <= 10):
        radius.append(6.333333333333334)
    elif (cases <= 25):
        radius.append(8.666666666666668)
    elif (cases <= 100):
        radius.append(11.0)
    elif (cases <= 200):
        radius.append(13.333333333333336)
    elif (cases <= 500):
        radius.append(15.666666666666668)
    elif (cases <= 1000):
        radius.append(18.0)
    elif (cases <= 2000):
        radius.append(20.333333333333336)
    elif (cases <= 5000):
        radius.append(22.66666666666667)
    elif (cases <= 70000):
        radius.append(25.0)
    else: # China
        radius.append(60.0)

nc["Radius"] = radius
nc["Latitude"] = latlong["lat"]
nc["Longitude"] = latlong["long"]

#print(nc.head())

# ---------- CREATING GEO DATA FRAME ----------

gnc = geopandas.GeoDataFrame(
    nc, geometry=geopandas.points_from_xy(nc.Longitude, nc.Latitude))

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Restrict to a continent example
#ax = world[world.continent == 'South America'].plot(
#    color='white', edgecolor='black')

ax = world.plot(color='white', edgecolor='black')

# We can now plot our ``GeoDataFrame``.
gnc.plot(ax=ax, color='red')

#plt.show()

# ---------- CALCULATING AREA ----------

area = []

for c in range(0, len(nc)):
    # Note: maybe multiply the radius by 1000 or a larger number
    area.append(geodesic_point_buffer(gnc["Latitude"].iloc[c], gnc["Longitude"].iloc[c], gnc["Radius"].iloc[c]))

gnc["Area"] = area

print(gnc.head())

# ---------- TEMPERATURE ----------