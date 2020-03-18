import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import keras 
 
df = pd.read_csv("../data/localData/newCases.csv")
del df["Unnamed: 0"]
y = df["3/15/20"]
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42)

model = keras.Sequential()
model.add(
  keras.layers.Bidirectional(
    keras.layers.LSTM(
      units=128,
      input_shape=(X_train.shape[0], X_train.shape[1])
    )
  )
)
model.add(keras.layers.Dropout(rate=0.2))
model.add(keras.layers.Dense(units=1))
model.compile(loss='mean_squared_error', optimizer='adam')
history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=32,
    validation_split=0.1,
    shuffle=False,
    validation_data=[X_test, y_test]
)
#score = rmsle_cv(model)
#print("LGBM score: {:.4f} ({:.4f})\n" .format(score.mean(), score.std()))