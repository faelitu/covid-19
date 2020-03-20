__author__ = "Rafael Machado"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "../data/localData/"
nc = pd.read_csv(path+"newCasesWithClass.csv") # to gen run getData...
nc.set_index("Unnamed: 0", inplace=True)
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