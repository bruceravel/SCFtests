


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

def do_fit(self, which):

    if which == 'testrun':
        folder = self.testrun
    elif which == 'baseline':
        folder = self.baseline
    else:
        folder = realpath(join(self.folder, 'baseline', which))
    #endif

    data = read_xdi(join(self.path, 'FeS2.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(1,      vary=True, _larch=self._larch),
                enot   = Parameter(1e-7,   vary=True, _larch=self._larch),
                alpha  = Parameter(1e-7,   vary=True, _larch=self._larch),
                ss     = Parameter(0.003,  vary=True, _larch=self._larch),
                ss2    = Parameter(0.003,  vary=True, _larch=self._larch),
                ss3    = Parameter(expr='ss2',        _larch=self._larch),
                ssfe   = Parameter(0.003,  vary=True, _larch=self._larch),
                _larch=self._larch  )

    paths = list() 
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")), # 1st shell S SS
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = 'ss',
                          deltar = 'alpha*reff', _larch=self._larch))
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


    trans = feffit_transform(kmin=3, kmax=12.956, kw=(2,1,3), dk=1, window='hanning', rmin=1.2, rmax=4.2, _larch=self._larch)
    dset  = feffit_dataset(data=data, pathlist=paths, transform=trans, _larch=self._larch)
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = 0.6*max(dset.data.chir_mag)
        _newplot(dset.data.r,  dset.data.chir_mag+offset, xmax=8, win=2,
              xlabel=r'$R \rm\,(\AA)$', label='data',
              ylabel=r'$|\chi(R)| \rm\,(\AA^{-3})$',
              title='Fit to '+self.folder, show_legend=True, _larch=self._larch)
        _plot(dset.model.r, dset.model.chir_mag+offset, label='fit', win=2, _larch=self._larch)
        _plot(dset.data.r,  dset.data.chir_re, label='data', win=2, _larch=self._larch)
        _plot(dset.model.r, dset.model.chir_re, label='fit', win=2, _larch=self._larch)
    #end if
    
    if self.verbose:
        print feffit_report(fit, _larch=self._larch)
    #end if

    write_ascii(join(self.folder, "fit_"+which+".k"), dset.data.k, dset.data.chi, dset.model.chi,
                labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)
    write_ascii(join(self.folder, "fit_"+which+".r"), dset.data.r, dset.data.chir_mag, dset.model.chir_mag,
                dset.data.chir_re, dset.model.chir_re, labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)

    renderer = pystache.Renderer()
    with open(join('FeS2','fit_'+which+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'fit.mustache', # gnuplot mustache file
                                        {'material': 'FeS2',
                                         'model': which,
                                         'kmin': 3,
                                         'kmax': 12.956,
                                         'rmin': 1.2,
                                         'rmax': 4.2,
                                         'offset': 1,
                                     } ))

    return fit
#end def
