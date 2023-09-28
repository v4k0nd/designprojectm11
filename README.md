# Dockerized human detection API with FastAPI and Detectron2

This modification to detectron2 exposes an API (using FastAPI) which for each picture "batch" creates a `.json` (format specified by project client) if a person was detected in the picture, and how confident detectron2 is with that label.

Setup assumed a Windows 10/11, with a working Ubuntu 20.04 on WSL2, and Docker Desktop (set with WSL2 backend)

## Steps to run

1. clone this repo on your device

```bash
git clone https://github.com/v4k0nd/designprojectm11.git
```

2. Start a shell and enter

```bash
cd designprojectm11/docker
```

3. Build the image (might need to `sudo`), \
`Dockerfile.folder` for the folder input output version 

    ```bash
    docker build --build-arg USER_ID=$UID -t detectron2:folder-v0 -f Dockerfile.folder .
    ```

    `Dockerfile.server` for the server API call version

    ```bash
    docker build --build-arg USER_ID=$UID -t detectron2:server-v0 -f Dockerfile.server .
    ```

4. Run it (might need to `sudo`)
for the folder version
```bash
docker run -p 9976:9976 --gpus all -it \
    -v /detectron2_detection/:/code/ \
    -v $(pwd)/inputs:/home/appuser/detectron2_repo/inputs \
    -v $(pwd)/outputs:/home/appuser/detectron2_repo/outputs \
    --env INPUT_DIR=/home/appuser/detectron2_repo/inputs \
    --env OUTPUT_DIR=/home/appuser/detectron2_repo/outputs \
    --name=detectron2_container_folder detectron2:folder-v0
```
the server version
```bash
docker run -p 9976:9976 --gpus all -it -v /detectron2_detection/:/code/ --name=detectron2_container_folder detectron2:server-v0
```

5. You should be in the docker container, and FastAPI server should have started

6. Open another shell, create `dataset-1-5` in main directory, and put some pictures in it

7. To test it working, run

```bash
python3 script/test_api.py
```
