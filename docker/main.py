import json
import shutil
import tempfile
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

from pathlib import Path
import subprocess

app = FastAPI()

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

        Path(out_tmp).mkdir(parents=True, exist_ok=True)
        
        inputs = " ".join(list_a)
        # subprocess run handles string variables with space weirdly.. so im only using one picture
        # inputs = list_a[3]
        # subprocess.run(["python3", "demo/demo.py", "--input",  f"{inputs}", "--output", out_tmp])
        try:
            p = subprocess.run(f"python3 demo/demo.py --input {inputs} --output {out_tmp}", shell=True)
            print(f"\ndetail of process: {p}")
        except FileNotFoundError as fnfe:
            raise HTTPException(status_code=500, detail=f"While running the algorithm, an error occured: {fnfe.strerror}")

        #
        if p.returncode != 0:
            print(p.stderr)
            raise HTTPException(status_code=500, detail="While running the algorithm, an error occured")
    
        data_json_location = Path(f"{out_tmp}/data.json")
        print(f"trying to get json from: {data_json_location}")
        if data_json_location.exists():
            with open(data_json_location) as f:
                return json.load(f)
    # return {}
    # return {"filenames": [file.filename for file in media]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/v1/analyse/" enctype="multipart/form-data" method="post">
<input name="media" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
