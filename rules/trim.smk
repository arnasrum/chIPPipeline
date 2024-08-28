rule trimgalore_pe:
	input:
		"reads/{id}_1.fastq",
		"reads/{id}_2.fastq",
	output:
		"output/trimgalore/{id}_val_1.fq",
		"output/trimgalore/{id}_val_2.fq",
	params:
		outputPath = "output/trimgalore",
		name = f"{{id}}"
	shell:
		"""
		trim_galore --paired --no_report_file -o {params.outputPath} --basename {params.name} {input} 
		"""
