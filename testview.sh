#!/bin/bash

# Function to print a horizontal line the width of the terminal
function viivo() {
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}

# Check if a directory was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Assign the provided directory to a variable
splitdir="$@"

# Check if the directory exists
if [[ ! -d "$splitdir" ]]; then
    echo "::: [ERROR!] Directory not found: $splitdir"
    exit 1
fi

# Navigate to the directory and display the contents of each text file
cd "$splitdir" || exit
for i in *.txt; do
    viivo
    echo "Segment: $i"
    viivo
    cat "$i"
    echo
done
viivo
