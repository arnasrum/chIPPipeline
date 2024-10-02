
rule MACS2:
    output:
        "test.txt"
    conda:
        "../envs/macs2.yml"
    shell:
        '''
        macs3 --help > test.txt
        '''