# About

Snakemake chromatin immunoprecipitation sequencing data analysis pipeline. 

The pipeline contains several steps like; downloading samples, quality control, trimming, aligning, etc. 

For each step a rule can be run to execute it. Prerequisite rules are ran if the called rule is missing input files. For example running the alignment rule trigger downloading and trimming rules. 

Each data analysis step can have multiple interchangable tools. Tools are chosen in the configuration file. More conviently the configuration file arguments can be overriden with the "--config" flag when running snakemake. This allows the user to choose tools from the CLI without changing the default configuration of the pipeline. 

`snakemake --config trimmer=cutadapt -np align`

# Usage

Use 

`snakemake --list`

to get at list of all available rules. 

The main rules do not have any prefixes, like **align** and **trim**, these can be ran by calling 

`snakemake -np RULENAME `
