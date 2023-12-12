#!/bin/bash

source env/bin/activate

## SMALL MODEL ## 
# evaluate SYNEDA
echo -e "[INFO:] INTIALISING EVALUATION"
python -m spacy benchmark accuracy models/syneda_small/model-best data/spacy_formats/test.spacy --output results/syneda_small/SYNEDA_results.json 

# evaluate DANE
python -m spacy benchmark accuracy models/syneda_small/model-best external_data/DANE_test.spacy --output results/syneda_small/DANE_results.json

# evaluate DANSK 
python -m spacy benchmark accuracy models/syneda_small/model-best external_data/DANSK_test.spacy --output results/syneda_small/DANSK_results.json

echo -e "[INFO:] DONE!"
deactivate