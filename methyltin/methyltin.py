


from os.path import realpath, exists, join

from larch import (Group, Parameter, use_plugin_path)
use_plugin_path('io')
from xdi import read_xdi
use_plugin_path('xafs')
from feffit import feffit_dataset, feffit_transform, feffit, feffit_report
from feffdat import feffpath, _ff2chi
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

    dmt = read_xdi(join(self.path, 'dmt.chik'), _larch=self._larch)
    mmt = read_xdi(join(self.path, 'mmt.chik'), _larch=self._larch)

    gds = Group(amp     = Parameter(0.9,       vary=True,  _larch=self._larch),
                enot    = Parameter(1e-7,      vary=True,  _larch=self._larch),
                delr_c  = Parameter(1e-7,      vary=True,  _larch=self._larch),
                ss_c    = Parameter(0.003,     vary=True,  _larch=self._larch),
                delr_cl = Parameter(1e-7,      vary=True,  _larch=self._larch),
                ss_cl   = Parameter(0.003,     vary=True,  _larch=self._larch),
                _larch=self._larch  )

    paths_dmt = list()
    paths_dmt.append(feffpath(realpath(join(folder, "feff0001.dat")),
                              degen  = 2,
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss_c',
                              deltar = 'delr_c', _larch=self._larch))
    paths_dmt.append(feffpath(realpath(join(folder, "feff0002.dat")),
                              degen  = 2,
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss_cl',
                              deltar = 'delr_cl', _larch=self._larch))
    paths_mmt = list()
    paths_mmt.append(feffpath(realpath(join(folder, "feff0001.dat")),
                              degen  = 1,
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss_c',
                              deltar = 'delr_c', _larch=self._larch))
    paths_mmt.append(feffpath(realpath(join(folder, "feff0002.dat")),
                              degen  = 3,
                              s02    = 'amp',
                              e0     = 'enot',
                              sigma2 = 'ss_cl',
                              deltar = 'delr_cl', _larch=self._larch))


    trans = feffit_transform(kmin=2, kmax=13, kw=(2,1,3), dk=1, window='hanning', rmin=1.25, rmax=3, _larch=self._larch)
    dset  = [feffit_dataset(data=dmt, pathlist=paths_dmt, transform=trans, _larch=self._larch),
             feffit_dataset(data=mmt, pathlist=paths_mmt, transform=trans, _larch=self._larch)]
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = max(dset[0].data.chir_mag)/2
        _newplot(dset[0].data.r,  dset[0].data.chir_mag+offset, xmax=5, win=1,
                 xlabel=r'$R \rm\,(\AA)$', label='data',
                 ylabel=r'$|\chi(R)| \rm\,(\AA^{-3})$',
                 title='Fit to '+self.folder, show_legend=True, _larch=self._larch)
        _plot(dset[0].model.r, dset[0].model.chir_mag+offset, label='fit', win=1, _larch=self._larch)
        _plot(dset[0].data.r,  dset[0].data.chir_re, label='data', win=1, _larch=self._larch)
        _plot(dset[0].model.r, dset[0].model.chir_re, label='fit', win=1, _larch=self._larch)

        _plot(dset[1].data.r,  dset[1].data.chir_mag+7*offset,  label='fit', win=1, _larch=self._larch)
        _plot(dset[1].model.r, dset[1].model.chir_mag+7*offset, label='fit', win=1, _larch=self._larch)
        _plot(dset[1].data.r,  dset[1].data.chir_re+6*offset,   label='data', win=1, _larch=self._larch)
        _plot(dset[1].model.r, dset[1].model.chir_re+6*offset,  label='fit', win=1, _larch=self._larch)
    #end if
    
    if self.verbose:
        print feffit_report(fit, _larch=self._larch)
    #end if

    return fit
#end def
