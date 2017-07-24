#!/usr/bin/env python

from __future__ import print_function
import argparse
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
import os.path
import vcf
import intervaltree
from operator import itemgetter

difference = lambda x,y: 0 if x == y else 1

string_difference = lambda query, target, query_len: sum((difference(query[i], target[i])) for i in range(query_len))

def fuzzysearch(query, target):
    query_len = len(query)
    target_len = len(target)
    assert query_len <= target_len, "query cannot be longer than target"
    min_distance = string_difference(query, target, query_len)
    best_pos = 0
    for i in range(0, target_len - query_len + 1):
        distance = string_difference(query, target[i:i+query_len], query_len)
        if distance < min_distance:
            (min_distance, best_pos) = (distance, i)
    return best_pos

parser = argparse.ArgumentParser()
parser.add_argument('--vcf_files', nargs="+")
parser.add_argument('--reference_file', type=argparse.FileType())
parser.add_argument('--output_file', type=argparse.FileType('w'))
parser.add_argument('--remove_invariant', action='store_true', default=False)
args = parser.parse_args()

do_inserts = False
do_deletes = False
do_snps = True
if (do_inserts or do_deletes) and args.remove_invariant:
    exit("Cannot combine indel processing with 'remove_invariant' argument")
# reference = str(SeqIO.read(os.path.expanduser("~/Data/fasta/NC_000962.fna"), "fasta").seq)
# print(reference, file=open('/tmp/reference.txt', 'w'))
# vcf_files_dir = os.path.expanduser("~/Data/vcf")
# vcf_files = [os.path.join(vcf_files_dir, "vcf{}.vcf".format(num)) for num in range(1,4)]
# print(vcf_files)
reference_seq  = SeqIO.read(args.reference_file, "fasta")
reference = str(reference_seq.seq)
# output_file = open(os.path.join(os.path.expanduser("~/Data/fasta/vcf_to_msa"), 'output.fasta'), 'w')
insertions = {}
insertion_sites = []
tree = intervaltree.IntervalTree()
sequence_names = []
sequences = {}
if args.remove_invariant:
    variant_sites = set()
for i, vcf_descriptor in enumerate(args.vcf_files):
    # seqname = os.path.splitext(os.path.basename(vcf_filename))[0]
    (seqname,vcf_filename) = vcf_descriptor.split('^^^')
    sequence_names.append(seqname)
    sequence = list(reference)
    sequences[seqname] = sequence
    print(seqname)
    # tsv_filename = vcf_filename.replace(".vcf", ".tsv")
    # output = open(tsv_filename, "wb")
    insertions[seqname] = []
    count = 0
    for record in vcf.VCFReader(filename=vcf_filename):
        type="unknown"
        if record.is_snp and do_snps:
            type="snp"
            try:
                sequence[record.affected_start] = str(record.alleles[1]) # SNP, simply insert alt allele
            except IndexError as e:
                print("snp: Error assigning to {}:{}: {}".format(record.affected_start, record.affected_end, str(e)), file=sys.stderr)
            if args.remove_invariant:
                variant_sites.add(record.affected_start)
            count += 1
        elif record.is_indel:
            length = record.affected_end - record.affected_start
            if record.is_deletion and do_deletes:
                type="del"
                try:
                    sequence[record.affected_start:record.affected_end] = ['-'] * length
                except IndexError as e:
                    print("del: Error assigning to {}:{}: {}".format(record.affected_start, record.affected_end, str(e)), file=sys.stderr)
                count += 1
            else:
                if do_inserts:
                    print("Warning: insert processing from VCF is dangerously broken", file=sys.stderr)
                    type="ins"
                    # insertions[seqname].append(record)
                    ref = str(record.alleles[0])
                    alt = str(record.alleles[1])
                    # print("ins", alt.startswith(ref), fuzzysearch(ref, alt), ref, alt, record.affected_start, record.affected_end, len(alt) - len(ref), len(alt), len(ref), record.affected_end - record.affected_start + 1)
                    alt_sequence = alt[len(ref) - 1:] if alt.startswith(ref) else alt
                    insertion_sites.append((record.affected_start, record.affected_end, alt_sequence, seqname))
                    # interval = intervaltree.Interval(record.affected_start, record.affected_start + length, data=[seqname])
                    # if interval in tree:
                    #     existing_interval = tree[interval.begin:interval.end + 1]
                    #     start = min([existing_interval.begin, interval.begin])
                    #     end = max([existing_interval.end, interval.end])
                    #     tree.remove(existing_interval)
                    #     new_interval = intervaltree.Interval(start, end, existing_interval.data + interval.data)
                    #     tree.add(new_interval)

if args.remove_invariant:
    reference_str = ''.join([c for (i, c) in enumerate(reference) if i in variant_sites])
    reference_seq_variant = SeqRecord(Seq(reference_str), id=reference_seq.id, description=reference_seq.description)
    SeqIO.write(reference_seq_variant, args.output_file, "fasta")
else:
    SeqIO.write(reference_seq, args.output_file, "fasta")

offset = 0
sequence_length = 0
for name in sequence_names:
    sequence = sequences[name]
    sequence_length = len(sequence)
    for site in sorted(insertion_sites, key=itemgetter(0)):
        (start, end, allele, seqname) = site
        # print(start, allele, seqname)
        length = len(allele)
        # start += offset
        # end += offset
        # offset += length
        try:
            if name == seqname:
                sequence[start:end] = list(str(allele))
            else:
                sequence[start:end] = ['-'] * length
        except IndexError as e:
            print("ins: Error assigning to {}:{}: {}".format(start, end, str(e)), file=sys.stderr)

    if args.remove_invariant:
        seq_str = ''.join([c for (i, c) in enumerate(sequence) if i in variant_sites])
    else:
        seq_str = ''.join(sequence)
    SeqIO.write(SeqRecord(Seq(seq_str, alphabet=IUPAC.ambiguous_dna), id=name, description=""), args.output_file, "fasta")

        # output.write(bytes("\t".join([type, str(record.affected_start), str(record.affected_end), str(record.alleles[0]), str(record.alleles[1])])+"\n", encoding="ascii"))
    # output.close()

args.output_file.close()
