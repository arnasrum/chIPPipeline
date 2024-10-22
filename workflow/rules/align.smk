trimmer = config["trimmer"]
aligner = config["aligner"]


rule buildBowtie2Index:
    input:
        f"resources/genomes/{config["genome"]}.fa.gz"
    output:
        expand("results/bowtie2-build/{genome}.{extension}", 
            extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], 
            genome=[config["genome"]]
        )
    params:
        genome = config["genome"],
        args = config["bowtie2"]["args"]
    shell:
        '''
        bowtie2-build {params.args} {input} results/bowtie2-build/{params.genome}
        '''

rule bowtie2_pe:
    input:
        expand("results/bowtie2-build/{genome}.{extension}", 
            extension=["1.bt2", "2.bt2", "3.bt2", "4.bt2"], 
            genome=config["genome"]
        ),
        input1 = f"results/{trimmer}/{{id}}_1.fastq", 
        input2 = f"results/{trimmer}/{{id}}_2.fastq"
    output:
        outputFile = f"results/bowtie2/{{id}}.sam"
    params:
        args = config["bowtie2"]["args"],
        genome = config["genome"],
        outputArgs = f"-S results/bowtie2/{{id}}.sam"
    log:
        "logs/bowtie2/{id}.log"
    shell:
        '''
        bowtie2 -x results/bowtie2-build/{params.genome} -1 {input.input1} -2 {input.input2} -S {output}
        '''


rule buildBWAIndex:
    input:
        f"resources/genomes/{config["genome"]}.fa.gz"
    output: 
        expand("results/bwa-index/{genome}.{ext}", 
            genome=config["genome"], 
            ext=["amb", "ann", "pac", "sa", "bwt"]
        ) 
    params:
        genome = config["genome"],
        args = config["bwa-index"]["args"]
    shell:
        """
        mkdir -p results/bwa-index
        bwa index {params.args} {input} -p results/bwa-index/{params.genome}
        """

rule bwa_pe:
    input:
        read1 = expand("results/{trimmer}/{id}_1.fastq", trimmer=config["trimmer"], allow_missing=True),
        read2 = expand("results/{trimmer}/{id}_2.fastq", trimmer=config["trimmer"], allow_missing=True),
        genomeIndex = expand("results/bwa-index/{genome}.{ext}", 
            genome=config["genome"], 
            ext=["amb", "ann", "pac", "sa", "bwt"]
        ) 
    output:
        "results/bwa/{id}.sam"
    params:
        args = config["bwa"]["args"]
    shell:
        """
        bwa mem {params.args} results/bwa-index/mm39 {input.read1} {input.read2} > {output}
        """


rule buildStarIndex:
    input:
        f"resources/genomes/{config["genome"]}.fa"
    output:
        expand("chr{name}.txt", name=["Length", "Name", "NameLength", "Start"]),
        "Genome",
        "genomeParameters.txt",
        "Log.out",
        "SA"
    params:
        pathToGenome = f"resources/genomes/{config["genome"]}.fa"
    threads:
        8
    shell:
        """
        mkdir -p results/starIndex
        STAR --runThreadN {threads} --runMode genomeGenerate --genomeDir results/starIndex --genomeFastaFiles {params.pathToGenome} 
        """ 


rule filterReads:
    input:
        f"results/{config["aligner"]}/{{id}}.sam"
    output:
        f"results/samtools/{{id}}_filtered.bam"
    params:
        args = config["samtools"],
        aligner = config["aligner"]
    log:
        "logs/samtools/{id}.log"
    shell:
        '''
        if [ ! -d "results/samtools" ]
        then
            mkdir "results/samtools"
        fi
        samtools view {params.args} -b -o {output} {input} 
        '''