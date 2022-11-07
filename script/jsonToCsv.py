import os
import pandas as pd
import json

DIRECTORY = "C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\images for testing"

def jsonToCsv(json):
    mediaIDs = []
    predictions = pd.DataFrame(columns=["media_id", "label"])
    for media in json.get("media"):
        mediaIDs.append(media.get("filename"))
    for file in os.scandir(DIRECTORY):
        if file.name in mediaIDs:
            predictions = pd.concat([predictions, pd.DataFrame([[file.name[:-4], "1"]], columns=["media_id", "label"])], ignore_index=True)
        else:
            predictions = pd.concat([predictions, pd.DataFrame([[file.name[:-4], "0"]], columns=["media_id", "label"])], ignore_index=True)

    print(predictions.head())
    predictions.to_csv("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\algorithm_predictions.csv")


def addGroundTruth(img_labels):
    predictions = pd.read_csv("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\algorithm_predictions.csv")
    mediaIds = predictions["media_id"].values.tolist()
    imageLabels = pd.read_csv(img_labels)
    ground_truth = pd.DataFrame(columns=["ground_truth"])
    for mediaId in mediaIds:
        print(imageLabels.loc[imageLabels["media_id"]==mediaId]["scientificName"].values.tolist())
        if imageLabels.loc[imageLabels["media_id"]==mediaId]["scientificName"].values == "Homo sapiens":
            ground_truth = pd.concat([ground_truth, pd.DataFrame([[1]], columns=["ground_truth"])], ignore_index=True)
        else:
            ground_truth = pd.concat([ground_truth, pd.DataFrame([[0]], columns=["ground_truth"])], ignore_index=True)
    predictions = pd.concat([predictions, ground_truth], axis=1)
    predictions.to_csv("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\algorithm_predictions_and_groundtruth.csv")


with open("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\example_apioutput_diopsis.json", 'r') as json_file:
    json = json.load(json_file)
jsonToCsv(json)
addGroundTruth("C:\\Users\\chris\\Documents\\University\\design project\\data\\testing\\labels_testing.csv")

