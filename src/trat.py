import pandas as pd

df = pd.read_csv("confirmedGit.csv")

df.fillna("", inplace=True)
df["Country"] = df["Province/State"] + df["Country/Region"]
del df["Province/State"], df["Country/Region"]
df.set_index("Country", inplace=True, verify_integrity=True)
lat, longt = df["Lat"], df["Long"]
df = df.T
df.drop("Lat", inplace=True)
df.drop("Long", inplace=True)

countrys = df.columns

df.reset_index(inplace=True)
dfAux = df.shift()
dfAux.iloc[0] = dfAux.iloc[1] 

out = pd.DataFrame()
for cc in countrys:
    out[cc] = df[cc] - dfAux[cc]
    out[out[cc] < 0] = 0
out = out.append(lat)
out = out.append(longt)
out.to_csv("coronga.csv")