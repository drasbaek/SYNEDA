#!/bin/bash

# activate env
source env/bin/activate

# debug small model
echo -e "[INFO:] DEBUGGING CONFIG ..."
python -m spacy debug config training/configs/config_small.cfg 

echo -e "[INFO:] DEBUGGING DATA ..."
python -m spacy debug data training/configs/config_small.cfg --verbose

deactivate
echo -e "[INFO:] DONE!"