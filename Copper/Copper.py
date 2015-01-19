


from os.path import realpath, exists, join

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass)
use_plugin_path('io')
from columnfile import write_ascii
from xdi import read_xdi
use_plugin_path('xafs')
from feffit import feffit_dataset, feffit_transform, feffit, feffit_report
from feffdat import feffpath
use_plugin_path('wx')
from plotter import (_newplot, _plot)

import pystache

def do_fit(self, which, firstshell=False, fittest='baseline'):

    if which == 'testrun':
        folder = self.testrun
    elif which == 'baseline':
        folder = self.baseline
    else:
        folder = realpath(join(self.folder, fittest, which))
    #endif

    data = read_xdi(join(self.path, 'Copper.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(1,     vary=True,  _larch=self._larch),
                enot   = Parameter(1e-7,  vary=True,  _larch=self._larch),
                ss1    = Parameter(0.003, vary=True,  _larch=self._larch), _larch=self._larch  )

    if firstshell:
        gds.delr   = Parameter(1e-7,   vary=True, _larch=self._larch)
        dr1param   = 'delr'
    else:
        gds.thetad = Parameter(500,   vary=True,  _larch=self._larch)
        gds.temp   = Parameter(10,    vary=False, _larch=self._larch)
        gds.alpha  = Parameter(1e-7,  vary=True,  _larch=self._larch)
        dr1param   = 'alpha*reff'

    imax = 16
    if firstshell: imax = 2
    paths = list()
    for index in range(1,imax):
        nnnn = realpath(join(folder, "feff%4.4d.dat" % index))
        if not exists(nnnn):
            continue
        #end if
        if index > 1:
            sigsqr = 'sigma2_debye(temp, thetad)' 
        else:
            sigsqr = 'ss1'
        #end if
        paths.append(feffpath(nnnn,
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = sigsqr,
                              deltar = dr1param, _larch=self._larch))
    #end for

    rx  = 5.0
    if firstshell: rx  = 2.8

    trans = feffit_transform(kmin=3, kmax=15, kw=(2,1,3), dk=1, window='hanning', rmin=1, rmax=rx, _larch=self._larch)
    dset  = feffit_dataset(data=data, pathlist=paths, transform=trans, _larch=self._larch)
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = max(dset.data.chir_mag)
        _newplot(dset.data.r,  dset.data.chir_mag+offset, xmax=8,
              xlabel=r'$R \rm\,(\AA)$', label='data',
              ylabel=r'$|\chi(R)| \rm\,(\AA^{-3})$',
              title='Fit to '+self.folder, show_legend=True, _larch=self._larch)
        _plot(dset.model.r, dset.model.chir_mag+offset, label='fit', _larch=self._larch)
        _plot(dset.data.r,  dset.data.chir_re, label='data', _larch=self._larch)
        _plot(dset.model.r, dset.model.chir_re, label='fit', _larch=self._larch)
    #end if
    
    if self.verbose:
        print feffit_report(fit, _larch=self._larch)
    #end if

    shells = ''
    if firstshell: shells='_1st'

    write_ascii(join(self.folder, fittest, "fit_"+which+shells+".k"), dset.data.k, dset.data.chi, dset.model.chi,
                labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)
    write_ascii(join(self.folder, fittest, "fit_"+which+shells+".r"), dset.data.r, dset.data.chir_mag, dset.model.chir_mag,
                dset.data.chir_re, dset.model.chir_re, labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)

    renderer = pystache.Renderer()
    with open(join(self.folder, fittest, 'fit_'+which+shells+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'fit.mustache', # gnuplot mustache file
                                        {'material': 'Copper',
                                         'model': which,
                                         'fittest': fittest,
                                         'shells': shells,
                                         'kmin': 3,
                                         'kmax': 15,
                                         'rmin': 1,
                                         'rmax': rx,
                                         'offset': 2,
                                     } ))

    return fit
#end def
