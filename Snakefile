configfile: "config/config.yml"

include: "rules/fastqc.smk"
include: "rules/trim.smk"
include: "rules/align.smk"
#include: "rules/download.smk"
