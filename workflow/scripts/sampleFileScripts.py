from requests import get, Response
import pandas as pd
from xml.etree import ElementTree
import re
import json
import os

def fetchGEOInfo(sampleSheet:str="config/samples.csv") -> dict:

    #if os.path.isfile("config/samples.json"):
        #with open("config/samples.json", "r") as file:
            #return json.load(file)

    pattern = re.compile(r"^GSM[0-9]*$")
    inputSamples = set()
    with open(sampleSheet, "r") as file:
        for index, row in pd.read_csv(file).iterrows():
            for gsm in row.values[2:]:
                inputSamples.add(gsm)
    sampleInfo = {}
    sampleInfo["public"] = {}; sampleInfo["private"] = {}
    #inputSamples.add("GSM7744846")
    gsmAccessions = set()

    for gsm in inputSamples:
        if pattern.match(gsm):
            gsmAccessions.add(gsm)
        else:
            fileName = gsm.split("/")[-1]
            sampleInfo["private"][fileName] = {}
            sampleInfo["private"][fileName]["path"] = gsm
            sampleInfo["private"][fileName]["cleanFileName"] = fileName.split(".")[0]
    for key,value in getMetaData(getSraAccessions(gsmAccessions).values()).items():
        sampleInfo["public"][key] = value 

    with open(f"config/samples.json", "w") as outfile:
        outfile.write(json.dumps(sampleInfo, indent=4))
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


def getSraAccessions(geoAccessions: list[str]) -> dict[str:str]:
    enterezUrl: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term="
    enterezUrl += "+OR+".join(geoAccessions)
    response: Response = get(enterezUrl)
    xmlResponse: ElementTree.Element = ElementTree.fromstring(response.content)
    idList: list[str] = []
    for id in xmlResponse[3]:
        idList.append(id.text)
    idList = list(filter(lambda item: int(item) > 299999999, idList))
    enterezUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id=" + ",".join(idList)
    response = get(enterezUrl)
    responseText: str = response.content.decode().lstrip("\n").rstrip("\n")
    gsmToSraMap: dict[str:str] = {} 
    prevEnd: int = 0
    for match in re.finditer(r"\n\n", responseText):
        subResponse: str = responseText[prevEnd: match.span()[1]]
        accessionPosition: re.Match = re.search(r"Accession:\sGSM[0-9]*", subResponse)
        sraAccessionPosition: re.Match = re.search(r"(?i)SRA Run Selector:\shttps?:\/\/www.[a-z.\/]*[a-z\/\?=0-9]*", subResponse)
        accession: str = subResponse[accessionPosition.span()[0]: accessionPosition.span()[1]].split(": ")[1]
        sraAccession: str = subResponse[sraAccessionPosition.span()[0]: sraAccessionPosition.span()[1]].split("acc=")[1]
        gsmToSraMap[accession] = sraAccession
        prevEnd = match.span()[1]
    return gsmToSraMap

def getMetaData(sraAccessions: list[str]) -> dict[str: dict]: 
    runAccessions: list[str] = []
    enterezUrl: str = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id={",".join(sraAccessions)}"
    result: Response = get(enterezUrl)
    root: ElementTree.Element = ElementTree.fromstring(result.content)
    metaData: dict[str: dict] = {}
    for node in root:
        runAccessions: list[str] = []
        geoAccession = node[4].attrib["alias"]
        metaData[geoAccession] = {"cleanFileName": __makeCleanFileName(node[0][1].text)}
        for run in node[6]:
            runAccessions.append(run.attrib["accession"])
        metaData[geoAccession]["runs"] = runAccessions
    #response = xmltodict.parse(result.content)
    return metaData

def __makeCleanFileName(title: str) -> str:
    for old, new in [(" ", ""), (":", "_"), ("+", "_"), (",", "_"), (";", "_")]:
        title = title.replace(old, new)
    return title



if __name__ == "__main__":
    fetchGEOInfo()
    #getGEOMetadata(["GSM1871972", "GSM1871973", "GSM1871976", "GSM1871977"])