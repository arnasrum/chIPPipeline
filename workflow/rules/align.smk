genome = config["genome"]
trimmer = config["trimmer"]


rule buildBowtie2Index:
    input:
        f"resources/genomes/{genome}.fa.gz"
    output:
        expand("results/bowtie2-build/{genome}.{extension}", extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], genome=[config["genome"]])
    params:
        args = config["bowtie2"]["args"]
    shell:
        f"bowtie2-build {params.args} {input} results/bowtie2-build/{genome}"

rule bowtie2:
    input:
        f"results/{trimmer}/{{id}}_1.fastq", 
        f"results/{trimmer}/{{id}}_2.fastq",
        expand("results/bowtie2-build/{genome}.{extension}", extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], genome=config["genome"])
    output:
        "results/bowtie2/{id}.bam"
    params:
        args = config["bowtie2"]["args"]
    shell:
        '''
        touch results/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        '''

