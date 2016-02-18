


from os.path import realpath, exists, join

from larch import (Group, Parameter, use_plugin_path)
use_plugin_path('io')
from xdi import read_xdi
from columnfile import write_ascii
use_plugin_path('xafs')
from feffit import feffit_dataset, feffit_transform, feffit, feffit_report
from feffdat import feffpath, _ff2chi
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

    data = read_xdi(join(self.path, 'bromoadamantane.chik'), _larch=self._larch)

    gds = Group(amp     = Parameter(0.9,       vary=True,  _larch=self._larch),
                enot    = Parameter(4.01,      vary=True,  _larch=self._larch),
                delr    = Parameter(1e-7  ,    vary=True,  units='AA',   decimals=3, _larch=self._larch),
                ss      = Parameter(0.003,     vary=True,  units='AA^2', _larch=self._larch),
                c3      = Parameter(1e-7,      vary=False, _larch=self._larch),
                _larch=self._larch  )
    if not firstshell:
        gds.brc     = Parameter(expr = '1.9521+delr',  units='AA',  _larch=self._larch)
        #gds.phir    = Parameter(109.29960 * 3.141592653589793 / 180,   vary=False, _larch=self._larch)
        gds.cc      = Parameter(1.53780,   vary=False, _larch=self._larch)
        #gds.tanbeta = Parameter(expr = '(brc+cc)*tan(phir/2) / (brc-cc)', _larch=self._larch)
        #gds.beta    = Parameter(expr = 'atan(tanbeta)', _larch=self._larch)
        #gds.brc2    = Parameter(expr = '(brc-cc)*cos(phir/2)/cos(beta)',  units='AA', _larch=self._larch)
        gds.drh     = Parameter(0.04,      vary=True,  units='AA', decimals=3, _larch=self._larch)
        gds.ssh     = Parameter(0.005,     vary=True,  units='AA^2', _larch=self._larch)
        gds.ss2     = Parameter(expr = 'ss*(brc2/brc)**2', units ='AA^2', _larch=self._larch)
        gds.drc     = Parameter(0.04,      vary=True,  units='AA', decimals=3, _larch=self._larch)
        gds.brc2    = Parameter(expr = '2.8565+drc',   units='AA', decimals=3, _larch=self._larch)
        
    paths = list()
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")),
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = 'ss',
                          deltar = 'delr',
                          third  = 'c3', _larch=self._larch))

    if not firstshell:
        paths.append(feffpath(realpath(join(folder, "feff0002.dat")),
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss2',
                              #deltar = 'brc2-2.8565',
                              deltar = 'drc',_larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0003.dat")),
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssh',
                              deltar = 'drh', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0004.dat")),
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = '(ss+ss2)/2',
                              deltar = '(brc+brc2+cc)/2 - 3.173', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0005.dat")),
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = '(ss+ss2)/2',
                              deltar = '(brc+brc2+cc)/2 - 3.173', _larch=self._larch))

    rx  = 3
    if firstshell: rx  = 1.83

    trans = feffit_transform(kmin=3, kmax=11, kw=(2,1,3), dk=1, window='hanning', rmin=1, rmax=3, _larch=self._larch)
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
    with open(join(self.folder, fittest,'fit_'+which+shells+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'plot.mustache', # gnuplot mustache file
                                        {'material': 'bromoadamantane',
                                         'model': which,
                                         'fittest': fittest,
                                         'shells': shells,
                                         'kmin': 3,
                                         'kmax': 13,
                                         'rmin': 1,
                                         'rmax': rx,
                                         'offset': 0.2,
                                     } ))

    return fit
#end def
