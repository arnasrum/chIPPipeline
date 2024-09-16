trimmer = config["alignment"]["trimmer"]

rule bowtie2:
    input:
        [f"results/{trimmer}/{{id}}_1.fastq", f"results/{trimmer}/{{id}}_2.fastq"]
    output:
        "results/bowtie2/{id}.bam"
    params:
    threads:
        2
    shell:
        '''
        touch results/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        '''

