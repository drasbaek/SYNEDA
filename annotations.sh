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
    "date.py"
    "person.py"
    "quantity.py"
)

echo "Running all scripts within $SCRIPTS_DIR"

# execute all scripts 
for script in "${SCRIPTS[@]}"; do
    python "$SCRIPTS_DIR/$script"
done

# deactivate env
deactivate