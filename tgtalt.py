import utils
import sys
import argparse

''' Usage:
python3 tgtalt.py --tgt_fna sample_inputs/Ash1.fna
                  --chroms  sample_inputs/chroms.csv
'''
def parse_chroms(fh):
    tgt = dict()
    for line in fh.readlines():
        ln = line.rstrip().split(",")
        tgt[ln[1]] = ln[0]
    fh.close()
    return tgt


def parse_args(arglist):
    parser = argparse.ArgumentParser(description="Canonicalize target genomes.")
    
    parser.add_argument('--tgt_fna', type=str, required=True, help="FNA file for the target genome reference (e.g., Ash1.fna)")
    parser.add_argument('--chroms', type=str, required=True, help="Path to the map file (e.g., chroms.csv)")
    args = parser.parse_args()
    return args


def main(arglist=None):
    args = parse_args(arglist=None if sys.argv[1:] else ['--help'])
    chrms = parse_chroms(open(args.chroms, 'r'))
    tgt_fna = utils.make_canonical(
      chrms, 
      [args.tgt_fna]
    )
    print(f'Canonicalized target file in {tgt_fna}')


if __name__=='__main__':
    main()