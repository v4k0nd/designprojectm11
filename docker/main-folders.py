from pathlib import Path
from PIL import Image
import subprocess
import os

INPUT_DIR = Path(os.getenv("INPUT_DIR", "/app/inputs/"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/app/outputs/"))

inputs = []
for image_path in INPUT_DIR.iterdir():
    if image_path.is_file():
        try:
            with Image.open(image_path) as img:
                img.verify()
            inputs.append(str(image_path))
        except (IOError, SyntaxError):
            print(f"Bad file: {image_path}") 

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

try:
    p = subprocess.run(["python3", "demo/demo.py", "--input"] + inputs + ["--output", str(OUTPUT_DIR)])
except FileNotFoundError as fnfe:
    raise RuntimeError("The required executable is missing") from fnfe
