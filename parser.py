import argparse

def parse_args(arglist):
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Merge genome reference files with customizable options for VDJ, rDNA, and chrY handling.")
    
    # First genome set (GRCh38 in the original example)
    parser.add_argument('--ref1_gff', type=str, required=True, help="GFF file for the first genome reference (e.g., GRCh38.gff)")
    parser.add_argument('--ref1_fna', type=str, required=True, help="FNA file for the first genome reference (e.g., GRCh38.fna)")
    parser.add_argument('--ref1_VDJ', type=str, choices=["Discard", None], default="Discard", help="VDJ handling option for the first reference")
    parser.add_argument('--ref1_rDNA', type=str, choices=["Discard", None], default="Discard", help="rDNA handling option for the first reference")
    parser.add_argument('--ref1_chrY', type=str, choices=["Discard", None], default="Discard", help="chrY handling option for the first reference")
    parser.add_argument('--ref1_alias', type=str, default='GRCh38',help="Alias for reference 1")

    # Second genome set (CHM13 in the original example)
    parser.add_argument('--ref2_gff', type=str, required=True, help="GFF file for the second genome reference (e.g., CHM13.gff)")
    parser.add_argument('--ref2_fna', type=str, required=True, help="FNA file for the second genome reference (e.g., CHM13.fna)")
    parser.add_argument('--ref2_VDJ', type=str, choices=["Extract", None], default=None, help="chrY handling option for the second reference")
    parser.add_argument('--ref2_rDNA', type=str, choices=["Extract", None], default=None, help="rDNA handling option for the second reference")
    parser.add_argument('--ref2_chrY', type=str, choices=["Extract", None], default="Extract", help="chrY handling option for the second reference")
    parser.add_argument('--ref2_alias', type=str, default='CHM13',help="Alias for reference 1")

    # Additional file input
    parser.add_argument('--mapfile', type=str, required=True, help="Path to the map file (e.g., chroms.csv)")

    # Parse the arguments
    args = parser.parse_args()

    # Here you would pass the parsed arguments to your actual merging function
    print(f"Processing with the following reference arguments:")
    print(f"Reference 1: GFF = {args.ref1_gff}\tFNA = {args.ref1_fna}\tVDJ = {args.ref1_VDJ}\trDNA = {args.ref1_rDNA}\tchrY = {args.ref1_chrY}")
    print(f"Reference 2: GFF = {args.ref2_gff}\tFNA = {args.ref2_fna}\tVDJ = {args.ref2_VDJ}\trDNA = {args.ref2_rDNA}\tchrY = {args.ref2_chrY}")
    print(f"Mapfile: {args.mapfile}")

    return args