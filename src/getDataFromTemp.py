__author__ = "Bruno Vilela, Rafael Machado"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "../data/localData/"
nc = pd.read_csv(path+"newCases.csv") # to gen run convertDataTo...
temp = pd.read_csv(path+"temperature.csv") # to gen run joinTempCsv...

fixedLat= -83.415313
fixedLong = 72.089528
R = 6371e3;

classValue = 44478.46666666667

temp["a"] = ((np.sin((temp["LATITUDE"] - fixedLat)/2) **2) + (np.cos(fixedLat) * np.cos(temp["LATITUDE"]) *(np.sin((temp["LONGITUDE"] - fixedLong)/2) **2)) )
temp["c"] = 2 * np.arctan2((temp["a"]**1/2),((temp["a"]-1)**1/2))
temp["d"] = R*temp["c"]

#for i in range(0,450):
temp["class"] = round((temp["d"] / classValue) - 450)

#nc = nc.T
nc.set_index("Unnamed: 0", inplace=True)

nc["a"] = ((np.sin((nc["lat"] - fixedLat)/2) **2) + (np.cos(fixedLat) * np.cos(nc["lat"]) *(np.sin((nc["long"] - fixedLong)/2) **2)) )
nc["c"] = 2 * np.arctan2((nc["a"]**1/2),((nc["a"]-1)**1/2))
nc["d"] = R*nc["c"]

#for i in range(0,450):
nc["class"] = round((nc["d"] / classValue) - 450)

# ------------ Rafael's alterations below ----------- #

days = []
days = nc.columns
days = days.drop(["lat", "long", "a", "c", "d", "class"])

nc = nc.T
bkp = nc.drop(days)
nc = nc.drop(["lat", "long", "a", "c", "d", "class"], axis=0)
nc = nc.replace(0, np.nan)
nc = nc.reset_index()
nc = nc.rename(columns={"index": "Date"})
countries = nc.columns
countries = countries.drop("Date")

# Converting the column to DateTime format
nc["Date"] = pd.to_datetime(days, format='%m/%d/%y')
nc = nc.set_index('Date')

# Imputing using interpolation
for c in countries:
    nc[c] = nc[c].interpolate(method='time')

print(nc)
print(bkp)

nc["Italy"].plot()
nc["Brazil"].plot()
plt.show()

bkp = bkp.T
nc = nc.T

nc = nc.merge(bkp, left_index=True, right_index=True)

print(nc)
print(bkp)

nc.to_csv(path+"newCasesWithClass_Interpolated.csv")
temp.to_csv(path+"temperatureWithClass_Interpolated.csv")