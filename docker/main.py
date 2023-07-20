import json
import shutil
import tempfile
from typing import List
import os
from PIL import Image
import gpustat

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
import subprocess

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/gpus")
async def list_gpus():
    return gpustat.new_query().jsonify()

@app.get("/cam", response_class=HTMLResponse)
def get_camera(request: Request): 
    return templates.TemplateResponse("cam.html", {"request": request})
  
@app.get("/tmp/{file_path:path}")
def get_image(
    file_path: str
):
    return FileResponse(f"./outputs/tmp/{file_path}")

@app.post("/live-cam")
async def stream_camera(
    
):
    try:
        p = subprocess.run(["python3", "demo/demo.py", "--webcam"])
            # p = subprocess.run(f"python3 demo/demo.py --input {inputs} --output {out_tmp}", shell=True)
    except FileNotFoundError as fnfe:
            raise HTTPException(status_code=500, detail=f"While running the algorithm, an error occured: {fnfe.strerror}")

@app.post("/v1/analyse/")
async def create_upload_files(
    media: List[UploadFile] = File(description="Multiple files as UploadFile"),
):
    with tempfile.TemporaryDirectory() as tmpdirname:
        out_tmp = str(Path(f"./outputs{tmpdirname}/"))
        
        inputs = []
        for file in media:
            file_location = str(Path(f"{tmpdirname}/{file.filename}"))
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object) 
            inputs.append(file_location)

        # Debugging
        print("File:", file_location) # print the name of the file
        print("out_tmp:", out_tmp) # print the name of the file
        print("Exists:", os.path.exists(file_location)) # check if the file exists
        print("Is file:", os.path.isfile(file_location)) # check if it's a file (not a directory)

        try:
            img = Image.open(file_location) # try opening the image
            img.verify() # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            print('Bad file:', file_location) # print out the names of bad files
        
        Path(out_tmp).mkdir(parents=True, exist_ok=True)
        
        try:
            p = subprocess.run(["python3", "demo/demo.py", "--input"] + inputs + ["--output", out_tmp])
            # p = subprocess.run(f"python3 demo/demo.py --input {inputs} --output {out_tmp}", shell=True)
        except FileNotFoundError as fnfe:
            raise HTTPException(status_code=500, detail=f"While running the algorithm, an error occured: {fnfe.strerror}")

        # if p.returncode != 0:
        #     print(p.stderr)
        #     raise HTTPException(status_code=500, detail="While running the algorithm, an error occured")
    
        data_json_location = Path(f"{out_tmp}/data.json")
        print(f"trying to get json from: {data_json_location}")
        if data_json_location.exists():
            with open(data_json_location) as f:
                return json.load(f)
        else:
            raise HTTPException(status_code=500, detail=f"did not find {data_json_location}")
            


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
