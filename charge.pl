#!/usr/bin/perl

use strict;
use warnings;
use File::Spec;
use Text::MarkdownTable;

my $material = $ARGV[0] || 'Copper';
chop $material if $material =~ m{/\z};

## make a list of all SCF radii
opendir(my $D, File::Spec->catfile($material, 'scf')) || die "can't opendir $material/scf/: $!";
my @scfdirs = grep { /^with/ } readdir($D);
closedir $D;


my @buffer;
my %mu = ();
my %ct = ();
my $flag = 0;
my $ipcount = 0;
my ($mu_old, $mu_feff6) = (0,0);
foreach my $d (sort @scfdirs) {
  my $logfile = File::Spec->catfile($material, 'scf', $d, 'f85e.log');
  #print $logfile, $/;

  @buffer  = ();
  $flag    = 0;
  $ipcount = 0;
  open(my $L, '<', $logfile) || die "can't open $logfile: $!";

  while (<$L>) {
    chomp;
    push @buffer, $_;
    shift @buffer if $#buffer > 15;
    if ($_ =~ m{mu_old}) {	#  find the initial value for mu
      my @list = split(" ", $_);
      $mu_old = $list[1];
    };
    last if $_ =~ m{Done with module 1:};
  };

  foreach my $i (0 .. $#buffer) {
    ## grab edge estimate
    if ($buffer[$i] =~ m{mu_new}) { # find each updated value for mu
      my @list = split(" ", $buffer[$i]);
      $mu{$d} = $list[-1];
      next;
    };
    ## final charge transfer table is about to begin
    if ($buffer[$i] =~ m{Charge transfer}) {
      $flag = 1;
      next;
    };
    if ($buffer[$i] =~ m{Done with}) {
      last;
    };
    if ($flag) {		# snarf up the charge transfer for each ipot
      my @list = split(" ", $buffer[$i]);
      $ct{$d}->[$list[0]] = $list[1];
      ++$ipcount;
    };
  };

  close $L;
};


#use Data::Dump::Color;
#Data::Dump::Color->dd(\%mu);
#Data::Dump::Color->dd(\%ct);

my @rscf = ();
foreach my $scf (sort keys %mu) {
  my @list = split(/_/, $scf);
  push @rscf, sprintf("%4s", $list[1]);
};


open(my $FD, '<', File::Spec->catfile($material, 'scf', 'feff6', 'files.dat')) or die "could not open feff6 files.dat";
while (<$FD>) {
  next if $_ !~ m{Mu=([^ ]+) };
  $mu_feff6 = sprintf("%.3f", $1);
  last;
}
close $FD;


print title("Charge transfer and threshold energy", 2);

my $t = Text::MarkdownTable->new();
foreach my $i (0 .. $ipcount-1) {
  my %these = ();
  $these{' ip'} = $i;
  foreach my $r (sort keys %mu) {
    #push @these, sprintf("%6.3f", $ct{$r}->[$i]);
    my $key = 'R='.(split(/_/, $r))[1];
    $these{$key} = sprintf("%6.3f", $ct{$r}->[$i]);
  };

  $t->add(\%these);
}

my %these = ();
$these{' ip'} = '&mu;';
foreach my $r (sort keys %mu) {
  my $key = 'R='.(split(/_/, $r))[1];
  $these{$key} = sprintf("%6.3f", $mu{$r});
};
$t->add(\%these);

$t->done;
print "\nStarting value for &mu; in feff8 = $mu_old\n";
print   "Value for &mu; in feff6 = $mu_feff6\n\n";


sub title {
  my ($phrase, $nnl) = @_;
  return $phrase, $/, "-" x length($phrase), $/ x $nnl;
};
