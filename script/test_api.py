import requests
from pathlib import Path
from pprint import pprint
import time
URL = "http://localhost:9976/v1/analyse/"

def load(file_name: str):
    return _load_handle(Path(file_name))

def _load_handle(file_name: Path):
    
    curr_path = file_name
    if curr_path.exists():
        return curr_path
    return  _load_handle(".." / curr_path)

images = list(load("dataset-1-5").iterdir())

files = []
for image_path in images:
   files.append(("media", open(str(image_path), "rb")))
files = []
start_time = time.time()
response = requests.post(URL, files=files)
print(f"this took {round(time.time() - start_time, 4)} seconds")

pprint(response)
pprint(response.json())