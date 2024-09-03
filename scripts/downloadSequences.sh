#!/bin/bash

file_name="accessions.txt"
IFS=' '

while read -r line; do
    #echo "$line"
    IFS=' ' read -ra options <<< "$line"
    #echo ${options[1]}
    fasterq-dump ${options[0]} -o ${options[1]} -p 
done < "accessions.txt"
