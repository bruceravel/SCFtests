


from os.path import realpath, exists, join

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass)
use_plugin_path('io')
from xdi import read_xdi
use_plugin_path('xafs')
from feffit import feffit_dataset, feffit_transform, feffit, feffit_report
from feffdat import feffpath
use_plugin_path('wx')
from plotter import (_newplot, _plot)


def do_fit(self, which):

    if which == 'testrun':
        folder = self.testrun
    elif which == 'baseline':
        folder = self.baseline
    else:
        folder = realpath(join(self.folder, 'baseline', which))
    #endif

    data = read_xdi(join(self.path, 'BaZrO3.chik'), _larch=self._larch)

    gds = Group(amp    = Parameter(0.95,    vary=True,  _larch=self._larch),
                enot   = Parameter(0.00001, vary=True,  _larch=self._larch),
                alpha  = Parameter(0.00001, vary=True,  _larch=self._larch),
                sso    = Parameter(0.003,   vary=True,  _larch=self._larch),
                ssba   = Parameter(0.003,   vary=True,  _larch=self._larch),
                sszr   = Parameter(0.003,   vary=True,  _larch=self._larch),
                #eba    = Parameter(0.00001, vary=True,  _larch=self._larch),
                #ezr    = Parameter(0.00001, vary=True,  _larch=self._larch),
                eba    = Parameter(expr='enot',          _larch=self._larch),
                ezr    = Parameter(expr='enot',         _larch=self._larch),
                sso2   = Parameter(0.003,   vary=True,  _larch=self._larch),
                czr    = Parameter(0.,      vary=False, _larch=self._larch),
                _larch=self._larch  )

    paths = list()
    paths.append(feffpath(realpath(join(folder, "feff0001.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0002.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso*1.5',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0003.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'eba',
                          sigma2 = 'ssba',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0004.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'ezr',
                          sigma2 = 'sszr',
                          third  = 'czr',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0005.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso*2',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0006.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = '(enot+ezr)/2',
                          sigma2 = 'sszr',
                          third  = 'czr',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0007.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso*2',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0009.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = '(2*enot+ezr)/3',
                          sigma2 = 'sszr',
                          third  = 'czr',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0008.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso*4',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0011.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = '(enot+eba)/2',
                          sigma2 = 'ssba+sso',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0012.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso2',
                          _larch=self._larch))
    paths.append(feffpath(realpath(join(folder, "feff0013.dat")),
                          s02    = 'amp',
                          deltar = 'alpha*reff',
                          e0     = 'enot',
                          sigma2 = 'sso+sso2',
                          _larch=self._larch))

    trans = feffit_transform(kmin=3, kmax=14.5, kw=(2,1,3), dk=1, window='hanning', rmin=1.2, rmax=4.5, _larch=self._larch)
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

    return fit
#end def
