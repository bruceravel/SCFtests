


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

def do_fit(self, which, firstshell=False):

    if which == 'testrun':
        folder = self.testrun
    elif which == 'baseline':
        folder = self.baseline
    else:
        folder = realpath(join(self.folder, 'baseline', which))
    #endif

    data = read_xdi(join(self.path, 'NiO.chik'), _larch=self._larch)
    if hasattr(data, 'wavenumber'):
        data.k = data.wavenumber

    gds = Group(amp    = Parameter(1,      vary=True, _larch=self._larch),
                enot   = Parameter(1e-7,   vary=True, _larch=self._larch),
                sso    = Parameter(0.003,  vary=True, _larch=self._larch), _larch=self._larch  )

    if firstshell:
        gds.delr   = Parameter(1e-7,   vary=True, _larch=self._larch)
        dr1param   = 'delr'
    else:
        gds.alpha  = Parameter(1e-7,   vary=True, _larch=self._larch)
        gds.ssni   = Parameter(0.003,  vary=True, _larch=self._larch)
        gds.sso2   = Parameter(0.003,  vary=True, _larch=self._larch)
        #gds.sso3   = Parameter(0.003,  vary=True, _larch=self._larch)
        gds.ssni2  = Parameter(0.003,  vary=True, _larch=self._larch)
        #gds.ssni3  = Parameter(0.003,  vary=True, _larch=self._larch)
        #gds.ssni4  = Parameter(0.003,  vary=True, _larch=self._larch)
        dr1param   = 'alpha*reff'

    paths = list() 
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")), # 1st shell O SS
                          s02    = 'amp',
                          e0     = 'enot',
                          sigma2 = 'sso',
                          deltar = dr1param, _larch=self._larch))
    if not firstshell:
        paths.append(feffpath(realpath(join(folder, "feff0002.dat")), # 2nd shell Ni SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssni',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0003.dat")), # O-O triangle
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = '1.5*sso',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0004.dat")), # O-Ni triangle
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'sso+ssni/2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0005.dat")), # 3rd shell O SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'sso2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0006.dat")), # 4th shell Ni SS
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssni2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0007.dat")), # O-O non-forward linear
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'sso*2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0008.dat")), # O-Ni forward scattering
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssni2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0009.dat")), # O-O forward through absorber
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'sso*2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0011.dat")), # O-Ni-O double forward
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ssni2',
                              deltar = 'alpha*reff', _larch=self._larch))
        paths.append(feffpath(realpath(join(folder, "feff0010.dat")), # O-O rattle (the order of 10 and 11 is different in Demeter's pathfinder!)
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'sso*4',
                              deltar = 'alpha*reff', _larch=self._larch))

    rx  = 4.2
    if firstshell: rx  = 1.95

    trans = feffit_transform(kmin=3, kmax=15.938, kw=(2,1,3), dk=1, window='hanning', rmin=1.0, rmax=rx, _larch=self._larch)
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

    write_ascii(join(self.folder, "fit_"+which+shells+".k"), dset.data.k, dset.data.chi, dset.model.chi,
                labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)
    write_ascii(join(self.folder, "fit_"+which+shells+".r"), dset.data.r, dset.data.chir_mag, dset.model.chir_mag,
                dset.data.chir_re, dset.model.chir_re, labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)

    renderer = pystache.Renderer()
    with open(join('NiO','fit_'+which+shells+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'fit.mustache', # gnuplot mustache file
                                        {'material': 'NiO',
                                         'model': which,
                                         'shells': shells,
                                         'kmin': 3,
                                         'kmax': 15.938,
                                         'rmin': 1.0,
                                         'rmax': rx,
                                         'offset': 1,
                                     } ))

    return fit
#end def
