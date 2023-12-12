#!/bin/bash

source env/bin/activate

# evaluate spacy
echo -e "[INFO:] INTIALISING EVALUATION"
python -m spacy benchmark accuracy models/syneda_small/model-best data/spacy_formats/train.spacy --output results/syneda_small/SYNEDA_results.json 

echo -e "[INFO:] DONE!"
deactivate