
* [Background](#background)
* [Copper](#copper)
* [NiO, nickel (II) oxide](#nio)
* [FeS2, pyrite](#fes2)
* [UO2, uraninite](#uo2)
* [BaZrO3, barium zirconate](#bazro3)
* [C10H15Br, bromoadamantane](#bromoadamantane)
* [uranyl hydrate](#uranyl-hydrate)
* [Conclusion](#conclusion)

_____


Background
==========

1.  All XAS data were processed sensibly in
    [Athena](http://bruceravel.github.io/demeter/) with E0 chosen to
    be the first peak of the first derivative in &mu;(E). That may not
    be the best choice of E0 in all cases, but it is the obvious first
    choice and the likeliest choice to be made by a novice user of the
    software.

2.  All EXAFS data were Fourier transformed starting at 3/&Aring; and
    ending at a reasonable place where the signal was still much
    bigger than the noise. The choice of 3/&Aring; as the starting
    point was deliberate. The
    [Autobk algorithm](http://dx.doi.org/10.1103/PhysRevB.47.14126)
    (and most – if not all – other algorithms) is often unreliable
    below about 3/&Aring; due to the fact that the &mu;(E) is changing
    very quickly in that region. Thus the data above 3/&Aring; are
    likely to be reliable a free of systematic error due to the
    details of the background removal.

3.  All the materials considered have well-known structures. For these
    tests, we want to avoid the situation where error in a fitting
    model could be attributed to incomplete prior knowledge about the
    structure. That is, we want to isolate the details of the fitting
    model from the details of the theoretical calculation.

4.  The first three examples are dense, crystalline solids for which
    we expect self-consistency to contribute rather little to the
    analysis. The remaining materials all contribute interesting
    features for which self-consistency might play a role.

5.  In the plots, the ranges of the Fourier transform and of the fit
    are indicated by vertical black lines.

6.  Each material is fitted using theory from the version of _Feff6_
    that ships with [Ifeffit](https://github.com/newville/ifeffit),
    from [_feff85exafs_](https://github.com/xraypy/feff85exafs) with
    self-consistency turned off, and from with
    [_feff85exafs_](https://github.com/xraypy/feff85exafs) with
    self-consistency.  In each case, the default self-energy model
    (Hedin-Lundqvist) was used.

7.  For each material that is not a molecule, the analysis is done
    with a sequence of self-consistency radii. This is done to test
    the importance of the consideration of that parameter on the
    analysis. In the case of hydrated uranyl hydrate, this is a
    molecule, but the Feff calculation is done of a crystalline
    analogue to the molecule. The effect of self-consistency radius is
    tested in that case.

8.  Where appropriate (bromoadamantane, for example), the `lfms`
    parameter of the `SCF` card is set to 1.

9.  The uranyl calculation was a bit challenging with
    [_feff85exafs_](https://github.com/xraypy/feff85exafs). To get the
    program to run to complation, it was necessary to set the FOLP
    parameter to 0.9 for each unique potential. Given that the quality
    of the fit was much the same as for using _Feff6_, this was not
    examined further. Still, this merits further attention for this
    material.

10. We were interested to know if the effect of SCF on EXAFS fitting
    was different for a first shell fit as compared to a more
    extensive fitting model. So fits were generated for the first
    shells only of all materials except for uranyl hydrate for which
    the axial and equatorial scatterers cannot be isolated. Also, Matt
    tells me that, years ago, he and John looked at some _Feff6_/_Feff8_
    comparisons, but only for first shell fits. These first shell fits
    are intended for comparison to that older work.  _The results of
    the first shell fits are included in the repository, but not on
    this page as they do not tell a different story from the more
    complete fits presented here._

11. All fits were performed with a toolset written by Bruce and
    included here in this repository using the XAS analysis
    capabilities of [Larch](https://github.com/xraypy/xraylarch/).

12. All uncertainties are 1&sigma; error bars determined from the
    diagonal elements of the covarience matrix evaluated during the
    Levenberg-Marquardt minimizations.

13. The plots shown below for each material were generated using the
    tools in this repository.  You will notice that they appear to be
    highly repetitive.  For each material it is the case that the fits
    using the different theoretical models are nearly
    indistinguishable by eye.  The full complement of fits are shown
    for the sake of completeness.  As you scroll through the plots of
    the fit results, you may be tempted to think that the same image
    has been replicated several times.  I assure you that each plot is
    actual plot made using the actual fit to the different theory
    models!

14. The very astute Feff user might point out that the path indexing
    is not guaranteed to be consistent across versions.  That is, a
    small MS path may barely exceed the heap criterion in one version
    of Feff, but not in another.  That would change the indexing for
    all paths with longer half-path-lengths, thus confounding the use
    of single Larch fitting script with the different version of the
    theory.  To avoid this problem, the pathfinder in _Feff6_ was run,
    generating a `files.dat` file.  This `files.dat` was then copied
    into the folders where the various
    [_feff85exafs_](https://github.com/xraypy/feff85exafs)
    calculations were run.  The pathfinder was then skipped in each of
    the _Feff8_ runs.  This guaranteed that each theory calculation
    generated the same list of `feffNNNN.dat` files with the same
    indexing.


_____

Copper
======

The data is the canonical copper foil spectrum of
[Newville, et al. fame](https://github.com/XraySpectroscopy/XAS-Data-Interchange/issues/29). The
fitting model is very simple. There is an S0&sup2; parameter (`amp`),
an energy shift for all paths (`enot`), and a volumetric lattice
expansion coefficient (`alpha`). The &sigma;&sup2; values for all paths
were computed using the correlated Debye model and a temperature of
10K, except for the first shell, which has its own &sigma;&sup2;
variable (`ss1`).

The fit included 4 coordination shells, which includes several
collinear multiple scattering paths of the same distance as the fourth
shell single scattering path.

`amp` and `alpha` are unitless. `enot` is eV, `ss1` is &Aring;&sup2;, and
`thetad` is K.

Best fit values
---------------

|model|alpha|amp|enot|ss1|thetad|
|:----|:----|:--|:---|:--|:-----|
|feff6|-0.00074(92)|0.96(4)|4.97(49)|0.00382(33)|253(22)|
|noSCF|-0.00046(90)|0.95(4)|5.71(48)|0.00400(33)|239(19)|
|withSCF(3)|-0.00077(104)|0.94(5)|3.45(56)|0.00402(38)|241(22)|
|withSCF(4)|-0.00076(104)|0.94(5)|3.54(56)|0.00402(38)|242(22)|
|withSCF(5)|-0.00077(104)|0.94(5)|3.40(56)|0.00402(38)|241(22)|
|withSCF(5.5)|-0.00077(105)|0.94(5)|3.41(56)|0.00402(38)|241(22)|
|withSCF(6)|-0.00076(104)|0.94(5)|3.46(56)|0.00402(38)|241(22)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|1444.2957|54.3832|0.0145|
|noSCF|1414.0154|53.2430|0.0142|
|withSCF(3)|1820.7826|68.5594|0.0182|
|withSCF(4)|1814.3186|68.3160|0.0182|
|withSCF(5)|1816.7825|68.4088|0.0182|
|withSCF(5.5)|1823.5990|68.6654|0.0183|
|withSCF(6)|1819.3955|68.5071|0.0182|


Fits
----

| feff6 | no SCF | SCF, R=3 | SCF, R=4 | SCF, R=5 | SCF, R=5.5 | SCF, R=6 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_withSCF_3.png)| ![fit with feff8, SCF, R=4](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_withSCF_4.png)| ![fit with feff8, SCF, R=5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_withSCF_5.png)| ![fit with feff8, SCF, R=5.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_withSCF_5.5.png)| ![fit with feff8, SCF, R=6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/Copper/scf/fit_withSCF_6.png)|

Discussion
----------

We start with copper because, well, it's copper.  Any discussion of
XAS theory starts with copper.  It's a tradition!

In fact, we expect copper to be a null result.  There is no reason to
expect that charge transfer and self-cosistency would have much effect
on a monoatomic material.  That expectation is borne out.

The fitting parameters are constant well within their uncertainties
and across all theory models.  The statistical parameters also do not
change much across the models.  Amusingly, reduced &chi;&sup2; and
R-factor are a bit smaller _without_ the use of self-consistency.

_____


NiO
===

The sample was NiO powder prepared by my colleague Neil Hyatt
(University of Sheffield) and checked by him for phase purity. The
powder was mixed with polyethylene glycol and pressed into a pellet to
make a edge step of 0.78. The data were measured by Bruce at NSLS
beamline X23A2 and will be appearing in an upcoming article in Journal
of Synchrotron Radiation. The simple fiting model to this rocksalt
structure included a S0&sup2; parameter (`amp`), an energy shift
(`enot`), and a volumetric lattice expansion coefficient (`alpha`).

The fit included 4 coordination shells, 2 with O and 2 with Ni. There
are several collinear multiple scattering paths at the same distance
as the fourth shell Ni scatterer. Each shell has its own &sigma;&sup2;
parameter (`sso`, `ssni`, `sso2`, and `ssni2`, respectively.).

`amp` and `alpha` are unitless. `enot` is eV. `sso`, `ssni`, `sso2`,
and `ssni2` are &Aring;&sup2;.


Best fit values
---------------

|model|alpha|amp|enot|ssni|ssni2|sso|sso2|
|:----|:----|:--|:---|:---|:----|:--|:---|
|feff6|0.00062(146)|0.71(5)|-1.22(54)|0.00546(56)|0.00714(95)|0.00437(120)|0.04205(3218)|
|noSCF|0.00050(152)|0.68(5)|2.49(56)|0.00534(58)|0.00715(101)|0.00468(131)|0.03946(2918)|
|withSCF(2.5)|-0.00021(148)|0.71(4)|-7.34(54)|0.00554(56)|0.00726(97)|0.00468(123)|0.03146(2038)|
|withSCF(3)|-0.00073(145)|0.71(4)|-7.95(53)|0.00555(55)|0.00715(95)|0.00456(119)|0.03368(2237)|
|withSCF(3.7)|-0.00068(145)|0.71(4)|-7.94(53)|0.00555(55)|0.00716(95)|0.00457(119)|0.03344(2213)|
|withSCF(4.2)|-0.00010(149)|0.71(4)|-7.29(55)|0.00554(56)|0.00727(98)|0.00470(124)|0.03099(1996)|
|withSCF(4.7)|-0.00023(148)|0.71(4)|-7.31(54)|0.00554(56)|0.00725(97)|0.00466(123)|0.03167(2060)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|27430.3658|1347.4609|0.0215|
|noSCF|29860.6446|1466.8434|0.0234|
|withSCF(2.5)|28069.2786|1378.8462|0.0220|
|withSCF(3)|26875.8980|1320.2238|0.0211|
|withSCF(3.7)|26950.4623|1323.8866|0.0211|
|withSCF(4.2)|28301.4677|1390.2520|0.0222|
|withSCF(4.7)|28050.1096|1377.9046|0.0220|

Fits
----

| feff6 | no SCF | SCF, R=2.5 | SCF, R=3 | SCF, R=3.7 | SCF, R=4.2 | SCF, R=4.7 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=2.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_withSCF_2.5.png)| ![fit with feff8, SCF, R=3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_withSCF_3.png)| ![fit with feff8, SCF, R=3.7](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_withSCF_3.7.png)| ![fit with feff8, SCF, R=4.2](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_withSCF_4.2.png)| ![fit with feff8, SCF, R=4.7](https://raw.githubusercontent.com/bruceravel/SCFtests/master/NiO/scf/fit_withSCF_4.7.png)|


Discussion
----------

NiO was chosen as the second example because it constitutes the
smallest added complexity compared to copper.  NiO is a rocksalt
structure, so it is highly ordered and the local configuration around
the Ni atom is very well known.  With an oxygen ligand, there should
be some charge transfer.

With the exception of the E0 parameter, all of the parameters are
constant well within their error bars.  The statistical parameters are
unchanged from model to model.

This is the first example of dependence of the E0 parameter on
theoretical model.  The ultimate value of Feff's threshold energy
depends the model.  The starting condition is not the same in _Feff6_
as in _Feff8_ without self-consistency.  This is seen by the 3.3 eV
shift in fitted E0 value.  Furthermore, the threshold changes as
charge is transfered and self-consistency is reached.  This results in
a -6 eV shift relative to _Feff6_.

My standard explanation of the E0 fitting parameter when I am teaching
EXAFS is that it is the parameter that lines up the zero of wavenumber
in the data with the zero of wavenumber in the theory.  As such, it is
hard to say that one of these E0 results is &ldquo;better&rdquo; than
the others.

One might hope that improvements in theory would lead to a fitted E0
parameter of 0 when the edge is chosen at the inflection point of the
rising edge of the XAS data.  While that might be true, we aren't
there yet with _Feff8_.  See [the conclusion](#conclusion) for more
discussion.


_____


FeS2
=========

This is one of
[my standard teaching examples](https://github.com/bruceravel/XAS-Education/tree/master/Examples/FeS2).
It’s good for teaching as it is fairly simple – it’s cubic – but it
has a bit of structure and two kinds of scatterers. The data are taken
from
[Matt’s online collection of references](http://cars.uchicago.edu/~newville/ModelLib/search.html).

The model includes a S0&sup2; parameter (`amp`), an energy shift (`enot`),
and a volumetric lattice expansion coefficient (`alpha`). The first
and second shell S scatterers each get a &sigma;&sup2; parameter (`ss` and
`ss2`). The third shell of S atoms only contains 2 scatterers. In
practice, floating its &sigma;&sup2; parameter independently does not
yeild a statistical improvment to the fit, so the `ss2` parameter is
used for the third shell &sigma;&sup2;. Finally a &sigma;&sup2; parameter is
floated for the Fe shell.

The fitting model includes a variety of multiple scattering paths,
including a triangle between the first shell S and the fourth shell
Fe, and four paths that bounce around among first shell S atoms.

`amp` and `alpha` are unitless. `enot` is eV. `ss`, `ss2`, and `ssfe`
are &Aring;&sup2;.

Best fit values
---------------

|model|alpha|amp|enot|ss|ss2|ssfe|
|:----|:----|:--|:---|:--|:--|:---|
|feff6|0.00092(126)|0.69(2)|2.77(42)|0.00296(41)|0.00366(106)|0.00484(50)|
|noSCF|0.00183(171)|0.65(3)|7.01(57)|0.00294(57)|0.00386(151)|0.00471(68)|
|withSCF(3)|0.00219(191)|0.68(3)|-2.01(63)|0.00311(63)|0.00422(172)|0.00495(77)|
|withSCF(3.6)|0.00212(188)|0.68(3)|-2.15(62)|0.00311(62)|0.00423(170)|0.00495(76)|
|withSCF(4)|0.00212(191)|0.68(3)|-2.17(63)|0.00311(63)|0.00423(172)|0.00494(77)|
|withSCF(5.3)|0.00216(194)|0.68(4)|-1.92(64)|0.00310(64)|0.00421(175)|0.00493(78)|
|withSCF(5.5)|0.00216(194)|0.68(4)|-1.88(64)|0.00310(64)|0.00421(175)|0.00493(78)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|2052.3016|146.4407|0.0064|
|noSCF|3783.2180|269.9491|0.0119|
|withSCF(3)|4639.2799|331.0329|0.0146|
|withSCF(3.6)|4502.7226|321.2889|0.0141|
|withSCF(4)|4634.9046|330.7207|0.0145|
|withSCF(5.3)|4778.2793|340.9511|0.0150|
|withSCF(5.5)|4798.0987|342.3653|0.0151|


Fits
----

| feff6 | no SCF | SCF, R=3 | SCF, R=3.6 | SCF, R=4 | SCF, R=5.3 | SCF, R=5.5 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_withSCF_3.png)| ![fit with feff8, SCF, R=3.6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_withSCF_3.6.png)| ![fit with feff8, SCF, R=4](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_withSCF_4.png)| ![fit with feff8, SCF, R=5.3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_withSCF_5.3.png)| ![fit with feff8, SCF, R=5.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/FeS2/scf/fit_withSCF_5.5.png)|


Discussion
----------

This is just slightly more complex than NiO.  It is diatomic, but with
a slightly less orderly structure than NiO.  Again, all parameters
except for E0 are consistent within uncertainty, although the &alpha;
parameter does show some correclation with E0.  All other parameters
are essentially unchanged.

The E0 parameter, with self-consistency, is equally far from 0 as for
_Feff6_, although with a sign change.

There are a small handful of small MS paths with half-path-lengths
within the fitting range but which are not included in this fit.  This
may account for the increase in reduced &chi;&sup2; and R-factor
between _Feff6_ and _Feff8_.

_____

UO2
===

![Uraninite](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/UO2.png)

The data are the UO2 shown in Shelly’s paper on *Reduction of
Uranium(VI) by Mixed Iron(II)/Iron(III) Hydroxide (Green Rust): 
Formation of UO2 Nanoparticles*:
[`http://dx.doi.org/10.1021/es0208409`](http://dx.doi.org/10.1021/es0208409)

This is an interesting test as it is an f-electron system.

The fitting model follows rather closely to what is described in that
paper, particularly the content of Table 2, although I allow S0&sup2; to
float (`amp`). Along with an energy shift (`enot`), a &Delta;R and
&sigma;&sup2; for the first shell O (`dro` and `sso`), a &Delta;R and
&sigma;&sup2; for the second shell U (`dru` and `ssu`), and a &Delta;R and
&sigma;&sup2; for the third shell O (`dro2` and `sso2`), there is a
parameter for the number of U scatterers (`nu`).

The model includes the same 6 paths given in Table 2 of Shelly’s
paper.

`amp` is unitless. `enot` is eV. `dro`, `dru`, and `dro2` are
&Aring;. `sso`, `ssu`, and `sso2` are &Aring;2.


Best fit values
---------------

|model|amp|dro|dro2|dru|enot|nu|sso|sso2|ssu|
|:----|:--|:--|:---|:--|:---|:--|:--|:---|:--|
|feff6|0.87(11)|-0.022(14)|-0.055(24)|0.005(11)|4.87(136)|11.43(481)|0.00939(213)|0.01060(440)|0.00488(247)|
|noSCF|0.84(11)|-0.023(15)|-0.024(32)|0.001(12)|8.15(146)|9.27(416)|0.00872(221)|0.01061(618)|0.00382(273)|
|withSCF(3)|0.84(10)|-0.026(13)|-0.013(28)|-0.002(11)|1.63(129)|9.21(376)|0.00894(209)|0.00976(511)|0.00393(250)|
|withSCF(4)|0.84(10)|-0.026(13)|-0.013(29)|-0.003(11)|2.08(130)|9.16(373)|0.00892(209)|0.00972(513)|0.00389(250)|
|withSCF(5)|0.84(10)|-0.026(13)|-0.012(28)|-0.003(11)|1.72(129)|9.18(373)|0.00893(208)|0.00969(508)|0.00391(249)|
|withSCF(5.5)|0.84(10)|-0.026(13)|-0.012(28)|-0.003(11)|1.62(129)|9.17(372)|0.00894(208)|0.00970(509)|0.00391(249)|
|withSCF(6)|0.84(10)|-0.026(13)|-0.012(29)|-0.003(11)|1.71(129)|9.16(372)|0.00893(208)|0.00971(510)|0.00390(249)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|166.2736|22.0712|0.0160|
|noSCF|188.4320|25.0125|0.0181|
|withSCF(3)|169.5918|22.5116|0.0163|
|withSCF(4)|169.9560|22.5600|0.0163|
|withSCF(5)|169.1192|22.4489|0.0163|
|withSCF(5.5)|169.1306|22.4504|0.0163|
|withSCF(6)|169.2412|22.4651|0.0163|



Fits
----

| feff6 | no SCF | SCF, R=3 | SCF, R=4 | SCF, R=5 | SCF, R=5.5 | SCF, R=6 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_withSCF_3.png)| ![fit with feff8, SCF, R=4](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fitUO2/scf/fit_withSCF_4.png)| ![fit with feff8, SCF, R=5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_withSCF_5.png)| ![fit with feff8, SCF, R=5.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_withSCF_5.5.png)| ![fit with feff8, SCF, R=6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/UO2/scf/fit_withSCF_6.png)|


Discussion
----------

The first thing to notice about UO2 is that the statistical parameters
of the fit are completely unchanged between theory models.

This E0 parameter is the first one that behaves in the expected way
&ndash; with self-consistency and charge transfer, the fitted E0 ends
up closer to 0.  Perhaps this is a hint that self-consistency is
important for f-electron systems.

All of the other fitting parameters are unchanged within their
uncertainties.  One parameter merits a bit more discussion.  In the
paper cited above, the fitten value of `nu`, i.e. the partial
occupancy of the U atom in the second scattering shell, is used to say
something about the size of the uraninite nanoparticles generated by
the reduction process.  While the fitted value of `nu` does not change
outside of its very large uncertainty, it does change substantively.
This would likely effect the interpretation of the fitting results in
the context of the reduction process.

_____


BaZrO3
======

![The perovskite structure.](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/perovskite.png)

In a short paper on the Zr edge of BaZrO3,
[`http://dx.doi.org/10.1016/0921-4526(94)00654-E`](http://dx.doi.org/10.1016/0921-4526(94)00654-E),
Haskel et al.  proposed that shortcomings of _feff_’s potential model
could be accommodated by floating an energy shift parameter for each
scatterer species. The concept is that doing so approximates the
effect of errors in the scattering phase shifts.

The data are the same as in that paper, although the fitting model is
slightly different. Rather than floating &Delta;R parameters for each
shell, I used a volumetric expansion coefficient (`alpha`). Along with
S0&sup2; (`amp`), there are energy shifts for each scatterer (`enot`,
`ezr`, and `eba`) and &sigma;&sup2; parameters for each scatterer (`sso`,
`sszr`, and `ssba`. The fourth shell O is included in the fit. It gets
a &sigma;&sup2; (`sso2`) but uses the energy shift for the O scatterer.

BaZrO3 is a true perovskite. Zr sites in the octahedral B site. A
variety of collinear multiple scattering paths at the distance of the
third shell Zr scatterer are included in the fit. The energy shifts
are parameterized as described in the paper.

`amp` and `alpha` are unitless. `enot`, `ezr`, and `eba` are
eV. `sso`, `sszr`, `ssba`, and `sso2` are &Aring;&sup2;.

Best fit values
---------------

|model|alpha|amp|eba|enot|ezr|ssba|sso|sso2|sszr|
|:----|:----|:--|:--|:---|:--|:---|:--|:---|:---|
|feff6|-0.00032(85)|1.22(7)|-9.906(567)|-8.55(57)|-5.597(1717)|0.00561(37)|0.00403(70)|0.00908(253)|0.00413(33)|
|noSCF|0.00044(86)|1.07(6)|-3.901(589)|-2.32(58)|0.946(1886)|0.00530(38)|0.00361(70)|0.00791(242)|0.00369(34)|
|withSCF(3)|-0.00007(72)|1.13(5)|-10.768(469)|-10.52(47)|-6.682(1580)|0.00561(32)|0.00382(58)|0.00855(208)|0.00362(28)|
|withSCF(4)|-0.00007(74)|1.13(5)|-11.026(482)|-10.60(48)|-6.794(1618)|0.00559(33)|0.00380(59)|0.00850(213)|0.00362(28)|
|withSCF(5)|-0.00007(73)|1.13(5)|-11.094(479)|-10.81(48)|-7.057(1604)|0.00561(33)|0.00381(59)|0.00850(211)|0.00363(28)|
|withSCF(5.5)|-0.00007(73)|1.13(5)|-10.950(477)|-10.77(48)|-7.050(1594)|0.00562(33)|0.00382(59)|0.00850(210)|0.00364(28)|
|withSCF(6)|-0.00005(73)|1.13(5)|-10.705(474)|-10.49(48)|-6.726(1590)|0.00562(33)|0.00382(59)|0.00851(208)|0.00364(28)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|8979.2479|555.6561|0.0108|
|noSCF|9536.0604|590.1130|0.0114|
|withSCF(3)|6579.0004|407.1234|0.0079|
|withSCF(4)|6898.9084|426.9200|0.0083|
|withSCF(5)|6837.1517|423.0984|0.0082|
|withSCF(5.5)|6790.5892|420.2170|0.0081|
|withSCF(6)|6690.0972|413.9983|0.0080|



Fits
----

| feff6 | no SCF | SCF, R=3 | SCF, R=4 | SCF, R=5 | SCF, R=5.5 | SCF, R=6 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=3](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_withSCF_3.png)| ![fit with feff8, SCF, R=4](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_withSCF_4.png)| ![fit with feff8, SCF, R=5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_withSCF_5.png)| ![fit with feff8, SCF, R=5.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_withSCF_5.5.png)| ![fit with feff8, SCF, R=6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/BaZrO3/scf/fit_withSCF_6.png)|


Discussion
----------

In the paper cited above, the authors speculate that inaccuracies in
Feff's potential model can be accommodated by allowing separate E0
parameters to float for each kind of scatterer.  In the paper, the
claim is that the &Delta;R parameters used to model low temperature
BaZrO3 data correctly follow the trends seen in high temperature XRD
data on the same material.

I didn't quite use the same fitting model as in that paper.  Instead
of a variety of &Delta;R parameters, I used a single isotropic
expansion coefficient, &alpha;.  With just one data set, the fit using
many &Delta;R parameters was not stable.

The hope, in this case, is that self-consistency and charge transfer
would make all the E0 parameters close to 0 **and** remove the need
for multiple E0 parameters in the fit.  Neither of those hopes were
realized.  The E0 parameters in the self-consistent fits were not much
different from the results of the _Feff6_ fit and none of them ended
up near 0.

Other fitting parameters were, as in other materials, consistent
within uncertainties.  In this case, the reduced &chi;&sup2; and
R-factor were a bit lower with self-consistency with relative
reductions on the same scale as the increases in FeS2 and NiO.

_____


bromoadamantane
===============

![ 1-bromoadamantane](https://raw.githubusercontent.com/bruceravel/SCFtests/master/bromoadamantane/bromoadamantane.png)

The data are 1-bromoadamantane. Adamantane is a cycloalkane, meaning
that it is a hydrocarbon with rings of carbon atoms. It is also a
diamondoid, meaning that it is a strong, stiff, 3D network of covalent
bonds. 1-bromoadamantane has one hydrogen atom replaced by a bromine
atom.

The material was supplied by my colleague Alessandra Leri of Manhattan
Marymount College in the form of a white powder. This powder was
spread onto kapton tape which was folded to make a sample with an edge
step of about 1.7. The data were measured by Bruce at NSLS beamline
X23A2.

This is an interesting test case because it is a molecule (thus the
entire molecule can be included in the self-consistency calculation)
and because there is measureable scattering from the neighboring
hydrogen atoms. While the &sigma;&sup2; of the hydrogen scatterers is
not well-determined, the fit is statistically significantly worse when
the hydrogen scatterers are excluded.

The fit includes the nearest neighbor C, the next three C atoms, and
the neighboring 6 hydrogen atoms. The DS triangle paths involving the
first and second neighbor C atoms are also included. The fitting model
assumes that the adamanatane anion is very rigid compared to the Br-C
bond. Thus, the formula explained in
[`http://dx.doi.org/10.1088/1742-6596/190/1/012026`](http://dx.doi.org/10.1088/1742-6596/190/1/012026)
is used to constrain the second neighbor C distance to the first
neighbor C &Delta;R parameter.


Best fit values
---------------

|model|amp|delr|drh|enot|ss|ssh|
|:----|:--|:---|:--|:---|:--|:--|
|feff6|1.57(24)|0.01826(1456)|0.041(20)|5.95(181)|0.00659(183)|0.00159(266)|
|noSCF|1.24(22)|0.01682(1608)|0.079(24)|12.03(169)|0.00554(206)|0.00008(310)|
|withSCF(8)|1.33(20)|0.01762(1408)|0.073(25)|1.54(156)|0.00560(180)|0.00143(319)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|7743.8859|1493.2531|0.0207|
|noSCF|10540.8219|2032.5862|0.0281|
|withSCF(8)|8632.0582|1664.5194|0.0230|


Fits
----


| feff6 | no SCF | SCF, R=8 |
|-------|--------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/bromoadamantane/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/bromoadamantane/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=8](https://raw.githubusercontent.com/bruceravel/SCFtests/master/bromoadamantane/scf/fit_withSCF_8.png)|


Discussion
----------

In June 2015, the
[following quote](http://www.mail-archive.com/ifeffit@millenia.cars.aps.anl.gov/msg05040.html)
appeared on the Ifeffit mailing list:

      There are some demonstrated cases where _Feff8_ is slightly
      better than _Feff6_ at modeling EXAFS. The most notable cases
      are when H is in the input file -- _Feff6_ is terrible at this.

Bromoadamantane is a case where scattering from H atoms can be seen
inthe EXAFS data.  The statistical parameters are all much smaller
when the H SS path is included in the fit compared to fits which
exclude that scattering path.  This is true even though the
&sigma;&sup2; value for the H SS path is ill-determined &ndash; its
uncertainty is such that &sigma;&sup2; for H is not positive-definite.
This is likely because the small mass of the H atom makes its partial
pair distribution function highly non-Gaussian.  The approximation of
a simple &sigma;&sup2; to model this distribution is not all that
good.  Despite the ill-defined &sigma;&sup2;, the &Delta;R is well
defined.

The parameters of the first shell C scatterer are quite well defined
and consistent accross theory models.  S0&sup2; varies a bit outside
of its uncertainty, as does &Delta;R for the H atom.  The statistical
parameters for the fits with self-consistency and _Feff6_ are
basically indistinguishable.

The fitting model is clearly inadequate in the region from 2
&Aring; to 2.5 &Aring;.  The likely cause of this is the fairly rigid
constrain placed on the parameters of the second shell C scatterer.
This fitting model should be re-examined by relaxing this constraint.
Future work!

So, is _Feff6_ &ldquo;terrible&rdquo; at handling H scatterers?  The
answer may be &ldquo;yes&rdquo; and may be &ldquo;no&rdquo;, but these
data on bromoadamantane don't suggest that it is any worse than
_Feff8_.


_____


uranyl hydrate
==============

![The uranyl motif from sodium uranyl triacetate.](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/uranyl.png)

The data are the hydrated uranyl hydrate shown in Shelly’s paper on
*X-ray absorption fine structure determination of pH-dependent
U-bacterial cell wall interactions*,
[`http://dx.doi.org/10.1016/S0016-7037(02)00947-X`](http://dx.doi.org/10.1016/S0016-7037(02)00947-X)

This is an interesting test case because it involves very short
~1.78&Aring; oxygenyl bonds in an f-electron system.

The `AFOLP` card was used to run _feff6_. The `FOLP` card with a value
of 0.9 for each potential was used to get _feff8.5_ to run to
completion.

Following the lead of that paper, feff was run on the crystal sodium
uranyl triacetate. The relevant bit of the structure is shown in the
figure. For the fitting model, scattering paths related to the axial
and equatorial O atoms (red balls) are used in the fit. Other paths
are unused. The parameterization given in Tables 2 and 5 is used in
this fit.

There is an S0&sup2; (`amp`) and an energy shift (`enot`). The axial
and equatorial oxyegn atoms each get a &Delta;R (`deloax` and
`deloeq`) and a &sigma;&sup2; (`sigoax` and `sigoeq`).

`amp` is unitless. `enot` is eV. `deloax` and `deloeq` are
&Aring;. `sigoax` and `sigoeq` are &Aring;&sup2;.

Best fit values
---------------

|model|amp|deloax|deloeq|enot|sigoax|sigoeq|
|:----|:--|:-----|:-----|:---|:-----|:-----|
|feff6|0.93(4)|0.03504(396)|-0.04278(770)|10.63(60)|-0.00007(53)|0.00726(94)|
|noSCF|1.04(6)|0.03684(523)|-0.05319(975)|11.32(78)|0.00032(72)|0.00699(118)|
|withSCF(2.5)|1.08(6)|0.04165(548)|-0.04475(972)|3.45(81)|0.00074(73)|0.00692(115)|
|withSCF(2.9)|1.08(6)|0.04172(547)|-0.04485(971)|3.50(81)|0.00074(73)|0.00691(115)|
|withSCF(4.0)|1.08(6)|0.04144(545)|-0.04455(969)|3.59(81)|0.00075(73)|0.00694(115)|
|withSCF(5.2)|1.08(6)|0.04154(545)|-0.04473(967)|3.66(81)|0.00074(72)|0.00693(114)|
|withSCF(6.8)|1.08(6)|0.04163(545)|-0.04478(968)|3.63(81)|0.00074(72)|0.00693(114)|

Statistics
----------

|model|&chi;&sup2;|reduced &chi;&sup2;| R-factor |
|:----|---------:|-------------:|--------------:|
|feff6|37.6972|6.0758|0.0027|
|noSCF|69.0909|11.1356|0.0049|
|withSCF(2.5)|71.0295|11.4480|0.0050|
|withSCF(2.9)|70.8922|11.4259|0.0050|
|withSCF(4.0)|70.4038|11.3472|0.0050|
|withSCF(5.2)|70.2351|11.3200|0.0050|
|withSCF(6.8)|70.3644|11.3408|0.0050|



Fits
----

| feff6 | no SCF | SCF, R=2.5 | SCF, R=2.9 | SCF, R=4 | SCF, R=5.2 | SCF, R=6.8 |
|-------|--------|----------|----------|----------|----------|----------|
|![fit with feff6](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_feff6.png) | ![fit with feff8 no SCF](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_noSCF.png) | ![fit with feff8, SCF, R=2.5](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_withSCF_2.5.png)| ![fit with feff8, SCF, R=2.9](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_withSCF_2.9.png)| ![fit with feff8, SCF, R=4](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_withSCF_4.png)| ![fit with feff8, SCF, R=5.2](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_withSCF_5.2.png)| ![fit with feff8, SCF, R=6.8](https://raw.githubusercontent.com/bruceravel/SCFtests/master/uranyl/scf/fit_withSCF_6.8.png)|


Discussion
----------

The most interesting part of this fit is the extremely short, double
bonded, axial oxygen scattering path.  With such an extremely rigid
bond, &sigma;&sup2; is hard to determine.  Even the most sensible
result in the table above gives an answer that is barely
positive-definite.

Beyond that parameter, the story here is, by now, familiar.  Most
fitting parameters are consistent over the theory models.  This is one
of the cases where the statistical parameters are slightly better for
_Feff6_ than for any of the _Feff8_ fits.

Like with UO2, the E0 values of the self-consistent fits are what one
hopes to find.  They are much closer to zero when the edge energy of
the data is chosen at the inflection point of the rising edge.  Is
this a trend suggesting that self-consistency is important for setting
the energy scale of f-electron systems?

Also like tghe UO2 example, the SO&sup2; value is a bit different
using _Feff6_ and _Feff8_, which could have an impact on the
interpretation of the data.  It is, however, correlated with the axial
&sigma;&sup2; result.

_____


Conclusion
==========

Blah blah