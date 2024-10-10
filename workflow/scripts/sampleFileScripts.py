import requests
import pandas as pd
from xml.etree import ElementTree
from pysradb import SRAweb
import GEOparse
import re
import json
import os

def fetchGEOInfo(sampleSheet="config/samples.csv") -> dict:

    if os.path.isfile("config/samples.json"):
        with open("config/samples.json", "r") as file:
            return json.load(file)

    pattern = re.compile(r"^GSM[0-9]*$")
    sraDatabase = SRAweb()
    gsm_accessions = set()
    with open(sampleSheet, "r") as file:
        for index, row in pd.read_csv(file).iterrows():
            for gsm in row.values[2:]:
                gsm_accessions.add(gsm)
    sampleInfo = {}
    sampleInfo["public"] = {}
    sampleInfo["private"] = {}
    for gsm in gsm_accessions:
        if pattern.match(gsm):
            sampleInfo["public"][gsm] = {}
            print(gsm)
            gsmData = GEOparse.get_GEO(geo=gsm, destdir="./temp")
            #print(gsmData.metadata.keys())
            sraAccession = re.findall(r"SRX[0-9]*", gsmData.metadata["relation"][1])[0]
            sampleInfo["public"][gsm]["runs"] = [run for run in getRunsFromSraAccession(sraAccession)]
            srr = sampleInfo["public"][gsm]["runs"][0]
            #cleanTitle = sraDatabase.sra_metadata(srr)["experiment_title"][0]
            cleanTitle = gsm 
            for symbol, replacement in [(": ", "_"), ("; ", "_"), (".", "_"), (" ", "_")]:
                cleanTitle = cleanTitle.replace(symbol, replacement)
            sampleInfo["public"][gsm]["cleanFileName"] = cleanTitle
        else:
            fileName = gsm.split("/")[-1]
            sampleInfo["private"][fileName] = {}
            sampleInfo["private"][fileName]["path"] = gsm
            sampleInfo["private"][fileName]["cleanFileName"] = fileName.split(".")[0]

    #with open(f"config/samples.json", "w") as outfile:
        #outfile.write(json.dumps(sampleInfo, indent=4))
    return sampleInfo

def getAllSampleFilePaths(includeDirectories=True) -> list:
    if includeDirectories:
        directory = "resources/reads/"
    else:
        directory = ""
    filePaths = []
    with open("config/samples.json", "r") as file:
        data = json.load(file)
        for gsm, values in data["public"].items():
            filePaths.append(f"{directory}{data["public"][gsm]["cleanFileName"]}_1.fastq")
            filePaths.append(f"{directory}{data["public"][gsm]["cleanFileName"]}_2.fastq")
    return filePaths

def getRunsFromSraAccession(bioSample: str) -> list: 
    runAccessions = []
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id={bioSample}"
    result = requests.get(url)
    tree = ElementTree.fromstring(result.content)
    for node in tree[0][6]:
        runAccessions.append(node.attrib["accession"])
    #response = xmltodict.parse(result.content)
    return runAccessions

if __name__ == "__main__":
    fetchGEOInfo()