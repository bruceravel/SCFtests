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

## Established tests

### SCF

This is a test that runs any of the curated standards against a
sequence of different feff models related to probing the effect of
self-consistency.  Feff will be run in each of the following ways:

1. feff6
2. feff8 without self-consistency
3. feff8 with one or more radii for the self-consistency computation

The point of this test is to evaluate the effect of the feff model on
EXAFS fitting.  This tests feff6 against feff8 and self-consistency
against the absence of self-consistency.

### iorder

In the paper that introduced feff6 ("Multiple-scattering calculations
of x-ray-absorption spectra", S. I. Zabinsky, J. J. Rehr,
A. Ankudinov, R. C. Albers, and M. J. Eller, Phys. Rev. **B**52,
p. 2995,
[doi:10.1103/PhysRevB.52.2995](http://dx.doi.org/10.1103/PhysRevB.52.2995)),
the authors discuss an approximation made in the computation of the
Rehr-Albers separable propagators.  The scaling of the spherical
harmonic scattering factors used to compute the photoelectron free
propagator is such that the corresponding matrix can be limited in
dimension to 6x6.  There is some discussion about the accuracy of this
approximation at high energy, but the authors assert the numerical
accuracy of this approximation is within 1% of the full calculation at
photoelectron wavenumbers below 20.

The size of this matrix is controlled in the feff input file by the
IORDER keyword.  The default value of 2 corresponds to the 6x6
matrix.  The assertion that the 6x6 matrix is adequate is easily tested
using this testing framework.

The iorder test runs feff8 with a short self-consistency radius and
with a range of iorder values, including 1, 2, 3, 4, and 10 (10 being
something the source code refers to as the "cute" algorithm).

Limiting the iorder test to first shell fitting will result in
identical fits for all iorder values.  Single scattering paths are
computed exactly in feff.  It is only multiple scattering paths that
are subject to the IORDER approximation.

## Workflow

The testing is implemented as a larch plugin.  Once larch has been
started, load the `fefftest` plugin:

```
larch> add_plugin('fefftest')
```

Note that these instructions presume that your working directory is
the main directory of the repository.  This is not a Larch plugin in
the sense that it is designed and written to be used anywhere and in
any way.  The workflow of the feff testing expects to find certain
files in certain locations.  The easiest way to ensure this is to do
you testing in the repository directory.

Once the plugin is loaded, create a FeffTestGroup object, set some
of its attributes, and prepare the feff calculations:

```
larch> a = ft()
larch> a.test = 'scf'
larch> a.material = 'Copper'
larch> a.prep()
```

The `a.prep()` step may be quite time consuming, depending on the
SCF radii used in the testing steps.  Once the feff calculations have
run to completion, you can run the canned fitting model using each of
the feff models:

```
larch> a.fits()
>>>>>>>>> fitting with model: feff6
wrote to file 'Copper/scf/fit_feff6.k'
wrote to file 'Copper/scf/fit_feff6.r'
>>>>>>>>> fitting with model: noSCF
wrote to file 'Copper/scf/fit_noSCF.k'
wrote to file 'Copper/scf/fit_noSCF.r'
>>>>>>>>> fitting with model: withSCF_3
wrote to file 'Copper/scf/fit_withSCF_3.k'
wrote to file 'Copper/scf/fit_withSCF_3.r'
  (and so one)
```

### Make a plot of any fit:

```
larch> a.plot('feff6')
```

As a shortcut, you can use integer arguments where the integers refer
to the (1-based) position of the model in the `models` attribute.

```
larch> show a.models
['feff6', 'noSCF', withSCF_3', withSCF_4', withSCF_5', withSCF_5.5', withSCF_6']
larch> a.plot(1)
```

`a.plot(1)` and `a.plot('feff6')` make the same plot.


### Make a nice PNG image of any fit:

```
larch> a.png('feff6')
```

In the case of the Copper SCF test, this writes a file to
`Copper/scf/fit_feff6.png`.

The integer shortcut from the `plot()` method can be used here.

### Examine an individual parameter

To examine the evolution of an individual fitting parameter over
the sequence of feff calculations:

```
larch> a.compare('enot')

```

### Tables of fit results

To generate a table of results for variables and statistical
parameters from the fit sequence:

```
larch> a.table()

```

The formatting of the table is controlled by the `tableformat`
attribute and can be any of the
[strings specified here](https://pypi.python.org/pypi/tabulate#table-format).
By default, the `pipe` format is used.  `latex` is handled specially
by the `table()` method.


## A larch script for testing all standards

Here is a very simple script.  It will be very time consuming due as
feff must be run in the `prep()` step for each material.

```python
add_plugin('fefftest')
a = ft()
a.test = 'scf'
for m in ("Copper", "NiO", "FeS2", "UO2", "BaZrO3", "bromoadamantane", "uranyl"):
    a.material = m
    a.prep()
    a.fits()
    print a.table()
#endfor
```

It would be wise to capture the output of the `table()` method in
some way.  As this example is written, the table containing the
fitting results will be lost among the voluminous screen output of
the many feff runs.



## Obsolete stuff follows

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
* `plot.mustache`: mustache template used to generate gnuplot scripts
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

The file `plot.mustache` is a [mustache](https://mustache.github.io/)
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
