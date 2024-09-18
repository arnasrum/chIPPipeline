import sys
import pandas as pd
sys.path.append("./workflow/scripts")
from sampleFileScripts import parseSampleFile

outdir = "resources/reads"

def unpack(files, outdir):
    if len(files) == 1:
        return [f"{outdir}/{files[0]}"]
    if len(files) == 2:
        return [f"{outdir}/{files[0]}", f"{outdir}/{files[1]}"]

for fileInfo in parseSampleFile():
    rule:
        output:
            unpack(fileInfo["outputFiles"], outdir)
        params:
            args = config["fasterq-dump"]["args"],
            accession = fileInfo["accession"],
            fileName = fileInfo["fileName"]
        shell:
            '''
            fasterq-dump -t temp -p -O {outdir} -o {params.args} {params.fileName} {params.accession}
            '''
