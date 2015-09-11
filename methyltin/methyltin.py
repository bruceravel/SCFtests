


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


    trans = feffit_transform(kmin=3, kmax=13, kw=(2,1,3), dk=1, window='hanning', rmin=1.25, rmax=3, _larch=self._larch)
    dset  = [feffit_dataset(data=dmt, pathlist=paths_dmt, transform=trans, _larch=self._larch),
             feffit_dataset(data=mmt, pathlist=paths_mmt, transform=trans, _larch=self._larch)]
    fit   = feffit(gds, dset, _larch=self._larch)

    if self.doplot:
        offset = max(dset[0].data.chir_mag)/2
        _newplot(dset[0].data.r,  dset[0].data.chir_mag+offset, xmax=5, win=1,
                 xlabel=r'$R \rm\,(\AA)$', label='dimethyltin',
                 ylabel=r'$|\chi(R)| \rm\,(\AA^{-3})$',
                 title='Fit to '+self.folder, show_legend=True, _larch=self._larch)
        _plot(dset[0].model.r, dset[0].model.chir_mag+offset,   label='fit',  win=1, _larch=self._larch)
        _plot(dset[0].data.r,  dset[0].data.chir_re,            label='dimethyltin', win=1, _larch=self._larch)
        _plot(dset[0].model.r, dset[0].model.chir_re,           label='fit',  win=1, _larch=self._larch)

        _plot(dset[1].data.r,  dset[1].data.chir_mag+7*offset,  label='monomethyltin', win=1, _larch=self._larch)
        _plot(dset[1].model.r, dset[1].model.chir_mag+7*offset, label='fit',  win=1, _larch=self._larch)
        _plot(dset[1].data.r,  dset[1].data.chir_re+6*offset,   label='monomethyltin', win=1, _larch=self._larch)
        _plot(dset[1].model.r, dset[1].model.chir_re+6*offset,  label='fit',  win=1, _larch=self._larch)
    #end if
    
    if self.verbose:
        print feffit_report(fit, _larch=self._larch)
    #end if

    shells = ''
    if firstshell: shells='_1st'

    write_ascii(join(self.folder, fittest, "fit_"+which+".k"), dset.data[0].k, dset.data[0].chi, dset.model[0].chi,
                labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)
    write_ascii(join(self.folder, fittest, "fit_"+which+".r"), dset.data[0].r, dset.data[0].chir_mag, dset.model[0].chir_mag,
                dset.data[0].chir_re, dset.model[0].chir_re, labels="r data_mag fit_mag data_re fit_re", _larch=self._larch)

    renderer = pystache.Renderer()
    with open(join(self.folder, fittest, 'fit_'+which+'.gp'), 'w') as inp:
        inp.write(renderer.render_path( 'plot.mustache', # gnuplot mustache file
                                        {'material': 'methyltin',
                                         'model': which,
                                         'fittest': fittest,
                                         'shells': shells,
                                         'kmin': 3,
                                         'kmax': 13,
                                         'rmin': 1.25,
                                         'rmax': 3,
                                         'offset': 1,
                                     } ))

    return fit
#end def
