#!/usr/bin/perl
use strict;
use warnings;

# Usage: perl remove_fasta.pl input.fasta output.fasta chr1 chr2 ...

if (@ARGV < 3) {
    die "Usage: perl remove_fasta.pl input.fasta output.fasta chr1 chr2 ...\n";
}

my $input_fasta = shift @ARGV; 
my $output_fasta = shift @ARGV;
my %remove_names = map { $_ => 1 } @ARGV;  # Chromosomes to remove

open(my $in_fh, '<', $input_fasta) or die "Could not open file '$input_fasta': $!";
open(my $out_fh, '>', $output_fasta) or die "Could not open file '$output_fasta': $!";

my $keep = 1;
while (my $line = <$in_fh>) {
    chomp $line;

    if ($line =~ /^>(\S+)/) {  # Matches the header line by '>'
        my $chr_name = $1;     # Extract the chromosome name (e.g., chr1)

        # If the chromosome is one we want to remove, stop writing it
        if (exists $remove_names{$chr_name}) {
            $keep = 0;         # Don't keep this chromosome
        } else {
            $keep = 1;
            print $out_fh "$line\n";  # Write the header of chromosomes we are keeping
        }
    } elsif ($keep) {
        print $out_fh "$line\n";  # Write sequence data only for kept chromosomes
    }
}

close $in_fh;
close $out_fh;

print "Removal completed.\n";