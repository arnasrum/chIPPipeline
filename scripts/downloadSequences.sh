#!/bin/bash

file_name="accessions.txt"
IFS=' '

python3 getaccessions.py

while read -r line; do
    echo "$line"
    IFS=' ' read -ra options <<< "$line"
    #echo ${options[1]}
    fasterq-dump ${options[0]} -o ${options[1]} -p 
done < "accessions.txt"
