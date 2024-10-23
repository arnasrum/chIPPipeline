

rule filter_aligned_macs3:
    input:
        f"results/{config["trimmer"]}/{{sample}}.sam"
    output:
        f"results/macs3-filterdup/{sample}.sam" 
    conda:
        "../envs/peakCalling.yml"
    shell:
        """
        macs3 filterdup -f {input} --outdir results/macs3-filterdup -o {wildcards.sample}
        """
    
rule macs3:
    input:
        f"results/macs3-filterdup/{sample}.sam" 
    output:
    shell:
        """
        """