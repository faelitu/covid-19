__author__ = "Bruno Vilela"
import os, glob
import pandas as pd

path = "../data/temperature/"
all_files = glob.glob(os.path.join(path, "*.csv"))

all_df = []
for f in all_files:
    df = pd.read_csv(f, sep=',')
    df['file'] = f.split('/')[-1]
    all_df.append(df)
    #print(f)
    
merged_df = pd.concat(all_df, ignore_index=True, sort=True)
merged_df.to_csv("../data/localData/temperature.csv", index=False)