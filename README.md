# Dockerized human detection via Detectron2

This modification to detectron2 creates a csv which for each picture shows if a person was detected in the picture, and how confident is detectron with that label.

Setup assumed a Windows 10/11, with a working Ubuntu 20.04 on WSL2, and Docker Desktop (set with WSL2 backend)


## Steps to run:

1. Get the `detectron2` repo on your device

```bash
git clone https://github.com/v4k0nd/designprojectm11.git
```

1. Start a shell and enter 

```bash
cd designprojectm11/docker
```

2. Build the image (might need to `sudo`)

```bash
docker build --build-arg USER_ID=$UID -t detectron2:v0 .
```

3. Run it (might need to `sudo`)

```bash
docker run -p 9976:9976 --gpus all -it -v /detectron2_detection/:/code/ --name=detectron2_container detectron2:v0
```

4. You should be in the docker container, and have a shell

5. Make `start.sh` runnable by: 
```bash
chmod +x start.sh
```
6. before executing it, we need to import pictures to run it on.
7. Open another shell
```bash
# get windows username
WINDOWS_USERNAME=$(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g')
docker cp /mnt/c/Users/$WINDOWS_USERNAME/Downloads/humandata/dataset-1-100  detectron2_container:/home/appuser/detectron2_repo
```
8. Go back to the docker terminal, and run it with
```bash
./start.sh
```
