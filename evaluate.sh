#!/bin/bash

source env/bin/activate

source env/bin/activate

echo -e "[INFO:] INITIALIZING EVALUATION"

# models to evaluate
#models=("SYNEDA" "SYNEDA_DANSK", "DANSK")
models=("DANSK")

# datasets to evaluate
datasets=("SYNEDA" "DANE" "DANSK")

for model in "${models[@]}"; do
    for dataset in "${datasets[@]}"; do
        # evaluate
        python -m spacy benchmark accuracy "training/models/$model/model-best" "data/test/${dataset}_test.spacy" --output "results/$model/results_on_$dataset.json"
    done
done

echo -e "[INFO:] DONE!"
deactivate