import json
import shutil
import tempfile
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

from pathlib import Path
import subprocess

app = FastAPI()


@app.post("/files/")
async def create_files(
    media: List[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in media]}


@app.post("/v1/analyse/")
async def create_upload_files(
    media: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    with tempfile.TemporaryDirectory() as tmpdirname:
        out_tmp = str(Path(f"./outputs{tmpdirname}/"))
        
        list_a = []
        for file in media:
            file_location = str(Path(f"{tmpdirname}/{file.filename}"))
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object) 
            list_a.append(file_location)

        # subprocess run handles spaces weirdly.. so im only using one picture
        # inputs = " ".join(list_a)
        inputs = list_a[3]

        Path(out_tmp).mkdir(parents=True, exist_ok=True)
        subprocess.run(["python3", "demo/demo.py", "--input",  f"{inputs}", "--output", out_tmp])
        data_json = Path(f"{out_tmp}/data.json")
        print(data_json)
        if data_json.exists():
            with open(data_json) as f:
                return json.load(f)
    
    return {"filenames": [file.filename for file in media]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="media" type="file" multiple>
<input type="submit">
</form>
<form action="/v1/analyse/" enctype="multipart/form-data" method="post">
<input name="media" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
