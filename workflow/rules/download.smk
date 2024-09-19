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
