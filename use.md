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

[As discussed elsewhere](README.md), self-consistency provides scant
impact on the quality of the EXAFS analysis or on the measured
results.

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

The executive summary of this test is that the original assessment of
6x6 (IORDER=2) is the correct choice.

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
SCF radii used in the testing steps.

If the feff calculations have already be run, this will be noticed
when setting the `material` attribute.  In that case, the `prep()`
step can be skipped, and you can proceed directly to fitting.

Once the feff calculations have run to completion, you can run the
canned fitting model using each of the feff models:

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

There is no persistence of the fitting results (yet).

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
       feff6: 4.96784 +/- 0.49360
       noSCF: 5.70543 +/- 0.48196
   withSCF_3: 3.44875 +/- 0.56411
   withSCF_4: 3.54301 +/- 0.56281
   withSCF_5: 3.39539 +/- 0.56334
 withSCF_5.5: 3.40748 +/- 0.56450
   withSCF_6: 3.46357 +/- 0.56386
```

### Tables of fit results

To generate a table of results for variables and statistical
parameters from the fit sequence:

```
larch> print a.table()

Best fit values

| model        | alpha         | amp     | enot     | ss1         | thetad   |
|:-------------|:--------------|:--------|:---------|:------------|:---------|
| feff6        | -0.00074(92)  | 0.96(4) | 4.97(49) | 0.00382(33) | 253(22)  |
| noSCF        | -0.00046(90)  | 0.95(4) | 5.71(48) | 0.00400(33) | 239(19)  |
| withSCF(3)   | -0.00077(104) | 0.94(5) | 3.45(56) | 0.00402(38) | 241(22)  |
| withSCF(4)   | -0.00076(104) | 0.94(5) | 3.54(56) | 0.00402(38) | 242(22)  |
| withSCF(5)   | -0.00077(104) | 0.94(5) | 3.40(56) | 0.00402(38) | 241(22)  |
| withSCF(5.5) | -0.00077(105) | 0.94(5) | 3.41(56) | 0.00402(38) | 241(22)  |
| withSCF(6)   | -0.00076(104) | 0.94(5) | 3.46(56) | 0.00402(38) | 241(22)  |

Statistics

| model        |   chi-square |   chi-reduced |   R-factor |
|:-------------|-------------:|--------------:|-----------:|
| feff6        |    1444.2957 |       54.3832 |     0.0145 |
| noSCF        |    1412.8206 |       53.1981 |     0.0142 |
| withSCF(3)   |    1820.8201 |       68.5608 |     0.0182 |
| withSCF(4)   |    1814.2834 |       68.3147 |     0.0182 |
| withSCF(5)   |    1816.9001 |       68.4132 |     0.0182 |
| withSCF(5.5) |    1823.0856 |       68.6461 |     0.0183 |
| withSCF(6)   |    1819.9264 |       68.5271 |     0.0182 |

```

The formatting of the table is controlled by the `tableformat`
attribute and can be any of the
[strings specified here](https://pypi.python.org/pypi/tabulate#table-format).
By default, the `pipe` format is used.  `latex` is handled specially
by the `table()` method.

### Examine the full fit report

```
larch> a.report('feff6')
```

This writes larch's fit report to the screen for the fit using the
specified feff model.

The integer shortcut from the `plot()` method can be used here.

## A larch script for testing all standards

Here is a very simple script.  It will be quite time consuming as feff
must be run in the `prep()` step for each material.

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


# Adding new materials

Each material must have a set of files with specific names.  Using
Copper as the example, there must be a subdirectory of the repository
called `Copper`.  In that subdirectory, there must be the following
files:

1. `Copper.json`: a JSON file containing values used in the mustache
   file 
2. `Copper.mustache`: a feff.inp for running feff8 with certain values
   replaced by [mustache](https://github.com/mustache/mustache)
   tokens
3. `Copper.feff6`: the same feff.inp data, but structured for use with
   feff6
4. `Copper.py`: the fitting model, using larch syntax for setting up
   and running the fit
5. `Copper.chik`: the chi(k) as a column ASCII file with wavenumber in
   the first column and un-k-weighted chi(k) in the second column

So, if you introduce a new material, you **must** provide each of
these files, replacing `Copper` with the name of the new material.

A few notes:

* In the JSON file, the `radii` item is a list of radii over which to
  compute the self-consistency.  Unless the material is a small
  molecule, you should select 5 or so values.  The first should
  include only the first coordination shell.  The largest radii should
  not be so large that the feff calculation takes inordinately long.
* For the mustache template of the feff.inp file, follow the example
  of the ones already in the repository.  You will likely want to
  generate a feff8 input file using whatever tool you normally use
  (Atoms, for example), then edit it by hand to insert the mustache
  tokens in the same places as in the examples.
* For the feff6 input file, just use Atoms (or whatever) to make a
  feff6 input, then rename it.
* For the fitting model in the `.py` file, again follow the examples
  given.  How you set up the parameters and paths is entirely up to,
  but be sure to include all of the logic towards the end of the file,
  including:
  * The setting of `rx` the upper bound of the fit in R
  * The bits controlled with the `doplot` and `verbose` flags
  * The writing of the output ASCII column files
  * The writing of the gnuplot script, making sure to set all of its
    mustache substitutions correctly for your fitting model
* My typical pattern was to play with the fitting model in Artemis,
  the reproduce my final model in the `.py` file.  I then used Artemis
  to generate the `.chik` file.


# Adding new tests

A new test is added by making a new python script in the `fefftests`
folder.  This python file defines the `prep()` method.  That is, it
defines the conditions under which feff is run, then makes each feff
calculation.

The scf and iorder tests are pretty well commented.  Follow those
examples.  The bottom line is that they loop through the list of
testing conditions.  For each condition, a subdirectory called
`<testname>/<condition>` is created.  The mustache template is filled
in and written to `<testname>/<condition>/feff.inp`.  Finally, feff is
run.

Note that, to verify that the *exact* same set of scattering paths are
used for every test, the `paths.dat` file from the `scf/feff6` test
should be copied into each new testing subdirectory.  The reason for
this is to be sure that path indexing is consistent between models.
Which a small change to the feff model, the amplitude of a small path
might cause it to fall below one of feff's filtering criteria.  This
would change the indexing of subsequent paths.  The fitting models in
the `.py` files expect consistent path indexing.

If you add a new material, you should edit the `fefftest.py` plugin
file to add the name of your new material to the list at line 42.

If your test requires modification of the `feff.inp` file, then you
should edit the `<material>.mustache` file for each material
accordingly and add the necessary parameters to the `<material>.json`
files.  Be sure to provide a sensible default for your new parameters
so that other tests will still run correctly.

# Results and documentation

The file `results.tex` gathers up the output of all the stuff above
for conversion to a nice PDF file.  Eventually I decided I wanted to
make a GitHub Pages website instead.  The content of `results.tex` was
the starting point for the current `README.md` file.

The `README.md` file is being maintained.

The file `iord.tex` collects the results of the iorder test for
conversion to a nice PDF file.

If you add a new material, you should edit the `fefftest.py` plugin
file to add the name of your new test to the list at line 43.

