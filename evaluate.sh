#!/bin/bash

source env/bin/activate

## SYNEDA MODEL ## 
# evaluate SYNEDA
echo -e "[INFO:] INTIALISING EVALUATION"
python -m spacy benchmark accuracy training/models/syneda/model-best data/test/SYNEDA_test.spacy --output results/SYNEDA/results_on_SYNEDA.json 

# evaluate DANE
python -m spacy benchmark accuracy training/models/syneda/model-best data/test/DANE_test.spacy --output results/SYNEDA/results_on_DANE.json

# evaluate DANSK 
python -m spacy benchmark accuracy training/models/syneda/model-best data/test/DANSK_test.spacy --output results/SYNEDA/results_on_DANSK.json

echo -e "[INFO:] DONE!"
deactivate