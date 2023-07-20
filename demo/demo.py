# Copyright (c) Facebook, Inc. and its affiliates.
import argparse
import glob
import multiprocessing as mp
import numpy as np
import os
import tempfile
import time
import warnings
import cv2
import tqdm
import csv
import json
from datetime import datetime

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
import torch

from predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    # To use demo for Panoptic-DeepLab, please uncomment the following two lines.
    # from detectron2.projects.panoptic_deeplab import add_panoptic_deeplab_config  # noqa
    # add_panoptic_deeplab_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def test_opencv_video_format(codec, file_ext):
    with tempfile.TemporaryDirectory(prefix="video_format_test") as dir:
        filename = os.path.join(dir, "test_file" + file_ext)
        writer = cv2.VideoWriter(
            filename=filename,
            fourcc=cv2.VideoWriter_fourcc(*codec),
            fps=float(30),
            frameSize=(10, 10),
            isColor=True,
        )
        [writer.write(np.zeros((10, 10, 3), np.uint8)) for _ in range(30)]
        writer.release()
        if os.path.isfile(filename):
            return True
        return False


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        curr_dev_nr = torch.cuda.current_device()
        total_memory = torch.cuda.get_device_properties(curr_dev_nr).total_memory
        total_memory_gb = round(total_memory / (1024 ** 3), 1)
        
        logger.info("=========== GPU info ==========")
        logger.info(f"| Current device: {torch.cuda.current_device()}")
        logger.info(f"| Number of GPUs: {torch.cuda.device_count()}")
        logger.info(f"| Current device name: {torch.cuda.get_device_name(curr_dev_nr)}")
        logger.info(f"| Total memory on device: {total_memory_gb} GB")
        
        logger.info(f"| Memory allocated: {torch.cuda.memory_allocated(curr_dev_nr)}")
        logger.info(f"| Memory cached (reserved): {torch.cuda.memory_reserved(curr_dev_nr)}")

        logger.info("===============================")
        logger.info("\n= detectron's way of gpu info =")
        max_reserved_mb = torch.cuda.max_memory_reserved() / 1024.0 / 1024.0
        reserved_mb = torch.cuda.memory_reserved() / 1024.0 / 1024.0
        max_allocated_mb = torch.cuda.max_memory_allocated() / 1024.0 / 1024.0
        allocated_mb = torch.cuda.memory_allocated() / 1024.0 / 1024.0

        logger.info(
            (
                "| max_reserved_mem: {:.0f}MB "
                "| reserved_mem: {:.0f}MB "
                "| max_allocated_mem: {:.0f}MB "
                "| allocated_mem: {:.0f}MB "
            ).format(
                max_reserved_mb,
                reserved_mb,
                max_allocated_mb,
                allocated_mb,
            )
        )
        logger.info("===============================")
    else:
        logger.info("No GPUs detected.")
        


    demo = VisualizationDemo(cfg)
    f_csv = None
    f_json = None

    # Normalizes coordinates to a 0-1 scale.
    def normalize_coordinates(x1, y1, x2, y2, img):
        h, w = img.shape[:2]
        new_x1 = x1/(w - 1.)
        new_y1 = y1/(h - 1.)
        new_x2 = x2/(w - 1.)
        new_y2 = y2/(h - 1.)
        return [new_x1, new_y1, new_x2, new_y2]
    
    images_output = {}
    row_json = []

    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        for path in tqdm.tqdm(args.input, disable=not args.output):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")



            start_time = time.time()
            predictions, visualized_output = demo.run_on_image(img)
            
            row_csv = []
            
            
            file_name = path.split('/')[-1]
            mediaID = file_name.split('.')[0]


            pred_class_list = predictions["instances"].pred_classes.tolist()
            scores_list = predictions["instances"].scores.tolist()
            # print(predictions["instances"].pred_boxes.tensor.tolist())
            pred_boxes_list = predictions["instances"].pred_boxes.tensor.tolist()
            human = 0
            score = 0
            human_id = 0  
            for i, e in enumerate(pred_class_list):
                if e == 0:
                    human = 1
                    score = round(scores_list[i] , 2)

                    # contains x1, y1, x2, y2
                    pred_boxes = pred_boxes_list[i]
                    pred_boxes = normalize_coordinates(*pred_boxes, img)
                    row_json.append([path, file_name, pred_boxes, score])
                row_csv.append([mediaID, human, human_id, score])
                human_id += 1


            logger.info(
                "{}: {} in {:.2f}s".format(
                    path,
                    "detected {} instances".format(len(predictions["instances"]))
                    if "instances" in predictions
                    else "finished",
                    time.time() - start_time,
                )
            )

            if args.output:
                print(f"checking if output is there {args.output}")
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    print(f"found and it is a directory")
                    out_filename = os.path.join(args.output, os.path.basename(path))
                    # write to csv
                    if f_csv is None:
                        csv_dir = os.path.join(args.output, "data.csv")
                        f_csv = open(csv_dir, 'w', newline='')
                        header = ['mediaID', 'human', 'id', 'score']
                        writer = csv.writer(f_csv)
                        writer.writerow(header)
                    writer.writerows(row_csv)
                    # write json below
                    
                    
                else:
                    print("did not find")
                    assert len(args.input) == 1, "Please specify a directory with args.output"
                    out_filename = args.output
                visualized_output.save(out_filename)
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                if cv2.waitKey(0) == 27:
                    break  # esc to quit

        # write to json (API)
        # if f_json is None:
        json_dir = os.path.join(args.output, "data.json")
        print(f"placing data.json in: {json_dir}")
        # f_json = open(json_dir, 'w', newline='')
        # writer_ = csv.writer(f_csv)
        res = {
            "generated_by": {
                "datetime": datetime.now().isoformat(),
                "version": "0.6",
                "tag": "DT2HD"
            },
            "media": [],
            "region_groups": [],
            "predictions": [],
        }

        media_list = []
        region_groups_list = []
        predictions_list = []
        #  row_json.append([path, file_name, pred_boxes, score])
        for row in row_json:
            print(f"row: {row}")
            media_list.append({"id": row[0], "filename": row[1]})
            region_groups_list.append({"id": "",
                                    # After reading the docs im quite sure we can delete the individual_id 
                                    # "individual_id": "",
                                    "regions": [
                                            {
                                                "media_id": row[0], 
                                                "box": {
                                                    "x1": row[2][0],
                                                    "y1": row[2][1],
                                                    "x2": row[2][2],
                                                    "y2": row[2][3],
                                                }
                                            }
                                        ]
                                    })
            predictions_list.append(
                {
                    "region_group_id": row[0],
                    "taxa": {
                        "type": "Homo sapiens",
                        "items": [{
                            "scientific_name": "Homo sapiens",
                            "probability": row[3],
                            "scientific_name_id": "https://data.biodiversitydata.nl/naturalis/specimen/RGM.1332465"
                        }]
                    }
                
                }
            )
        res["media"] = media_list
        res["region_groups"] = region_groups_list
        res["predictions"] = predictions_list
        print(json.dumps(res))
        with open(json_dir, 'w') as f:
            json.dump(res, f)


    elif args.webcam:
        assert args.input is None, "Cannot have both --input and --webcam!"
        assert args.output is None, "output not yet supported with --webcam!"
        cam = cv2.VideoCapture(0)
        for vis in tqdm.tqdm(demo.run_on_video(cam)):
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.imshow(WINDOW_NAME, vis)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        cam.release()
        cv2.destroyAllWindows()
    elif args.video_input:
        video = cv2.VideoCapture(args.video_input)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        basename = os.path.basename(args.video_input)
        codec, file_ext = (
            ("x264", ".mkv") if test_opencv_video_format("x264", ".mkv") else ("mp4v", ".mp4")
        )
        if codec == ".mp4v":
            warnings.warn("x264 codec not available, switching to mp4v")
        if args.output:
            if os.path.isdir(args.output):
                output_fname = os.path.join(args.output, basename)
                output_fname = os.path.splitext(output_fname)[0] + file_ext
            else:
                output_fname = args.output
            assert not os.path.isfile(output_fname), output_fname
            output_file = cv2.VideoWriter(
                filename=output_fname,
                # some installation of opencv may not support x264 (due to its license),
                # you can try other format (e.g. MPEG)
                fourcc=cv2.VideoWriter_fourcc(*codec),
                fps=float(frames_per_second),
                frameSize=(width, height),
                isColor=True,
            )
        assert os.path.isfile(args.video_input)
        for vis_frame in tqdm.tqdm(demo.run_on_video(video), total=num_frames):
            if args.output:
                output_file.write(vis_frame)
            else:
                cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
                cv2.imshow(basename, vis_frame)
                # send back visframe
                vis_frame
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        video.release()
        if args.output:
            output_file.release()
        else:
            cv2.destroyAllWindows()
