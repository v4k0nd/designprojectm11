mkdir -p outputs/dataset-1-100
FILES=$(find ./dataset-1-100 -type f  -printf "%h/%f ")
python3 demo/demo.py --input $FILES --output ./outputs/dataset-1-100/