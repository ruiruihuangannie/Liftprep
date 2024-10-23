#!/usr/bin/perl
use strict;
use warnings;

# Usage: perl extract_fasta.pl input.fasta output.fasta chr1 chr2 ...

if (@ARGV < 3) {
    die "Usage: perl extract_fasta.pl input.fasta output.fasta chr1 chr2 ...\n";
}

my $input_fasta = shift @ARGV; 
my $output_fasta = shift @ARGV;
my %extract_names = map { $_ => 1 } @ARGV;

open(my $in_fh, '<', $input_fasta) or die "Could not open file '$input_fasta' $!";
open(my $out_fh, '>', $output_fasta) or die "Could not open file '$output_fasta' $!";

my $keep = 0;
while (my $line = <$in_fh>) {
  chomp $line;

  if ($line =~ /^>(\S+)/) {   # Matches the header line by '>'
    my $chr_name = $1;        # Extract the chromosome name (e.g., chr1)
    
    if (exists $extract_names{$chr_name}) {
      $keep = 1;
      print $out_fh "$line\n";  # Write the header to the output file
    } else {
      $keep = 0;
    }
  } elsif ($keep) {
    print $out_fh "$line\n";
  }
}

close $in_fh;
close $out_fh;

print "Extraction completed.\n";