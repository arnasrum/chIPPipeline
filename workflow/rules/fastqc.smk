

rule fastqc:
	input:
		f"{config["path_to_reads"]}/{{id}}.fastq",
	output:
		"results/fastqc/{id}_fastqc.html",
		"results/fastqc/{id}_fastqc.zip",
	params:
		outputPath = "results/fastqc"
	shell:
		"""
		fastqc -o {params.outputPath} {input} 
		"""


