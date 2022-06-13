import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Opening execution times JSON
with open('../../results/realtime-perf/execution_times.json') as json_file:
    data = json.load(json_file)

df = pd.DataFrame.from_dict(data)
df.columns = ["MP Hands","Heuristic","NN 23f","NN 60f"]

print(df.head())

av = df.mean(axis=0)
print(av)

ax = df.plot()
ax.set_xlabel("Frame")
ax.set_ylabel("Time (Ms)")
plt.show()