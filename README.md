Setup assumed a Windows 10/11, with a working Ubuntu 20.04 on WSL2

### Steps:

1. Get the `detectron2` repo on your device

```bash
git clone https://github.com/facebookresearch/detectron2.git
```

1. Start a shell and enter 

```bash
cd detectron2/docker
```

1. Copy the original `Dockerfile` 

```bash
cp Dockerfile Dockerfile_original
```

1. Change out the ubuntu version in the docker file (`Dockerfile` )

```docker
FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04
```

1. Build the image (might need to `sudo`)

```bash
docker build --build-arg USER_ID=$UID -t detectron2:v0 .
```

1. Run it (might need to `sudo`)

```bash
docker run -p 9976:9976 --gpus all -it -v /detectron2_detection/:/code/ --name=detectron2_container detectron2:v0
```

1. You should be in the docker container, and have a shell like this

![Untitled](Dockerized%20Detectron2%20dde44cc233a6418585ee9d2a43cf4a95/Untitled.png)

1. Download an example picture then run the python demo script

```bash
wget https://farm4.staticflickr.com/3216/2471938514_1ec1fddf08_z.jpg -O input.jpg
mkdir outputs
python3 demo/demo.py --input ./input.jpg --output outputs/

# python3 demo/demo.py  \
	#--config-file configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml \
	#--input input.jpg --output outputs/ \
	#--opts MODEL.WEIGHTS detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl
```

1. Open another shell
2. Copy out the folder `outputs` to `Downloads` to windows

```bash
# get windows username
WINDOWS_USERNAME=$(/mnt/c/Windows/System32/cmd.exe /c 'echo %USERNAME%' | sed -e 's/\r//g')

docker cp detectron2_container:/home/appuser/detectron2_repo/outputs /mnt/c/Users/$WINDOWS_USERNAME/Downloads/
```
