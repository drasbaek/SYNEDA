#!/bin/bash

# activate env
source env/bin/activate

# define scripts dir 
SCRIPTS_DIR="src/tags"

# scripts to run
SCRIPTS=(
    "money.py"
    "percent.py"
    "date.py"
    "person.py"
    "quantity.py"
)

echo "Running all scripts within $SCRIPTS_DIR"

# Loop through and execute each script
for script in "${SCRIPTS[@]}"; do
    python "$SCRIPTS_DIR/$script"
done

# Deactivate the virtual environment
deactivate