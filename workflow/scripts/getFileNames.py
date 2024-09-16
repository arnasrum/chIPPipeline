import pandas as pd
from pysradb import SRAweb

outdir = "resources/reads/"

def getFileNames():
    db = SRAweb()
    fileNames = []
    with open("config/samples.csv", "r") as file:
        table = pd.read_csv(file, header=0)
        for index, run in enumerate(table["run"]):
            runData = db.sra_metadata(run)
            experimentInfo = runData.get("experiment_title")[0]
            libraryLayout = runData.get("library_layout")[0]
            for symbol in [": ", "; ", ".", " "]:
                experimentInfo = experimentInfo.replace(symbol, "_")
            fileName = f"{run}_{experimentInfo}"
            if libraryLayout == "PAIRED":
                fileNames.append((f"{outdir}{fileName}_1.fastq", f"{outdir}{fileName}_2.fastq"))
            else:
                fileNames.append((f"{outdir}{fileName}.fastq"))
    return fileNames
