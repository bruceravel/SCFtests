## see http://dx.doi.org/10.1021/es0208409


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

    data = read_xdi(join(self.path, 'UO2.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(1,      vary=True, _larch=self._larch),
                enot   = Parameter(1e-7,   vary=True, _larch=self._larch),
                sso    = Parameter(0.003,  vary=True, _larch=self._larch),
                ssu    = Parameter(0.003,  vary=True, _larch=self._larch),
                sso2   = Parameter(0.003,  vary=True, _larch=self._larch),
                dro    = Parameter(1e-7,   vary=True, _larch=self._larch),
                dru    = Parameter(1e-7,   vary=True, _larch=self._larch),
                dro2   = Parameter(1e-7,   vary=True, _larch=self._larch),
                nu     = Parameter(12,     vary=True, _larch=self._larch),
                no2    = Parameter(expr='2*nu',       _larch=self._larch),
                _larch=self._larch  )

    paths = list() 
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")), # 1st shell O SS
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = 'sso',
                          deltar = 'dro', _larch=self._larch))
    # paths.append(feffpath(realpath(join(folder, "feff0002.dat")), # triangle in first shell
    #                       s02    = 'amp',
    #                       e0     = 'enot',
    #                       sigma2 = 'sso*(1+sqrt(3))**2',
    #                       deltar = 'dro*(1+sqrt(3))/2', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0003.dat")), # 2nd shell U SS
                          degen  = 1,
                          s02    = 'amp*nu',
                          e0     = 'enot',
                          sigma2 = 'ssu',
                          deltar = 'dru', _larch=self._larch))
    # paths.append(feffpath(realpath(join(folder, "feff0004.dat")), # 1st shell, longer triangle
    #                       s02    = 'amp',
    #                       e0     = 'enot',
    #                       sigma2 = 'sso*(1+sqrt(2/3))**2',
    #                       deltar = '(1+sqrt(2/3))*dro', _larch=self._larch))
    # paths.append(feffpath(realpath(join(folder, "feff0005.dat")), # 1st shell, longer U-O-U triangle
    #                       degen  = 1,
    #                       s02    = 'amp*nu',
    #                       e0     = 'enot',
    #                       sigma2 = 'sso*ssu/2',
    #                       deltar = '(1+sqrt(2/3))*dro', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0006.dat")), # 3rd shell O SS
                          degen  = 1,
                          s02    = 'amp*no2',
                          e0     = 'enot',
                          sigma2 = 'sso2',
                          deltar = 'dro2', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0007.dat")), # 1st shell, non-forward linear through absorber
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = '2*sso2',
                          deltar = '2*dro2', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0008.dat")), # 1st shell forward through absorber
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = '2*sso',
                          deltar = '2*dro', _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0009.dat")), # rattle in 1st shell
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = '2*sso',
                          deltar = '2*dro', _larch=self._larch))


    trans = feffit_transform(kmin=3, kmax=11, kw=(2,1,3), dk=1, window='hanning', rmin=1.25, rmax=4.3, _larch=self._larch)
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
    with open(join('UO2','fit_'+which+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'fit.mustache', # gnuplot mustache file
                                        {'material': 'UO2',
                                         'model': which,
                                         'kmin': 3,
                                         'kmax': 11,
                                         'rmin': 1.25,
                                         'rmax': 4.3,
                                         'offset': 0.75,
                                     } ))

    return fit
#end def
