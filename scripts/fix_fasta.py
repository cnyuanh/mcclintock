import os
import subprocess
import sys
from Bio import SeqIO


def fix_fasta_lines(fasta, length):
    lines = []
    fasta_records = SeqIO.parse(fasta,"fasta")
    for record in fasta_records:
        # print(">"+record.id)
        header = ">"+str(record.id)
        lines.append(header)
        seq = str(record.seq)
        x = 0
        while(x+length < len(seq)):
            # print(seq[x:x+length])
            lines.append(seq[x:x+length])
            x += length

        remainder = (len(seq)) - x
        # print(seq[x:x+remainder])
        lines.append(seq[x:x+remainder])
    
    return lines