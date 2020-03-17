import pandas as pd

path = "../data/localData/"

nc = pd.read_csv(path+"newCases.csv") # to gen run convertDataTo...
tempt = pd.read_csv(path+"temperature.csv") # to gen run joinTempCsv...

