#rsync -a -P rsync://hgdownload.soe.ucsc.edu/goldenPath/{genome}/bigZips/{genome}.fa.gz resources/genomes/
#wget https://hgdownload.soe.ucsc.edu/goldenPath/{genome}/bigZips/{genome}.fa.gz -o resources/genomes/{genome}.fa.gz
import sys
sys.path.append("workflow/scripts")
import pandas as pd
from sampleFileScripts import parseSampleFile

def unpack(files, outdir="resources/reads"):
    if len(files) == 1:
        return [f"{outdir}/{files[0]}"]
    if len(files) == 2:
        return [f"{outdir}/{files[0]}", f"{outdir}/{files[1]}"]

for fileInfo in parseSampleFile():
    rule:
        output:
            unpack(fileInfo["outputFiles"])
        params:
            args = config["fasterq-dump"]["args"],
            outdir = config["fasterq-dump"]["downloadPath"],
            accession = fileInfo["accession"],
            fileName = fileInfo["fileName"]
        shell:
            '''
            fasterq-dump -t temp -p -O {params.outdir} -o {params.fileName} {params.accession}
            '''

rule downloadReferenceGenome:
    output:
        "resources/genomes/{genome}.fa.gz"
    shell:
        '''
        rsync -a -P rsync://hgdownload.soe.ucsc.edu/goldenPath/{genome}/bigZips/{genome}.fa.gz resources/genomes/
        '''