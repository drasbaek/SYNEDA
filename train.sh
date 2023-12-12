#!/bin/bash

# activate env
source env/bin/activate

# train small model
echo -e "[INFO:] INTIALISING MODEL TRAINING"
python -m spacy train training/configs/config_small.cfg --output ./models/syneda_small

# train big model 
# python -m spacy train training/configs/config_big.cfg --output ./models/syneda_big

deactivate
echo -e "[INFO:] DONE!"