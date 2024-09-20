#genome = config["genome"]
#trimmer = config["trimmer"]
genome = "mm39" 
trimmer = "trimgalore" 



rule bowtie2:
    input:
        f"results/{trimmer}/{{id}}_1.fastq", 
        f"results/{trimmer}/{{id}}_2.fastq",
        f"resources/genomes/{genome}.fa.gz"
    output:
        "results/bowtie2/{id}.bam"
    params:
    shell:
        '''
        touch results/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        '''

