


from os.path import realpath, exists, join

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass)
use_plugin_path('io')
from xdi import read_xdi
from columnfile import write_ascii
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

    data = read_xdi(join(self.path, 'FeS2.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(1,      vary=True, _larch=self._larch),
                enot   = Parameter(1e-7,   vary=True, _larch=self._larch),
                ss     = Parameter(0.003,  vary=True, _larch=self._larch), _larch=self._larch  )

    if firstshell:
        gds.delr   = Parameter(1e-7,   vary=True, _larch=self._larch)
        dr1param   = 'delr'
    else:
        gds.alpha  = Parameter(1e-7,   vary=True, _larch=self._larch)
        gds.ss2    = Parameter(0.003,  vary=True, _larch=self._larch)
        gds.ss3    = Parameter(expr='ss2',        _larch=self._larch)
        gds.ssfe   = Parameter(0.003,  vary=True, _larch=self._larch)
        dr1param   = 'alpha*reff'

    paths = list() 
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")), # 1st shell S SS
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = 'ss',
                          deltar = dr1param, _larch=self._larch))
    if not firstshell:
        paths.append(feffpath(realpath(join(folder, "feff0002.dat")), # 2nd shell S SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0003.dat")), # 3rd shell S SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss3',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0004.dat")), # 4th shell Fe SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssfe',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0005.dat")), # S-S triangle
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss*1.5',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0006.dat")), # S-Fe triangle
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss/2+ssfe',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0012.dat")), # S-S non-forward linear
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss*2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0013.dat")), # S-S forward scattering
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss*2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0014.dat")), # S-S rattle
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss*4',
                              deltar = 'alpha*reff', _larch=self._larch))


    rx  = 4.2
    if firstshell: rx  = 2.3

    trans = feffit_transform(kmin=3, kmax=12.956, kw=(2,1,3), dk=1, window='hanning', rmin=1.2, rmax=rx, _larch=self._larch)
    dset  = feffit_dataset(data=data, pathlist=paths, transform=trans, _larch=self._larch)
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = 0.6*max(dset.data.chir_mag)
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
        inp.write(renderer.render_path( 'plot.mustache', # gnuplot mustache file
                                        {'material': 'FeS2',
                                         'model': which,
                                         'fittest': fittest,
                                         'shells': shells,
                                         'kmin': 3,
                                         'kmax': 12.956,
                                         'rmin': 1.2,
                                         'rmax': rx,
                                         'offset': 1,
                                     } ))

    return fit
#end def
