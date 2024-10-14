from requests import get, Response
from xml.etree import ElementTree
import pandas as pd
import json
import os
import re

def makeSampleInfo(sampleSheet:str="config/samples.csv") -> dict:

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
    directory = "resources/reads/" if includeDirectories else ""
    filePaths = []
    with open("config/samples.json", "r") as file:
        data = json.load(file)
        for type in data:
            for gsm, values in data[type].items():
                filePaths.append(f"{directory}{data[type][gsm]["cleanFileName"]}_1.fastq")
                filePaths.append(f"{directory}{data[type][gsm]["cleanFileName"]}_2.fastq")
    return filePaths


def getSraAccessions(geoAccessions: list[str]) -> dict[str:str]:
    '''
        Given a list of GEO accessions retrieve their related SRA accessions 
    '''
    enterezUrl: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term="
    enterezUrl += "+OR+".join(geoAccessions)

    ### Handle 5** and 4** status codes
    response: Response = get(enterezUrl, timeout=5)
    xmlResponse: ElementTree.Element = ElementTree.fromstring(response.content)
    #idList: list[str] = []
    idList = list(filter(lambda item: int(item) > 299999999, [id.text for id in xmlResponse[3]]))
    enterezUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id=" + ",".join(idList)
    response = get(enterezUrl, timeout=5)
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
    '''
        Fetch metadata for SRA samples 
    '''
    runAccessions: list[str] = []
    enterezUrl: str = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id={",".join(sraAccessions)}"
    response: Response = get(enterezUrl, timeout=5)
    root: ElementTree.Element = ElementTree.fromstring(response.content)
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

def getFileNames(includeProvided: bool = True, includePubliclyAvailiable: bool = True) -> list[str]:
    """
        Returns a list of file names 
    """
    if not includeProvided and not includePubliclyAvailiable:
        return list()

    if not os.path.isfile("config/samples.json"):
        makeSampleInfo()
    #makeSampleInfo()
    with open("config/samples.json", "r") as file:
        fileInfo = json.load(file)
        publicFiles = []
        providedFiles = []
        if includePubliclyAvailiable:
            publicFiles = list(map(lambda item: item["cleanFileName"], fileInfo["public"].values()))
        if includeProvided:
            providedFiles = list(map(lambda item: item["cleanFileName"], fileInfo["private"].values()))
    return publicFiles + providedFiles


def __makeCleanFileName(title: str) -> str:
    for old, new in [(" ", ""), (":", "_"), ("+", "_"), (",", "_"), (";", "_")]:
        title = title.replace(old, new)
    return title



if __name__ == "__main__":
    #print(getAllFileNames())
    #makeSampleInfo()
    print(getFileNames(includeProvided=True, includePubliclyAvailiable=True))
    #getGEOMetadata(["GSM1871972", "GSM1871973", "GSM1871976", "GSM1871977"])