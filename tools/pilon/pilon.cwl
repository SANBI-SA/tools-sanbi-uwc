#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
stdout: output.txt

requirements:
  - class: EnvVarRequirement
    envDef:
      - envName: CLASSPATH
        envValue: /home/pvh/Documents/code/SANBI/pilon/pilon-1.18.jar
#  - class: InlineJavascriptRequirement

inputs:
  java_opts:
    type: string?
    doc: "JVM arguments should a quoted, space separated list (e.g. \"-Xms128m -Xmx512m\")"
    inputBinding:
      position: 1
  genome:
    type: File
    doc: |
      The input genome we are trying to improve, which must be the reference used
      for the bam alignments.  At least one of --frags or --jumps must also be given.
    inputBinding:
      position: 5
      prefix: "--genome"
  frags:
    type:
      - 'null'
      - type: array
        items: File
        inputBinding:
          prefix: --frags
          position: 6
    doc: |
      A bam file consisting of fragment paired-end alignments, aligned to the --genome
      argument using bwa or bowtie2.  This argument may be specifed more than once.
    secondaryFiles:
      - ".bai"
  jumps:
    type:
      - 'null'
      - type: array
        items: File
        inputBinding:
          prefix: --jumps
          position: 6
    doc: |
      A bam file consisting of fragment paired-end alignments, aligned to the --genome
      argument using bwa or bowtie2.  This argument may be specifed more than once.
    secondaryFiles:
      - ".bai"
  unpaired:
    type:
      - 'null'
      - type: array
        items: File
        inputBinding:
          prefix: --unpaired
          position: 6
    doc: |
      A bam file consisting of unpaired alignments, aligned to the --genome argument
      using bwa or bowtie2.  This argument may be specifed more than once.
    secondaryFiles:
      - ".bai"
  bam:
    type:
      - 'null'
      - type: array
        items: File
        inputBinding:
          prefix: "--bam"
          position: 6
    secondaryFiles:
      - ".bai"
    doc: |
      A bam file of unknown type; Pilon will scan it and attempt to classify it as one
      of the above bam types.
  vcf_output:
    type: boolean
    default: false
    inputBinding:
      position: 7
      prefix: "--vcf"
  output_prefix:
    type: string
    default: pilon
    inputBinding:
      prefix: "--output"
      position: 7
  variant_output:
    type: boolean
    default: false
    doc: Sets up heuristics for variant calling, as opposed to assembly improvement, equivalent to "--vcf --fix all,breaks"
    inputBinding:
      prefix: --variant
      position: 7
  changes:
    type: boolean
    default: false
    doc: Output file describing changes in FASTA output
    inputBinding:
      prefix: --changes
      position: 7
  tracks:
    type: boolean
    default: false
    doc: Write many track files (*.bed, *.wig) suitable for viewing in a genome browser.
    inputBinding:
      prefix: --tracks
      position: 7
  vcfqe:
    type: boolean
    default: false
    doc: Add a QE (quality-weighted evidence) field rather than the default QP (quality-weighted percentage of evidence) field.
    inputBinding:
      prefix: --vcfqe
      position: 7
  chunksize:
    type: int?
    doc: Input FASTA elements larger than this will be processed in smaller pieces not to exceed this size (default 10000000).
    inputBinding:
      prefix: --chunksize
      position: 8
  vcf:
    type: boolean
    default: false
    doc: Generate a VCF file describing variants
    inputBinding:
      prefix: --vcf
      position: 8
  diploid:
    type: boolean
    default: false
    doc: Sample is from diploid organism; will eventually affect calling of heterozygous SNPs
    inputBinding:
      prefix: --diploid
      position: 8
  fix:
    type: string?
    doc: |
              A comma-separated list of categories of issues to try to fix:
                "bases": try to fix individual bases and small indels;
                "gaps": try to fill gaps;
                "local": try to detect and fix local misassemblies;
                "all": all of the above (default);
                "none": none of the above; new fasta file will not be written.
              The following are experimental fix types:
                "amb": fix ambiguous bases in fasta output (to most likely alternative).
                "breaks": allow local reassembly to open new gaps (with "local").
                "novel": assemble novel sequence from unaligned non-jump reads.
    inputBinding:
      prefix: --fix
      position: 8
  dumpreads:
    type: boolean
    default: false
    doc: Dump reads for local re-assemblies.
    inputBinding:
      prefix: --dumpreads
      position: 8
  duplicates:
    type: boolean
    default: false
    doc: Use reads marked as duplicates in the input BAMs (ignored by default).
    inputBinding:
      prefix: --duplicates
      position: 8
  iupac:
    type: boolean
    default: false
    doc: Output IUPAC ambiguous base codes in the output FASTA file when appropriate.
    inputBinding:
      prefix: --iupac
      position: 8
  nonpf:
    type: boolean
    default: false
    doc: Use reads which failed sequencer quality filtering (ignored by default).
    inputBinding:
      prefix: --nonpf
      position: 8
  targets:
    type: string?
    doc: |
      Only process the specified target(s).  Targets are comma-separated, and each target
      is a fasta element name optionally followed by a base range.
      Example: "scaffold00001,scaffold00002:10000-20000" would result in processing all of
      scaffold00001 and coordinates 10000-20000 of scaffold00002.
      If "targetlist" is the name of a file, each line will be treated as a target
      specification.
    inputBinding:
      prefix: --targets
      position: 8
  threads:
    type: int?
    doc: Degree of parallelism to use for certain processing (default 1). Experimental.
    default: 1
    inputBinding:
      prefix: --threads
      position: 8
  verbose:
    type: boolean
    default: false
    doc: More verbose output
    inputBinding:
      prefix: --verbose
      position: 8
  debug:
    type: boolean
    default: false
    doc: Debugging output (implies verbose)
    inputBinding:
      prefix: --debug
      position: 8
  defaultqual:
    type: int?
    doc: Assumes bases are of this quality if quals are no present in input BAMs (default 15).
    inputBinding:
      prefix: --defaultqual
      position: 9
  flank:
    type: int?
    doc: Controls how much of the well-aligned reads will be used; this many bases at each end of the good reads will be ignored (default 10).
    inputBinding:
      prefix: --flank
      position: 9
  gapmargin:
    type: int?
    doc: Closed gaps must be within this number of bases of true size to be closed (100000)
    inputBinding:
      prefix: --gapmargin
      position: 9
  kmersize:
    type: int?
    doc: Kmer size used by internal assembler (default 47).
    inputBinding:
      prefix: --K
      position: 9
  mindepth:
    type: float?
    doc: |
      Variants (snps and indels) will only be called if there is coverage of good pairs
      at this depth or more; if this value is >= 1, it is an absolute depth, if it is a
      fraction < 1, then minimum depth is computed by multiplying this value by the mean
      coverage for the region, with a minumum value of 5 (default 0.1: min depth to call
      is 10% of mean coverage or 5, whichever is greater).
    inputBinding:
      prefix: --mindepth
      position: 9
  mingap:
    type: int?
    doc: Minimum size for unclosed gaps (default 10)
    inputBinding:
      prefix: --mingap
      position: 9
  minmq:
    type: int?
    doc: Minimum alignment mapping quality for a read to count in pileups (default 0)
    inputBinding:
      prefix: --minmq
      position: 9
  minqual:
    type: int?
    doc: Minimum base quality to consider for pileups (default 0)
    inputBinding:
      prefix: --minqual
      position: 9
  nostrays:
    type: boolean
    default: false
    doc: |
      Skip making a pass through the input BAM files to identify stray pairs, that is,
      those pairs in which both reads are aligned but not marked valid because they have
      inconsistent orientation or separation. Identifying stray pairs can help fill gaps
      and assemble larger insertions, especially of repeat content.  However, doing so
      sometimes consumes considerable memory.
    inputBinding:
      prefix: --nostrays
      position: 9

outputs:
  pilon_output:
    type: stdout
  fasta_output:
    type: File?
    outputBinding:
      glob: $(inputs.output_prefix).fasta
  vcf_output:
    type: File?
    outputBinding:
      glob: $(inputs.output_prefix).vcf
  track_outputs:
    type: File[]?
    outputBinding:
      glob:
        - $(inputs.output_prefix)Pilon.bed
        - $(inputs.output_prefix)Changes.wig
        - $(inputs.output_prefix)Unconfirmed.wig
        - $(inputs.output_prefix)CopyNumber.wig
        - $(inputs.output_prefix)Coverage.wig
        - $(inputs.output_prefix)BadCoverage.wig
        - $(inputs.output_prefix)PctBad.wig
        - $(inputs.output_prefix)DeltaCoverage.wig
        - $(inputs.output_prefix)DipCoverage.wig
        - $(inputs.output_prefix)PhysicalCoverage.wig
        - $(inputs.output_prefix)ClippedAlignments.wig
        - $(inputs.output_prefix)WeightedQual.wig
        - $(inputs.output_prefix)WeightedMq.wig
        - $(inputs.output_prefix)GC.wig

  changes_output:
    type: File?
    outputBinding:
      glob: $(inputs.output_prefix).changes

baseCommand: [java]

arguments:
    - valueFrom: "com.simontuffs.onejar.Boot"
      position: 2

doc: |
  Pilon is a software tool which can be used to:

      * Automatically improve draft assemblies
      * Find variation among strains, including large event detection

  For more info: https://github.com/broadinstitute/pilon/wiki
