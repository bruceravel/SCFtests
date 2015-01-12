## see http://dx.doi.org/10.1016/S0016-7037(02)00947-X


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

    data = read_xdi(join(self.path, 'uranyl.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(1,      vary=True,  _larch=self._larch),
                enot   = Parameter(1e-7,   vary=True,  _larch=self._larch),
                #enot   = Parameter(1e-7,   vary=True,  _larch=self._larch, min=0, max=13),
                enoteq = Parameter(expr= 'enot',     _larch=self._larch),
                deloax = Parameter(1e-7,   vary=True,  _larch=self._larch),
                deloeq = Parameter(1e-7,   vary=True,  _larch=self._larch),
                sigoax = Parameter(0.003,  vary=True,  _larch=self._larch),
                sigoeq = Parameter(0.003,  vary=True,  _larch=self._larch),
                nax    = Parameter(2.0,    vary=False, _larch=self._larch),
                neq    = Parameter(6,      vary=False, _larch=self._larch), #, min=0, max=12),
                _larch=self._larch  )

    paths = list() 
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")), # axial oxygen
                          degen  = 1,
                          s02    = 'amp*nax',
                          e0     = 'enot',
                          sigma2 = 'sigoax',
                          deltar = 'deloax', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0003.dat")), # equatorial oxygen
                          degen  = 1,
                          s02    = 'amp*neq',
                          e0     = 'enoteq',
                          sigma2 = 'sigoeq',
                          deltar = 'deloeq', _larch=self._larch))

    paths.append(feffpath(realpath(join(folder, "feff0008.dat")), # axial oxygen, rattle
                          degen  = 1,
                          s02    = 'amp*nax',
                          e0     = 'enot',
                          sigma2 = 'sigoax*4',
                          deltar = 'deloax*2', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0009.dat")), # axial oxygen, non-forward
                          degen  = 1,
                          s02    = 'amp*nax',
                          e0     = 'enot',
                          sigma2 = 'sigoax',
                          deltar = 'deloax*2', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0010.dat")), # axial oxygen, forward
                          degen  = 1,
                          s02    = 'amp*nax',
                          e0     = 'enot',
                          sigma2 = 'sigoax',
                          deltar = 'deloax*2', _larch=self._larch))




    trans = feffit_transform(kmin=3, kmax=11, kw=(2,1,3), dk=1, window='hanning', rmin=1.0, rmax=3.2, _larch=self._larch)
    dset  = feffit_dataset(data=data, pathlist=paths, transform=trans, _larch=self._larch)
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = max(dset.data.chir_mag)
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
    with open(join('uranyl','fit_'+which+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'fit.mustache', # gnuplot mustache file
                                        {'material': 'uranyl',
                                         'model': which,
                                         'kmin': 3,
                                         'kmax': 11,
                                         'rmin': 1.0,
                                         'rmax': 3.2,
                                         'offset': 1,
                                     } ))

    return fit
#end def
