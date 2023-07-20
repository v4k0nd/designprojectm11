#!/bin/bash
nvidia-smi
uvicorn main:app --host 0.0.0.0 --port 9976 --reload