import sys
sys.path.append("./workflow/scripts")

from getFileNames import getFileNames

for outputFiles in getFileNames():
    rule:
        output:
           *outputFiles 
        params:
            args = config["fasterq-dump"]["args"]
        run:
            file = outputFiles[0].split("/")[2][:-8]
            accession = outputFiles[0].split("/")[2].split("_")[0]
            shell(f"fasterq-dump -p -O resources/reads -o {params.args} {file} {accession}")
