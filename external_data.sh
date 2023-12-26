#!/bin/bash

# activate env 
source env/bin/activate

# fetch data 
echo "[INFO:] Fetching data ..."
python src/external_data/fetch_data.py

# combine data
echo "[INFO:] Creating new SYNEDA-DANSK dataset by combining datasets..."
python src/external_data/combine_SYNEDA_DANSK.py

# deactivate
echo "[INFO:] DONE! ..."
deactivate