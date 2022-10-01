from pathlib import Path
from crosschecker import merge
import pandas as pd


# FILE_NAME_GROUND_TRUTH = "merge_result.csv"
COLUMNS_TO_USE = ["human","humanDetectron", "score", "mediaID"]

def load(file_name: str):
    return _load_handle(Path(file_name))

def _load_handle(file_name: Path):
    curr_path = file_name
    if curr_path.exists():
        return curr_path
    return  _load_handle(".." / curr_path)

def merge_csv(table1: pd.DataFrame, table2: pd.DataFrame, join_on):
    # print(table2.index)
    # exit()
    if len(table1.index) < len(table2.index):
        join = "left"
    else:
        join = "right"
    # join = "inner"
    return pd.merge(table1, table2, how=join, on=join_on)
    

csv_hdo_file_path = load("csv/merge_result.csv")
csv_mega_file_path = load("csv/megadetector-results-cleanup.csv")
csv_openp_file_path = load("csv/openpose_results-cleanup.csv")

df_hdo = pd.read_csv(csv_hdo_file_path, usecols=COLUMNS_TO_USE)
df_hdo.rename(columns={"human": "ground_truth", "humanDetectron": "human_detectron", "score":"human_detectron_score"}, inplace=True, errors="raise")
df_mega = pd.read_csv(csv_mega_file_path)
df_openp = pd.read_csv(csv_openp_file_path, index_col=0)

print(df_hdo)
print(df_mega)
print(df_openp)


# print(len(df_hdo["mediaID"]))
# print(len(df_mega["mediaID"]))
# print(len(df_openp["mediaID"]))

df_merged = merge_csv(df_hdo, df_mega, "mediaID")

df_merged = merge_csv(df_merged, df_openp, "mediaID")
# print(df_merged)


df_merged = df_merged.reindex(columns=["mediaID","ground_truth","human_detectron","human_megadetector","human_openpose","human_detectron_score"])
df_merged.to_csv("../csv/humandata_all.csv")
# merge()