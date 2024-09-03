from pysradb import SRAweb
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def getaccessionsGSMtoSRR(filename="input.txt", write_to_file=False):
    db = SRAweb()
    srr_accessions = []
    with open(filename) as file:
        for line in file.readlines():
            accession = db.gsm_to_srr(line)
            print(line)
            info = db.sra_metadata(line)
            sra_accession = info.get("run_accession")
            sra_info = info.get("experiment_title")[0]
            sra_info = sra_info.replace(": ", "_")
            sra_info = sra_info.replace("; ", "_")
            sra_info = sra_info.replace(".", "-")
            sra_info = sra_info.replace(" ", "_")
        with open("accessions.txt", "w") as writefile:
            for sra in sra_accession.values:
                result = f"{sra}_{sra_info}"
                srr_accessions.append([sra, result])
                if write_to_file:
                    writefile.write(f"{sra} {result}\n")
    return srr_accessions

if __name__=="__main__":
    print(getaccessionsGSMtoSRR(filename="query.txt"))
