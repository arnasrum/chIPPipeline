ext=[".fastq.gz", ".fastq", ".fq", ".fq.gz"]
pathToInput = f"resources/reads"

rule trimgalore_pe:
    input:
        "resources/reads/{id}_1.fastq",  
        "resources/reads/{id}_2.fastq"
    params:
        name = f"{{id}}",
        args = config["trimgalore"]["args"],
    output:
        temp([f"results/trimgalore/{{id}}_1.fastq", f"results/trimagalore/{{id}}_2.fastq"])
    shell:
        """
        trim_galore --paired --no_report_file -o results/trimgalore --basename {params.name} {params.args} {input}
        mv results/trimgalore/{wildcards.id}_val_1.fq results/trimgalore/{wildcards.id}_1.fastq
        mv results/trimgalore/{wildcards.id}_val_2.fq results/trimgalore/{wildcards.id}_2.fastq
        """

rule cutadapt_pe:
    input:
        "resources/reads/{id}_1.fastq",
        "resources/reads/{id}_2.fastq"
    output:
        out1 = temp("results/cutadapt/{id}_1.fastq"),
        out2 = temp("results/cutadapt/{id}_2.fastq")
    params:
        args = config["cutadapt"]["args"]
    shell:
        '''
        cutadapt -o {output.out1} -p {output.out2} {params.args} {input}
        '''

rule fastp_pe:
    input:
        read1 = "resources/reads/{id}_1.fastq",
        read2 = "resources/reads/{id}_2.fastq"
    output:
        out1 = temp("results/fastp/{id}_1.fastq"),
        out2 = temp("results/fastp/{id}_2.fastq")
    params:
        args = config["fastp"]["args"]
    shell:
        '''
        fastp -j results/fastp/fastp.json -h results/fastp/fastp.html -i {input.read1} -I {input.read2} -o {output.out1} -O {output.out2} {params.args}
        '''
