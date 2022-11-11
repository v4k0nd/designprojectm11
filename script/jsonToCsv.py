import os
import pandas as pd
import json

DIRECTORY = "C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\images for testing"

def jsonToCsv(json, dataset_name, algorithm_name):
    mediaIDs = []
    ground_truth = pd.read_csv(f"..//datasets//{dataset_name}//ground_truth.csv")
    predictions = pd.DataFrame(columns=["mediaID", "label", "ground_truth"])
    for media in json.get("media"):
        mediaIDs.append(media.get("filename"))
    for index, row in ground_truth.iterrows():
        if row["mediaID"] in mediaIDs:
            predictions = pd.concat([predictions, pd.DataFrame([[row["mediaID"], "1", row["ground_truth"]]], columns=["mediaID", "label", "ground_truth"])], ignore_index=True)
        else:
            predictions = pd.concat([predictions, pd.DataFrame([[row["mediaID"], "0", row["ground_truth"]]], columns=["mediaID", "label", "ground_truth"])], ignore_index=True)

    print(predictions.head())
    save_path = f"..\\eval_framework_results\\{algorithm_name}\\{dataset_name}.csv"
    predictions.to_csv(save_path)
    return save_path


def extractGroundTruth(dataset_dir):
    image_names = []
    ground_truth = pd.DataFrame(columns=["mediaID", "ground_truth"])
    for file in os.scandir(dataset_dir + "//images"):
        image_names.append(file.name[:-4])
    for file in os.scandir(dataset_dir):
        if file.name.endswith(".csv"):
            image_labels = pd.read_csv(file)
    for image_name in image_names:
        if image_labels.loc[image_labels["mediaID"]==image_name]["scientificName"].values == "Homo sapiens":
            ground_truth = pd.concat([ground_truth, pd.DataFrame([[image_name, 1]], columns=["mediaID", "ground_truth"])], ignore_index=True)
        else:
            ground_truth = pd.concat([ground_truth, pd.DataFrame([[image_name, 0]], columns=["mediaID", "ground_truth"])], ignore_index=True)
    ground_truth.to_csv(dataset_dir + "//ground_truth.csv")



with open("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\example_apioutput_diopsis.json", 'r') as json_file:
    json = json.load(json_file)
jsonToCsv(json)
addGroundTruth("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\labels_testing.csv")

