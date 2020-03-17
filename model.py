import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("full_data.csv")
df.fillna(0, inplace=True)  

locations = ["Brazil", "Italy", "United States", "United Kingdom", "Iran", "South Korea", "Japan"]
#tempt = [28]

#for location in locations:
location = "Japan"
plt.plot(df["date"][df["location"] == location], df["new_cases"][df["location"] == location], '-', label=location)

plt.grid(axis='x', color='0.95')
plt.legend(title='Parameter where:')
plt.title('plt.step(where=...)')
plt.show()