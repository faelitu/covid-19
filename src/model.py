__author__ = "Bruno Vilela"

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import lightgbm as lgb
df = pd.read_csv("../data/localData/newCasesWithClass.csv")
temp = pd.read_csv("../data/localData/temperatureWithClass.csv")

df.set_index("Unnamed: 0", inplace=True)
countrys = df.index
model = None
del df["lat"], df["long"]

def split_data(train_data, country, cl):
    train_data['index'] = pd.to_datetime(train_data['index'])
    temp['DATE'] = pd.to_datetime(temp['DATE'])
    #train_data['month'] = train_data['index'].dt.month
    train_data['day'] = train_data['index'].dt.dayofweek
    #train_data['year'] = train_data['index'].dt.year
    y = train_data[country]

    aux = temp.groupby(["class", "DATE"]).agg({"TEMP": "mean"}).reset_index()
    train_data = train_data.merge(aux[aux["class"] == cl], left_on= "index", right_on= "DATE", how="left")
    del train_data[country], train_data['index'], train_data['DATE']
    train_x, test_x, train_y, test_y = train_test_split(train_data,y, test_size=0.01, random_state=2018)
    return (train_x, test_x, train_y, test_y)

for country in countrys: #countrys
    cc = df.loc[country]
    cl = cc.loc["class"]
    cc.drop(["a", "c", "d", "class"], inplace=True)
    cc = cc.reset_index()   

    train_x, test_x, train_y, test_y = split_data(cc, country, cl)

    
    params = {
        'nthread': 10,
         'max_depth': 50,
#         'max_depth': 9,
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'regression_l1',
        'metric': 'mape', # this is abs(a-e)/max(1,a)
#         'num_leaves': 39,
        'num_leaves': 64,
        'learning_rate': 0.00002,
       'feature_fraction': 0.9,
#         'feature_fraction': 0.8108472661400657,
#         'bagging_fraction': 0.9837558288375402,
       'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'lambda_l1': 3.097758978478437,
        'lambda_l2': 2.9482537987198496,
#       'lambda_l1': 0.06,
#       'lambda_l2': 0.1,
        'verbose': 1,
        'min_child_weight': 6.996211413900573,
        'min_split_gain': 0.037310344962162616,
        }
    lgb_train = lgb.Dataset(train_x,train_y)
    lgb_valid = lgb.Dataset(test_x,test_y)
    if model is not None:
        model = lgb.train(params, lgb_train, 3000, valid_sets=[lgb_train, lgb_valid],early_stopping_rounds=50, verbose_eval=50, init_model = model)
    else:
        model = lgb.train(params, lgb_train, 3000, valid_sets=[lgb_train, lgb_valid],early_stopping_rounds=50, verbose_eval=50)

cc = df.loc["Brazil"]
cl = cc.loc["class"]
cc.drop(["a", "c", "d", "class"], inplace=True)
cc = cc.reset_index()   
train_x, test_x, train_y, test_y = split_data(cc, "Brazil", cl)  
model.predict(test_x)
#model = model(train_x,train_y,test_x,test_y)
#del df["Unnamed: 0"]
#y = df["3/15/20"]
#X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)
#
#model = keras.Sequential()
#model.add(
#  keras.layers.Bidirectional(
#    keras.layers.LSTM(
#      units=128,
#      input_shape=(X_train.shape[1], X_train.shape[2])
#    )
#  )
#)
#model.add(keras.layers.Dropout(rate=0.2))
#model.add(keras.layers.Dense(units=1))
#model.compile(loss='mean_squared_error', optimizer='adam')
#history = model.fit(
#    X_train, y_train,
#    epochs=30,
#    batch_size=32,
#    validation_split=0.1,
#    shuffle=False,
#    validation_data=[X_test, y_test]
#)
##score = rmsle_cv(model)
#print("LGBM score: {:.4f} ({:.4f})\n" .format(score.mean(), score.std()))