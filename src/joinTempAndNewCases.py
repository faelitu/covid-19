__author__ = "Rafael Machado"

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
temp = pd.read_csv(path+"temperature.csv") # to gen run joinTempCsv...

# ---------- CALCULATING RADIUS FOR NEW CASES ----------

countries = nc["Unnamed: 0"]
latlong = pd.DataFrame()
latlong["lat"] = nc["lat"]
latlong["long"] = nc["long"]
nc = nc.drop(["lat", "long"], axis=1)
nc["Total"] = nc.sum(axis=1).astype(int)

cases = 0
radius = []
m = 1000
for c in range(0, len(nc)):
    cases = nc["Total"].iloc[c]
    if (cases == 0):
        radius.append(0.0 * m)
    elif (cases <= 5):
        radius.append(4.0 * m)
    elif (cases <= 10):
        radius.append(6.333333333333334 * m)
    elif (cases <= 25):
        radius.append(8.666666666666668 * m)
    elif (cases <= 100):
        radius.append(11.0 * m)
    elif (cases <= 200):
        radius.append(13.333333333333336 * m)
    elif (cases <= 500):
        radius.append(15.666666666666668 * m)
    elif (cases <= 1000):
        radius.append(18.0 * m)
    elif (cases <= 2000):
        radius.append(20.333333333333336 * m )
    elif (cases <= 5000):
        radius.append(22.66666666666667 * m)
    elif (cases <= 70000):
        radius.append(25.0 * m)
    else: # China
        radius.append(60.0 * m)

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

#print(gnc.head())

# ---------- TEMPERATURE ----------

#print(tempt.head())

temp = temp.rename(columns={"LATITUDE": "Latitude", "LONGITUDE": "Longitude"})

print(temp.columns)
print(gnc)

#meanTemps = pd.DataFrame()
#for c in range(0, len(gnc)):
#    temps = pd.DataFrame()
#    for t in range(0, len(temp)):
#        if ((abs(gnc["Latitude"].iloc[c] - temp["LATITUDE"].iloc[t])**2 + abs(gnc["Longitude"].iloc[c] - temp["LONGITUDE"].iloc[t])**2)**(1/2) <= gnc["Radius"].iloc[c]): # formula for checking if a point is inside a circle
#            temps.append(temp.iloc[t])
#    meanTemps.append(temps.mean(), ignore_index=True)

class Area:
    def __init__(self, id, cLat, cLong, rad, area):
        self.id = id
        self.cLat = cLat
        self.cLong = cLong
        self.rad = rad
        self.area = area

def isInArea(xC, yC, xP, yP, R):
    if (((abs(xC - xP)**2) + (abs(yC - yP)**2))**(1/2) <= R):
        return True
    return False

gnc["AreaId"] = 0
areas = []
for c in range(0, len(gnc)):
    areas.append(Area(c, gnc["Latitude"].iloc[c], gnc["Longitude"].iloc[c], gnc["Radius"].iloc[c], gnc["Area"].iloc[c]))
    gnc["AreaId"].iloc[c] = c

temp["AreaId"] = 0
for a in areas:
    temp["AreaId"][((a.cLat - temp["Latitude"])**2) + ((a.cLong - temp["Longitude"])**1/2)  <= a.rad] = a.id

print(temp["AreaId"])

gnc.to_csv("../data/localData/treatNewCases.csv")
temp.to_csv("../data/localData/treatTemperature.csv")