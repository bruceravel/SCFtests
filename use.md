SCFtests
========

Tools for testing effect of SCF on EXAFS fits

## Prerequisites

You **must** have these tools on your computer, properly built and functioning:

1. [Larch](https://github.com/xraypy/xraylarch)
2. [feff85exafs](https://github.com/xraypy/feff85exafs)

The following python modules are used:

1. [pystache](https://github.com/defunkt/pystache)
2. [tabulate](https://pypi.python.org/pypi/tabulate)

An adequately complete LaTeX installation is needed to compile the
latex documents.

## Curated set of standard data

1. Copper
2. NiO
3. FeS2
4. UO2
5. BaZrO3
6. Uranyl ion in solution
7. bromoadamantane

Each of these folders has much of the same stuff as the data-bearing
tests for [feff85exafs](https://github.com/xraypy/feff85exafs),
including a mustache template for `feff.inp`, a json file controlling
how the template is filled in, &chi;(k) data, and a python script
defining a fitting model using Larch.  There is also a Feff6 input
file and a `paths.dat` file which is used to be sure that each Feff
calculation produces the exact same set of paths.


Future materials:

* methyltin
* ???

## Workflow

This was all developed on a linux computer.  No explicit support is
offered for Windows although there should be enough information
provided to figure out how to get all this to work on Windows.

This is a mish-mash of shell, python, larch, and perl scripts.  That
works and is not exactly wrong, but it is pretty slap-dash.  One could
imagine rewriting the whole thing as a Larch app....

### File listing

* `prep.sh`: (shell) prepare a sequence of Feff calculations for a material
* `models.py`: (python) prepare and run a single Feff calculation
* `allfits.lar`: (larch) run all fits for all materials
* `ficompare.lar`: (larch) run all fits for a single material
* `fit.mustache`: mustache template used to generate gnuplot scripts
* `allplots.sh`: (shell) convert all the gnuplot scripts into PNG images
* `charge.pl`: (perl) snarf information about charge transfer and threshold energies from Feff run logs
* `README.md`: (markdown) full description of SCF/EXAFS results
* `results.tex`: (latex) full description of SCF/EXAFS results
* `iord.tex`: (latex) full description of iorder/EXAFS results
* `feffitplots.sty`: (latex) style file for formating grids of plots

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

This is time-consuming -- maybe hours, depending on your computer.
Each of those steps will create a set of subdirectories for each
material, then run Feff under a variety of conidtions.  For each
material, Feff will be run using:

1. Feff6
2. Feff85exafs, but without self-consistency
3. Feff85exafs, with self-consistency using a sequence of
   self-consistency cluster sizes.  For most materials, 5 calculations
   are made at increasing radii.  For bromoadamantane, only 1 SCF
   calculation is made which includes the entire molecule.

`prep.sh` is actually a wrapper around the `models.py` python script.
This script writes `feff.inp` appropriate to each calculation using a
mustache template found in each material's folder and the pystache
renderer.  It then uses Larch's feffrunner to run the correct version
of the Feff and cull chaff from Feff's output.

The `charge.pl` script examines the Feff run logs for a material and
generates a markdown table containing the results of charge transfer
for each unique potential in the material and for each SCF radius.  It
also shows the threshold energy for each of the calculations.  This
information may be useful in understanding the dependence of fitted E0
on Feff theory.


### Run all of the fits

The file `allfits.lar` is a Larch script which runs through all of the
materials and performs the sequence of fits.  Fire up larch, then run
it like so:

	larch> run 'allfits.lar'

It calls on the `fitcompare.lar` Larch script, which sets up default
values for various parameters (or uses those specified by the
`allfits.lar` script).  It then runs the `fitcompare` method from the
`f85ut` unit testing group.  That method knows how to search out the
folders containing each of the Feff calculations then run a fit on
each one.  Finally, `fitcompare.lar` gathers up all the fitting
results for a material and organizes them into some sort of table.
The `output` parameter in `allfits.lar` and `fitcompare.lar` is used
to set the format of the output table.  See
[the tabulate documentation](https://pypi.python.org/pypi/tabulate#table-format)
for the list of table formats.

The file `fit.mustache` is a [mustache](https://mustache.github.io/)
template for a [gnuplot](http://gnuplot.info) script.  Each python
script defining the fitting model for a material makes a call to the
pystache renderer after finishing each fit.  Thus a `.gp` file is
generated for each fit made to each material and given a name that
indicates the conditions of the fit (e.g. `fit_feff6.gp` or
`fit_withSCF_5.gp`).  After `allfits.lar` is finished, there will be
several such `.gp` files in each material's folder.

The shell script `allplots.sh` finds each of these gnuplot scripts and
runs gnuplot on them, producing a `.png` output file for each one.
The PNG files have the same name as the gnuplot script, thus
`fit_withSCF_5.gp` makes `fit_withSCF_5.png` and so on.



## Results and documentation

The file `results.tex` gathers up the output of all the stuff above
for conversion to a nice PDF file.  Eventually I decided I wanted to
make a GitHub Pages website instead.  The content of `results.tex` was
the starting point for the current `README.md` file.

The `README.md` file is being maintained.

The file `iord.tex` collects the results of the iorder test for
conversion to a nice PDF file.
