rule fastqc:
	input:
		"reads/{id}_1.fastq",
		#"reads/{id}_2.fastq",
	output:
		"output/fastqc/{id}.html",
		"output/fastqc/{id}.zip",
	shell:
		"""
		fastqc {input}	
		"""


