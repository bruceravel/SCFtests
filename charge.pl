#!/usr/bin/perl

use strict;
use warnings;
use File::Spec;
use Text::TabularDisplay;

my $material = $ARGV[0] || 'Copper';
chop $material if $material =~ m{/\z};

opendir(my $D, File::Spec->catfile($material, 'baseline')) || die "can't opendir $material/baseline/: $!";
my @scfdirs = grep { /^with/ } readdir($D);
closedir $D;


my @buffer;
my %mu = ();
my %ct = ();
my $flag = 0;
my $ipcount = 0;
my $mu_old = 0;
foreach my $d (sort @scfdirs) {
  my $logfile = File::Spec->catfile($material, 'baseline', $d, 'f85e.log');
  #print $logfile, $/;

  @buffer  = ();
  $flag    = 0;
  $ipcount = 0;
  open(my $L, '<', $logfile) || die "can't open $logfile: $!";

  while (<$L>) {
    chomp;
    push @buffer, $_;
    shift @buffer if $#buffer > 15;
    if ($_ =~ m{mu_old}) {
      my @list = split(" ", $_);
      $mu_old = $list[1];
    };
    last if $_ =~ m{Done with module 1:};
  };

  foreach my $i (0 .. $#buffer) {
    ## grab edge estimate
    if ($buffer[$i] =~ m{mu_new}) {
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
    if ($flag) {
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



print title("charge transfer in $material", 2);

my $t = Text::TabularDisplay->new('ip', @rscf);
foreach my $i (0 .. $ipcount-1) {
  my @these = ();
  foreach my $r (sort keys %mu) {
    push @these, sprintf("%6.3f", $ct{$r}->[$i]);
  };

  $t->add(" $i", @these);
}

my @these = ();
foreach my $r (sort keys %mu) {
  push @these, sprintf("%6.3f", $mu{$r});
};
$t->add('mu', @these);

print $t->render, $/ x 2;
print "mu_old = $mu_old\n\n";


sub title {
  my ($phrase, $nnl) = @_;
  return $phrase, $/, "=" x length($phrase), $/ x $nnl;
};
