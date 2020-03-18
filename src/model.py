import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.model_selection import train_test_split

df = pd.read_csv("../data/localData/newCases.csv")
del df["Unnamed: 0"]   


model = lgb.LGBMRegressor(objective='regression')


#X_train, X_test, y_train, y_test = train_test_split( df, y, test_size=0.2, random_state=42)
#score = rmsle_cv(model)
#print("LGBM score: {:.4f} ({:.4f})\n" .format(score.mean(), score.std()))