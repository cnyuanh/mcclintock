import os
import sys
import subprocess
from Bio import SeqIO
import traceback
try:
    sys.path.append(snakemake.config['args']['mcc_path'])
    import scripts.mccutils as mccutils
    import scripts.fix_fasta as fix_fasta
except Exception as e:
    track = traceback.format_exc()
    print(track, file=sys.stderr)
    print("ERROR...unable to locate required external scripts at: "+snakemake.config['args']['mcc_path']+"/scripts/", file=sys.stderr)
    sys.exit(1)


def main():
    te_gff = snakemake.input.te_gff
    taxonomy = snakemake.input.taxonomy
    consensus = snakemake.input.consensus
    mcc_out = snakemake.params.mcc_out
    run_id = snakemake.params.run_id
    log = snakemake.params.log
    augment = snakemake.params.augment
    chromosomes = snakemake.params.chromosomes.split(",")
    popoolationte_taxonomy = snakemake.output.taxonomy
    popoolationte_te_gff = snakemake.output.te_gff

    mccutils.log("processing", "making popoolationTE annotation files")
    taxonomy = make_popoolationTE_taxonomy(taxonomy, consensus, run_id, mcc_out)

    mccutils.run_command(["cp", te_gff, popoolationte_te_gff])
    mccutils.run_command(["cp", taxonomy, popoolationte_taxonomy])
    mccutils.log("processing", "popoolationTE annotation files created")

def make_popoolationTE_taxonomy(taxonomy, consensus, run_id, out):
    te_families = []
    popoolationTE_taxonomy = out+"/tmp/"+run_id+"tmppopoolationtetaxonomy.tsv"

    with open(taxonomy, "r") as intsv:
        for line in intsv:
            split_line = line.split("\t")
            te_families.append([split_line[0], split_line[1].replace("\n","")])
    
    fasta_records = SeqIO.parse(consensus,"fasta")

    for record in fasta_records:
        element = str(record.id)
        te_families.append([element, element])
    
    with open(popoolationTE_taxonomy, "w") as outtsv:
        header = "\t".join(["insert","id","family","superfamily","suborder","order","class","problem\n"])
        outtsv.write(header)

        for te_fam in te_families:
            element = te_fam[0]
            family = te_fam[1]
            line = "\t".join([element, family, family, family, "na", "na", "na", "0\n"])
            outtsv.write(line)
    
    return popoolationTE_taxonomy

if __name__ == "__main__":
    main()