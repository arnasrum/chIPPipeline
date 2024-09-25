import pandas as pd
from pysradb import SRAweb
import json
import os

def fetchGEOInfo():

    if os.path.isfile("config/samples.json"):
        with open("config/samples.json", "r") as file:
            return json.load(file)

    sraDatabase = SRAweb()
    gsm_accessions = set()
    with open("config/input.csv", "r") as file:
        for index, row in pd.read_csv(file).iterrows():
            for gsm in row.values[:4]:
                gsm_accessions.add(gsm)
    gsmToSRR = {}
    for gsm in gsm_accessions:
        gsmToSRR[gsm] = {}
        gsmToSRR[gsm]["runs"] = [run for run in sraDatabase.gsm_to_srr(gsm)["run_accession"]]
        srr = gsmToSRR[gsm]["runs"][0]
        cleanTitle = sraDatabase.sra_metadata(srr)["experiment_title"][0]
        for symbol, replacement in [(": ", "_"), ("; ", "_"), (".", "_"), (" ", "_")]:
            cleanTitle = cleanTitle.replace(symbol, replacement)
        gsmToSRR[gsm]["cleanFileName"] = cleanTitle

    with open(f"config/samples.json", "w") as outfile:
        outfile.write(json.dumps(gsmToSRR, indent=4))
    return gsmToSRR

def getAllSampleFilePaths(includeDirectories=True):
    if includeDirectories:
        directory = "resources/reads/"
    else:
        directory = ""
    filePaths = []
    with open("config/samples.json", "r") as file:
        data = json.load(file)
        for gsm, values in data.items():
            filePaths.append(f"{directory}{data[gsm]["cleanFileName"]}_1.fastq")
            filePaths.append(f"{directory}{data[gsm]["cleanFileName"]}_2.fastq")
    return filePaths
if __name__ == "__main__":
    fetchGEOInfo()