import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from pathlib import Path
from sklearn import svm, datasets
# from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay

# import some data to play with
# iris = datasets.load_iris()

def handle_running_from_different_directories(file_name: str):
    cwd = Path.cwd()
    base =  "csv" / Path(file_name)
    if (cwd / base).exists():
        return cwd / base
    elif (cwd / ".." / base).exists():
        return cwd / ".." / base
    # print(csv_loc)
# exit()

file_name = "humandata_modified.csv"
csv_loc = handle_running_from_different_directories(file_name)

df = pd.read_csv(csv_loc)
print(df)
exit()



## working on it

X = iris.data
y = iris.target
class_names = iris.target_names

# Split the data into a training set and a test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
# classifier = svm.SVC(kernel="linear", C=0.01).fit(X_train, y_train)

# np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
titles_options = [
    ("Confusion matrix, without normalization", None),
    ("Normalized confusion matrix", "true"),
]
for title, normalize in titles_options:
    disp = ConfusionMatrixDisplay.from_estimator(
        classifier,
        X_test,
        y_test,
        display_labels=class_names,
        cmap=plt.cm.Blues,
        normalize=normalize,
    )
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)

plt.show()