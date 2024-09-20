import sys
sys.path.append("workflow/scripts")
import pandas as pd
from sampleFileScripts import parseSampleFile

for fileInfo in parseSampleFile():
    rule:
        output:
            *fileInfo["outputFiles"]
        params:
            args = config["fasterq-dump"]["args"],
            outdir = config["fasterq-dump"]["downloadPath"],
            accession = fileInfo["accession"],
            fileName = fileInfo["fileName"]
        shell:
            '''
            fasterq-dump -t temp -p -O {params.outdir} -o {params.fileName} {params.args} {params.accession}
            '''

rule downloadReferenceGenome:
    output:
        "resources/genomes/{genome}.fa.gz"
    shell:
        '''
        rsync -a -P rsync://hgdownload.soe.ucsc.edu/goldenPath/{wildcards.genome}/bigZips/{wildcards.genome}.fa.gz resources/genomes/
        '''