SCFtests
========

Tools for testing effect of SCF on EXAFS fits

## Prerequisites

You **must** have these tools on your computer, properly built and functioning:

1. [Larch](https://github.com/xraypy/xraylarch)
2. [feff85exafs](https://github.com/xraypy/feff85exafs)

The following python modules are used:

1. [pystache](https://github.com/defunkt/pystache)

The report at the end of the performing all the fits is written using
LaTeX, so you will also need an adequately complete LaTeX installation.

## Curated set of standard data

1. Copper
2. NiO
3. FeS2
4. UO2
5. BaZrO3
6. Uranyl ion in solution
7. bromoadamantane

## Workflow

This was all developed on a linux computer.  No explicit support is
offered for Windows although there should be enough information
provided to figure out how to get all this to work on Windows.

### Set up workspace.

Run the `prep.sh` shell script:

```bash
./prep.sh Copper
./prep.sh BaZrO3
./prep.sh FeS2
./prep.sh NiO
./prep.sh UO2
./prep.sh bromoadamantane
./prep.sh uranyl
```

This is time-consuming.  Each of those steps will create a set of
subdirectories for each material, then run Feff under a variety of
conidtions.  For each material, Feff will be run using:

1. Feff6
2. Feff85exafs, but without self-consistency
3. Feff85exafs, with self-consistency using a sequence of
   self-consistency cluster sizes.  For most materials, 5 calculations
   are made at increasing radii.  For bromoadamantane, only 1 SCF
   calculation is made which includes the entire molecule.
