trimmer = config["trimmer"]


rule buildBowtie2Index:
    input:
        f"resources/genomes/{config["genome"]}.fa.gz"
    output:
        expand("results/bowtie2-build/{genome}.{extension}", 
                extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], 
                genome=[config["genome"]])
    params:
        genome = config["genome"],
        args = config["bowtie2"]["args"]
    shell:
        '''
        bowtie2-build {params.args} {input} results/bowtie2-build/{params.genome}
        '''

rule bowtie2:
    input:
        expand("results/bowtie2-build/{genome}.{extension}", extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], genome=config["genome"]),
        input1 = f"results/{trimmer}/{{id}}_1.fastq", 
        input2 = f"results/{trimmer}/{{id}}_2.fastq"
    output:
        "results/bowtie2/{id}.bam"
    params:
        args = config["bowtie2"]["args"],
        genome = config["genome"]
    shell:
        '''
        bowtie2 -x results/bowtie2-build/{params.genome} -1 {input.input1} -2 {input.input2}
        '''