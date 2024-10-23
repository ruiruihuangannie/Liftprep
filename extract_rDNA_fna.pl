#!/usr/bin/perl
use strict;
use warnings;

# Check if input file is provided
if (@ARGV != 1) {
    die "Usage: $0 <input_fasta_file>\n";
}

my $input_file = $ARGV[0];
my @target_chrs = qw(chr1 chr13 chr14 chr15 chr21 chr22);
my %target_hash = map { $_ => 1 } @target_chrs;

# Variables to store sequences
my $print = 0;
my $header = "";

# Open the input FASTA file
open(my $fh, '<', $input_file) or die "Could not open file '$input_file': $!\n";

# Parse the file line-by-line
while (my $line = <$fh>) {
    chomp $line;
    
    if ($line =~ /^>(\S+)/) {  # Match header line
        $header = $1;
        $print = exists $target_hash{$header} ? 1 : 0;
    }

    print "$line\n" if $print;
}

close($fh);