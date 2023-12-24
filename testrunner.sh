#!/bin/bash

# horizontal term width line
function viivo() {
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
}

export splitdir="2021.4.rocklobster-splits"

if [[ ! -d "$splitdir" ]]; then
    echo "::: [ERROR!] Directory not found: $splitdir"
    exit 1
fi    

rm -rfv "$splitdir"
python splitter.py 2021.4.rocklobster.txt
cd "$splitdir"
for i in *.txt; do viivo; echo "segment: $i"; viivo; cat $i; done
viivo
