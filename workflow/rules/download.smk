import sys
sys.path.append("workflow/scripts")
import pandas as pd
import numpy as np
from sampleFileScripts import fetchGEOInfo 





gsmMap = fetchGEOInfo()
for srr in [run for value in gsmMap.values() for run in value["runs"]]:
    rule:
        output:
            f"resources/reads/{srr}_1.fastq",
            f"resources/reads/{srr}_2.fastq"
        params:
            srr = srr
        shell:
            '''
            fasterq-dump -t temp -O resources/reads -p {params.srr}
            '''


for gsm, values in gsmMap.items():
    rule:
        input:
            expand("resources/reads/{run}_{readNum}.fastq", run=values["runs"], readNum=[1, 2])
        output:
            f"resources/reads/{values["cleanFileName"]}_1.fastq",
            f"resources/reads/{values["cleanFileName"]}_2.fastq"
        params:
            outdir = "resources/reads",
            read1Files = " ".join(list(map(lambda run: f"resources/reads/{run}_1.fastq", values["runs"]))),
            read2Files = " ".join(list(map(lambda run: f"resources/reads/{run}_2.fastq", values["runs"]))),
            outputName = values["cleanFileName"] 
        shell:
            """
            cat {params.read1Files} > {params.outdir}/{params.outputName}_1.fastq
            cat {params.read2Files} > {params.outdir}/{params.outputName}_2.fastq
            """

rule downloadReferenceGenome:
    output:
        "resources/genomes/{genome}.fa.gz"
    benchmark:
        "benchmarks/rsync/{genome}.benchmark.txt"
    shell:
        '''
        rsync -a -P rsync://hgdownload.soe.ucsc.edu/goldenPath/{wildcards.genome}/bigZips/{wildcards.genome}.fa.gz resources/genomes/
        '''