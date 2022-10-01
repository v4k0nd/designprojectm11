import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from rich import print
from rich.console import Console
from rich.table import Table
from rich import box 

# Configure script

FILE_NAME_GROUND_TRUTH = "merge_result.csv"
COLUMNS_TO_USE = ["human","humanDetectron", "score", "mediaID"]


def table_setup():
    table = Table(title="", box=box.ROUNDED)
    table.add_column("")
    table.add_column("predicted 0")
    table.add_column("predicted 1")
    return table

def handle_running_from_different_directories(file_name: str):
    cwd = Path.cwd()
    base =  "csv" / Path(file_name)
    if (cwd / base).exists():
        return cwd / base
    elif (cwd / ".." / base).exists():
        return cwd / ".." / base


def create_cutoff_csv():
    # create cutoffs csv
    df_2 = df[["human", "humanDetectron", "score"]].copy()
    df_2["score"] = df_2["score"].round(decimals = 3)
    df_2.rename(columns={"human": "ground_truth", "humanDetectron": "detectron-all"}, inplace=True, errors="raise")

    df_2["detectron-0.5"] = df_2["detectron-all"].where(df_2["score"] > 0.5, 0).tolist()
    df_2["detectron-0.6"] = df_2["detectron-all"].where(df_2["score"] > 0.6, 0).tolist()
    df_2["detectron-0.7"] = df_2["detectron-all"].where(df_2["score"] > 0.7, 0).tolist()
    df_2["detectron-0.8"] = df_2["detectron-all"].where(df_2["score"] > 0.8, 0).tolist()

    df_2.to_csv("./csv/cutoffs.csv")

console = Console(record=True)




csv_loc = handle_running_from_different_directories(FILE_NAME_GROUND_TRUTH)

df = pd.read_csv(csv_loc,usecols=COLUMNS_TO_USE)




# Calculating Confusion matrix
y = df["human"] # definite truth
val_count = y.value_counts()
total = len(y)
for conf_level in np.arange(0.2, 0.9, 0.05):
    conf_level = round(conf_level,2)
    console.rule(f"[bold red]Confusion matrix a={conf_level}", align="left")
    print(f"Nr of occurance of:\n{val_count}")
    print(f"total {total}")
    table = table_setup(conf_level)
    X = df["humanDetectron"].where(df['score'] > conf_level, 0)
    # continue
    tn, fp, fn, tp = confusion_matrix(y, X).ravel()
    
    f1 = f1_score(y, X)
    table.add_row("actual 0", "[blue]"+str(tn), str(fp))
    table.add_row("actual 1", str(fn), "[blue]"+str(tp))
    console.print(table)
    console.print(f"f1: [orange1]{f1}[/orange1]\n")
    # console.print(f"\n :right_arrow:   [red]{conf_level}[/red]\n tn: {tn}\ fp: {fp}\n fn: {fn}\n tp: {tp}\n f1: [orange1]{f1}[/orange1]")
    # print(f"\n\tcutoff conf lvl: {conf_level}\n tn: {tn}\n fp: {fp}\n fn: {fn}\n tp: {tp}\n f1: {f1}")
