trimmer = config["alignment"]["trimmer"]

rule bowtie2:
    input:
        [f"output/{trimmer}/{{id}}_1.fastq", f"output/{trimmer}/{{id}}_2.fastq"]
    output:
        "output/bowtie2/{id}.bam"
    threads:
        2
    shell:
        '''
        touch output/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        '''

