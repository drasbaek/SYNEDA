#!/bin/bash

# activate env
source env/bin/activate

echo -e "[INFO:] INTIALISING MODEL TRAINING"
# train SYNEDA model
#python -m spacy train training/configs/config_SYNEDA.cfg --output ./models/SYNEDA

# train SYNEDA-DANSK
python -m spacy train training/configs/config_SYNEDA_DANSK.cfg --output ./models/SYNEDA_DANSK

deactivate
echo -e "[INFO:] DONE!"