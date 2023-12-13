#!/bin/bash

## SCRIPT TO DEBUG CONFIG AND DATA TO MAKE SURE EVERYTHING WORKS!

# activate env
source env/bin/activate

# debug small model
echo -e "[INFO:] DEBUGGING CONFIG ..."
python -m spacy debug config training/configs/config_SYNEDA.cfg 

echo -e "[INFO:] DEBUGGING DATA ..."
python -m spacy debug data training/configs/config_SYNEDA.cfg --verbose

deactivate
echo -e "[INFO:] DONE!"