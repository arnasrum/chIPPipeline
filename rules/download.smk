import pandas as pd
from pysradb import SRAweb



def getFileNames():
    db = SRAweb()
    fileNames = []
    with open("./config/samples.csv", "r") as file:
        table = pd.read_csv(file, header=0)
        for index, run in enumerate(table["run"]):
            runData = db.sra_metadata(run)
            experimentInfo = runData.get("experiment_title")[0]
            libraryLayout = runData.get("library_layout")[0]
            experimentInfo = experimentInfo.replace(": ", "_")
            experimentInfo = experimentInfo.replace("; ", "_")
            experimentInfo = experimentInfo.replace(".", "-")
            experimentInfo = experimentInfo.replace(" ", "_")
            # Add format and if paired            
            fileNames.append(f"{run}_{experimentInfo}")
            fileName = f"reads/{run}_{experimentInfo}"
            if libraryLayout == "PAIRED":
                fileNames.append(f"{fileName}_1.fastq")
                fileNames.append(f"{fileName}_2.fastq")
            else:
                fileNames.append(f"{fileName}.fastq")
    return fileNames

for fileName in getFileNames():
    rule:
        input:
            "config/samples.csv"
        output:
            fileName 
        run:
            accession = fileName.split("/")[1]
            accession = accession.split("_")[0]
            shell(f"fasterq-dump -p -o {fileName} {accession}")
