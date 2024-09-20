import pandas as pd
from pysradb import SRAweb
import csv
import os


def parseSampleFile():
    '''
        Parses sample.csv file and returns dict for each run id provided
        with accession numbers for the sample runs,
        file names for the files that are going be downloaded,
        and file paths for the desired files
        (for making a download rule for each file convenient)
    '''
    fileData = []
    if not os.path.isfile("config/samples.csv"):
       generateSampleFile()
    outputDirectory = "resources/reads"
    with open("config/samples.csv", "r") as file:
        table = pd.read_csv(file)
        for _, row in table.iterrows():
            accession = row["run"]
            fileName = row["filename"]
            libraryLayout = row["libraryLayout"]
            if libraryLayout == "PAIRED":
                fileData.append({"accession": accession, "fileName": fileName, 
                                  "outputFiles": (f"{outputDirectory}/{fileName}_1.fastq", f"{outputDirectory}/{fileName}_2.fastq")})
            else:
                fileData.append({"accession": accession, "fileName": fileName, "outputFiles": (f"{fileName}.fastq")})
    return fileData

def getAllSampleFilePaths(includeDirectories=True):
    '''
    Parses samples.csv and returns a list with file paths to the sequence files.
    If includeDirectories is false, the function returns only the file names
    '''
    if not os.path.isfile("config/samples.csv"):
        generateSampleFile()
    outputDirectory = "resources/reads/"
    if not includeDirectories:
        outputDirectory = ""
    filePaths = []
    with open("config/samples.csv", "r") as file:
        table = pd.read_csv(file)
        for _, row in table.iterrows():
            fileName = row["filename"]
            libraryLayout = row["libraryLayout"]
            if libraryLayout == "PAIRED":
                filePaths.append(f"{outputDirectory}{fileName}_1.fastq")
                filePaths.append(f"{outputDirectory}{fileName}_2.fastq")
            else:
                filePaths.append(f"{outputDirectory}{fileName}.fastq")
    return filePaths


def generateSampleFile():
    '''
        This function generates samples.csv with the required info to name the output files from fasterq-dump
    '''
    sraDatabase = SRAweb()
    try:
        accessionInfo = []
        with open("config/input.csv", "r") as file:
            table = pd.read_csv(file, header=0)
            for accession in table["run"]:
                accession = accession.rstrip()
                accessionData = sraDatabase.sra_metadata(accession)
                # The data is the same in all column so just take the first one
                info = accessionData.get("experiment_title")[0]
                libraryLayout = accessionData.get("library_layout")[0]
                runAccession = list(filter(lambda run: run == accession, accessionData.get("run_accession")))
                for symbol, replacement in [(": ", "_"), ("; ", "_"), (".", "_"), (" ", "_")]:
                    info = info.replace(symbol, replacement)
                accessionInfo.append([runAccession[0], f"{runAccession[0]}_{info}", libraryLayout])
        with open("config/samples.csv", "w") as writefile:
            writer = csv.writer(writefile)
            writer.writerow(["run", "filename", "libraryLayout"])
            for row in accessionInfo:
                writer.writerow(row)
    except FileNotFoundError:
        raise FileNotFoundError("Missing input.csv file located in config folder. Try adding a input.csv with a column for desired SRR accessions")
