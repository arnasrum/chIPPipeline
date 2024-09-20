genome = config["genome"]
trimmer = config["trimmer"]


rule buildBowtie2Index:
    input:
        f"resources/genomes/{genome}.fa.gz"
    output:
        expand(f"results/bowtie2-build/index.{extension}", extension=["1.bt2l", "2.bt2l", "3.bt2l", "4.bt2l"])
    shell:
        '''
        bowtie2-build {input} results/bowtie2-build 
        '''

rule bowtie2:
    input:
        f"results/{trimmer}/{{id}}_1.fastq", 
        f"results/{trimmer}/{{id}}_2.fastq",
        expand(f"results/bowtie2-build/index.{extension}", extension=["1.bt2l", "2.bt2l", "3.bt2l", "4.bt2l"])
    output:
        "results/bowtie2/{id}.bam"
    params:
        args = config["bowtie2"]["args"]
    shell:
        '''
        touch results/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        bowtie2 -1 -2
        '''

