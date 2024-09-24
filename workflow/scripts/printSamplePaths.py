from sampleFileScripts import parseSampleFile
from sampleFileScripts import gsmToSrrMap, gsmDB
import numpy as np

if __name__ == "__main__":

    gsmMap = gsmDB() 
    for gsm, values in gsmMap.items():
        print(gsm)
        print(values["runs"])
        print(values["cleanFileName"])
    #print(gsmMap.values())
    #print([items["runs"] for items in gsmMap.values()])
    #print(" ".join(list(map(lambda srr: f"resources/reads/{srr}_1.fastq", gsmMap["GSM1871964"]))))
    #print(np.array(list(gsmMap.values())).flatten())
    #for gsm, runs in gsmMap.items():
        #print([f"resources/reads/{run}_1.fastq" f"resources/reads/{run}_2.fastq" for run in runs])
