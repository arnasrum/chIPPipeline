import pandas as pd
from pysradb import SRAweb
import csv


def getFileNames():
    outdir = "resources/reads/"
    fileNames = []
    with open("config/runFilenames.csv", "r") as file:
        table = pd.read_csv(file)
        for index, row in table.iterrows():
            fileName = row["filename"]
            libraryLayout = row["libraryLayout"]
            if libraryLayout == "PAIRED":
                fileNames.append((f"{outdir}{fileName}_1.fastq", f"{outdir}{fileName}_2.fastq"))
            else:
                fileNames.append((f"{outdir}{fileName}.fastq"))
    return fileNames

def fetchSampleData():
    db = SRAweb()
    try:
        accessionInfo = []
        with open("config/samples.csv", "r") as file:
            table = pd.read_csv(file, header=0)
            for accession in table["run"]:
                print(accession)
                accessionData = db.sra_metadata(accession)
                # The data is the same in all column so just take the first one
                info = accessionData.get("experiment_title")[0]
                libraryLayout = accessionData.get("library_layout")[0]
                for symbol, replacement in [(": ", "_"), ("; ", "_"), (".", "_"), (" ", "_")]:
                    info = info.replace(symbol, replacement)
                accessionInfo.append([accession, f"{accession}_{info}", libraryLayout])
        with open("config/runFilenames.csv", "w") as writefile:
            writer = csv.writer(writefile)
            writer.writerow(["run", "filename", "libraryLayout"])
            for row in accessionInfo:
                writer.writerow(row)
    except FileNotFoundError:
        raise FileNotFoundError("Missing samples.csv file located in config folder. Try adding a samples.csv with a column for desired SRR accessions")

if __name__ == "__main__":
    #fetchSampleData()
    print(getFileNames())