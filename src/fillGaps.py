__author__ = "Bruno Vilela"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "../data/localData/"
nc = pd.read_csv(path+"newCasesWithClass.csv") # to gen run getData...
nc.set_index("Unnamed: 0", inplace=True)
lat, long, a, c, d, clss = nc["lat"], nc["long"], nc["a"], nc["c"], nc["d"], nc["class"] 
del nc["lat"], nc["long"], nc["a"], nc["c"], nc["d"], nc["class"] 
italy = pd.DataFrame(nc.loc["Italy"])

