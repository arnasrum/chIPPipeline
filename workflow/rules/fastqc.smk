rule fastqc:
	input:
		"reads/{id}.fastq",
	output:
		"output/fastqc/{id}_fastqc.html",
		"output/fastqc/{id}_fastqc.zip",
	params:
		outputPath = "output/fastqc"
	shell:
		"""
		fastqc -o {params.outputPath} {input} 
		"""


