#!/bin/bash

## SCRIPT TO CREATE LISTS OF ENTITIES WITHIN ENTITIES LIST (EXCEPT MANUAL LISTS)

# activate env
source env/bin/activate

# define scripts dir 
SCRIPTS_DIR="src/annotations"

# scripts to run
SCRIPTS=(
    "money.py"
    "percent.py"
    #"date.py"
    "person.py"
    "quantity.py"
)

# run scripts
echo "[INFO:] Running all scripts within $SCRIPTS_DIR"
for script in "${SCRIPTS[@]}"; do
    python "$SCRIPTS_DIR/$script"
done

# exectute the generate annotations script
echo "[INFO:] Creating the anotation lists ..."
python "$SCRIPTS_DIR/create_annotations.py"

# deactivate env
deactivate