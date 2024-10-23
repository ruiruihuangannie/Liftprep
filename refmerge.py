from parser import parse_args
import utils
import sys, os
import subprocess

''' Usage:
python3 refmerge.py --ref1_gff sample_inputs/GRCh38.gff 
                    --ref1_fna sample_inputs/GRCh38.fna
                    --ref2_gff sample_inputs/CHM13.gff
                    --ref2_fna sample_inputs/CHM13.fna
                    --mapfile  sample_inputs/multi_chroms.csv
'''
def parse_chroms(fh):
    head = fh.readline().rstrip().split(',')
    ref_1, ref_2 = dict(), dict()
    ref_1_name, ref_2_name = head[0], head[1]
    for line in fh.readlines():
        ln = line.rstrip().split(",")
        if ln[1] != '':
            ref_1[ln[1]] = ln[0]
        if len(ln) >= 3:
            ref_2[ln[2]] = ln[0]
    fh.close()
    return [ref_1_name, ref_1, ref_2_name, ref_2]

def main(arglist=None):
    args = parse_args(arglist=None if sys.argv[1:] else ['--help'])
    ref1_alias, ref1_chrms, ref2_alias, ref2_chrms = parse_chroms(open(args.mapfile, 'r'))
    chrom_lst = {**ref1_chrms, **ref2_chrms}
    ref1, ref2, ref1_fna, ref2_fna = utils.make_canonical(
        chrom_lst, 
        [args.ref1_gff, args.ref2_gff, args.ref1_fna, args.ref2_fna]
    )

    out_ref1 = f"{ref1.split('.')[0]}_discarded.gff"
    if os.path.isfile(out_ref1):
        print(f'[Info]: {out_ref1} exists, moving on...')
    else:
        utils.discard_gff(
            open(ref1, 'r'), open(out_ref1, 'w'),
            discard_VDJ  = (args.ref1_VDJ == 'Discard'),
            discard_rDNA = (args.ref1_rDNA == 'Discard'),
            discard_chrY = (args.ref1_chrY == 'Discard')
        )

    out_ref2 = f"{ref2.split('.')[0]}_discarded.gff"
    if os.path.isfile(out_ref2):
        print(f'[Info]: {out_ref1} exists, moving on...')
    else:
        utils.extract_gff(
            open(ref2, 'r'), open(out_ref2, 'w'), 
            extract_VDJ  = (args.ref2_VDJ == 'Extract'),
            extract_rDNA = (args.ref2_rDNA == 'Extract'),
            extract_chrY = (args.ref2_chrY == 'Extract')
        )
   
    print(f"Finished processing the reference annotatons.")
    print(f"Output reference annotation 1: {out_ref1}")
    print(f"Output reference annotation 2: {out_ref2}")
    print(f"Mapfile: {args.mapfile}")

    print(f"Processing reference genomes:")
    
    out_ref1_fna = ref1_fna
    if args.ref1_chrY == 'Discard':
        out_ref1_fna = out_ref1_fna.split('.')[0] + '.no_chrY.fna'
        subprocess.run(f'perl remove_fasta.pl {ref1_fna} {out_ref1_fna} chrY', 
                       shell=True, check=True, text=True)
    
    out_ref2_fna = ref2_fna
    if args.ref2_chrY == 'Extract':
        out_ref2_fna = out_ref2_fna.split('.')[0] + '.only_chrY.fna'
        subprocess.run(f'perl extract_fasta.pl {ref2_fna} {out_ref2_fna} chrY', 
                       shell=True, check=True, text=True)
    print(f"Finished processing the reference genomes.")
    print(f"Output reference genome 1: {out_ref1_fna}")
    print(f"Output reference genome 2: {out_ref2_fna}")

    print(f"Merging processing the references genomes.")
    subprocess.run(f'cat {out_ref1} {out_ref2} > sample_inputs/final.gff', shell=True, check=True, text=True)
    subprocess.run(f'cat {out_ref1_fna} {out_ref2_fna} > sample_inputs/final.fna', shell=True, check=True, text=True)
    print(f"Sample liftoff command:")
    print(f"time liftoff -p 24 -g final.gff -o out_dir/out.gff -dir out_dir/ -u out_dir/unmapped_features.txt -chroms chroms.txt -polish -exclude_partial -copies -sc 0.95 target.fa final.fna")

if __name__=='__main__':
    main()