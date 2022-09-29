import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt

# from sklearn import svm, datasets
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import ConfusionMatrixDisplay

def handle_running_from_different_directories(file_name: str):
    cwd = Path.cwd()
    base =  "csv" / Path(file_name)
    if (cwd / base).exists():
        return cwd / base
    elif (cwd / ".." / base).exists():
        return cwd / ".." / base

file_name_ground_truth = "merge_result.csv"
csv_loc = handle_running_from_different_directories(file_name_ground_truth)
df = pd.read_csv(csv_loc)

# create cutoffs csv
df_2 = df[["human", "humanDetectron", "score"]].copy()
df_2["score"] = df_2["score"].round(decimals = 3)
df_2.rename(columns={"human": "ground_truth", "humanDetectron": "detectron-all"}, inplace=True, errors="raise")

df_2["detectron-0.5"] = df_2["detectron-all"].where(df_2["score"] > 0.5, 0).tolist()
df_2["detectron-0.6"] = df_2["detectron-all"].where(df_2["score"] > 0.6, 0).tolist()
df_2["detectron-0.7"] = df_2["detectron-all"].where(df_2["score"] > 0.7, 0).tolist()
df_2["detectron-0.8"] = df_2["detectron-all"].where(df_2["score"] > 0.8, 0).tolist()

df_2.to_csv("./csv/cutoffs.csv")


# Calculating Confusion matrix
y = df["human"] # definite truth

for conf_level in np.arange(0.5, 0.85, 0.05):
    conf_level = round(conf_level,2)
    X = df["humanDetectron"].where(df['score'] > conf_level, 0)
    # continue
    tn, fp, fn, tp = confusion_matrix(y, X).ravel()
    print(f"\n\tcutoff conf lvl: {conf_level}\n tn:{tn}\n fp:{fp}\n fn:{fn}\n tp:{tp}")

