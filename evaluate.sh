#!/bin/bash

source env/bin/activate

echo -e "[INFO:] INTIALISING EVALUATION"
## SYNEDA MODEL ## 
# evaluate SYNEDA
python -m spacy benchmark accuracy training/models/SYNEDA/model-best data/test/SYNEDA_test.spacy --output results/SYNEDA/results_on_SYNEDA.json 

# evaluate DANE
python -m spacy benchmark accuracy training/models/SYNEDA/model-best data/test/DANE_test.spacy --output results/SYNEDA/results_on_DANE.json

# evaluate DANSK 
python -m spacy benchmark accuracy training/models/SYNEDA/model-best data/test/DANSK_test.spacy --output results/SYNEDA/results_on_DANSK.json

## SYNEDA_DANSK MODEL ## 
# evaluate SYNEDA
python -m spacy benchmark accuracy training/models/SYNEDA_DANSK/model-best data/test/SYNEDA_test.spacy --output results/SYNEDA_DANSK/results_on_SYNEDA.json 

# evaluate DANE
python -m spacy benchmark accuracy training/models/SYNEDA_DANSK/model-best data/test/DANE_test.spacy --output results/SYNEDA_DANSK/results_on_DANE.json

# evaluate DANSK 
python -m spacy benchmark accuracy training/models/SYNEDA_DANSK/model-best data/test/DANSK_test.spacy --output results/SYNEDA_DANSK/results_on_DANSK.json


echo -e "[INFO:] DONE!"
deactivate