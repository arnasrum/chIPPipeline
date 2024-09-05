rule trimgalore_pe:
    input:
        "reads/{id}_1.fastq",
        "reads/{id}_2.fastq",
    output:
        temp(["output/trimgalore/{id}_1.fastq", "output/trimgalore/{id}_2.fastq"])
    params:
        outputPath = "output/trimgalore",
        name = f"{{id}}",
        args = config["trimgalore"]["args"]
    shell:
        """
        trim_galore --paired --no_report_file -o {params.outputPath} --basename {params.name} {params.args} {input}
        mv ./{params.outputPath}/{wildcards.id}_val_1.fq ./{params.outputPath}/{wildcards.id}_1.fastq
        mv ./{params.outputPath}/{wildcards.id}_val_2.fq ./{params.outputPath}/{wildcards.id}_2.fastq
        """

rule cutadapt_pe:
    input:
        "reads/{id}_1.fastq",
        "reads/{id}_2.fastq"
    output:
        out1 = temp("output/cutadapt/{id}_1.fastq"),
        out2 = temp("output/cutadapt/{id}_2.fastq")
    params:
        args = config["cutadapt"]["args"]
    shell:
        '''
        cutadapt -o {output.out1} -p {output.out2} {params.args} {input}
        '''

rule fastp_pe:
    input:
        read1 = "reads/{id}_1.fastq",
        read2 = "reads/{id}_2.fastq"
    output:
        out1 = temp("output/fastp/{id}_1.fastq"),
        out2 = temp("output/fastp/{id}_2.fastq")
    params:
        args = config["fastp"]["args"]
    shell:
        '''
        fastp -i {input.read1} -I {input.read2} -o {output.out1} -O {output.out2} {params.args}
        '''
