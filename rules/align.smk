
#configfile: "config/config.yml"
rule bowtie2:
    input:
        #expand(["output/{trimmer}/{{id}}_1.fastq", "output/{trimmer}/{{id}}_2.fastq"], trimmer=TRIMMERS)
        [f"output/{config["bowtie2"]["trimmer"]}/{{id}}_1.fastq", f"output/{config["bowtie2"]["trimmer"]}/{{id}}_2.fastq"]
    output:
        temp("output/bowtie2/{id}.bam")
    threads:
        2
    shell:
        '''
        touch output/bowtie2/{wildcards.id}.bam
        echo 'this should work' 
        '''

