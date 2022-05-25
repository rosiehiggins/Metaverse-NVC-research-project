import os
#manually add dll directories because they can't be found in system path
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
os.add_dll_directory("C:/tools/cuda/bin")

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
import numpy as np
import pandas as pd
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.metrics import precision_recall_curve,average_precision_score,PrecisionRecallDisplay
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from itertools import cycle

# Load in the model
model = load_model("../../model/gestureClassifier/v20/model.h5")

# Show the model architecture
model.summary()

#load dataset
df = pd.read_csv("../../training-data/dataset/dataset_multiclass_features10.csv",dtype=np.float32)

dataset = df.to_numpy()
#all rows, -1 cols
X = dataset[:,0:23]
#all rows, last 4 cols
Y = dataset[:,-4:]

#Generate same test set as used in training
#TODO consider splitting into different files
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=0.2,random_state=42)

#predict some values
Y_pred = model.predict(X_test)


#code adapted from https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html
# For each class
n_classes = 4
index_to_class = {0:"thumbs up", 1:"raise hand",2:"ok",3:"non-gesture"}

precision = dict()
recall = dict()
average_precision = dict()
for i in range(n_classes):
    precision[i], recall[i], _ = precision_recall_curve(Y_test[:, i], Y_pred[:, i])
    average_precision[i] = average_precision_score(Y_test[:, i], Y_pred[:, i])

# A "micro-average": quantifying score on all classes jointly
precision["micro"], recall["micro"], _ = precision_recall_curve(
    Y_test.ravel(), Y_pred.ravel()
)
average_precision["micro"] = average_precision_score(Y_test, Y_pred, average="micro")

# setup plot details
colors = cycle(["navy", "turquoise", "darkorange", "cornflowerblue"])

_, ax = plt.subplots(figsize=(7, 8))

f_scores = np.linspace(0.2, 0.8, num=4)
lines, labels = [], []
for f_score in f_scores:
    x = np.linspace(0.01, 1)
    y = f_score * x / (2 * x - f_score)
    (l,) = plt.plot(x[y >= 0], y[y >= 0], color="gray", alpha=0.2)
    plt.annotate("f1={0:0.1f}".format(f_score), xy=(0.9, y[45] + 0.02))

display = PrecisionRecallDisplay(
    recall=recall["micro"],
    precision=precision["micro"],
    average_precision=average_precision["micro"],
)
display.plot(ax=ax, name="Micro-average precision-recall", color="gold")

for i, color in zip(range(n_classes), colors):
    display = PrecisionRecallDisplay(
        recall=recall[i],
        precision=precision[i],
        average_precision=average_precision[i],
    )
    display.plot(ax=ax, name=f"Precision-recall for {index_to_class[i]}", color=color)

# add the legend for the iso-f1 curves
handles, labels = display.ax_.get_legend_handles_labels()
handles.extend([l])
labels.extend(["iso-f1 curves"])
# set the legend and the axes
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.legend(handles=handles, labels=labels, loc="best")
ax.set_title("Precision-Recall curve")

plt.show()