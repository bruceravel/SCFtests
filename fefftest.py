
from   os        import makedirs, chdir, getcwd, unlink, listdir
from   os.path   import realpath, isdir, isfile, join
from   shutil    import rmtree
import sys, subprocess, glob, pystache, json, re
from   termcolor import colored
import numpy     as np
import importlib
from   distutils.spawn import find_executable
from   shutil  import rmtree, copy

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass, Interpreter)
use_plugin_path('xafs')
from feffdat import feffpath
from feffrunner import feffrunner
use_plugin_path('wx')
from plotter import (_newplot, _plot)

class FeffTestGroup(Group):
    """
    Feff testing group
    """

    def __init__(self, _larch=None, **kws):
        kwargs = dict(name='Feff test framework')
        kwargs.update(kws)
        Group.__init__(self,  **kwargs)
        self._larch       = Interpreter()
        self.materials    = ("Copper", "NiO", "FeS2", "UO2", "BaZrO3", "bromoadamantane", "uranyl")
        self._material    = None
        self.json         = None
        self.mustache     = None
        self.test         = 'scf'
        self.tests        = ('scf', 'iorder')
        self.dryrun       = False
        self.dopathfinder = False
        ## some things to make the cohabitation with f85ut happy
        self.doplot       = False
        self.verbose      = False
        self.firstshell   = False
        self.folder       = None
        self.path         = None
        
    @property
    def material(self):
        return self._material
    @material.setter
    def material(self, value):
        if value in self.materials:
            self._material = value
            self.folder = value
            self.path = realpath(self.folder)
            self.json = json.load(open(join(value, value + '.json')))
            self.mustache = join(value, value + '.mustache')
        else:
            self._material = None
            self.folder = None
            self.path = None
            self.json = None
            self.mustache = None
            
    def __repr__(self):
        if not self.material:
            return '<Feff Test Group (none)>'
        if self.material is not None:
            return '<Feff Test Group: %s>' % self.material
        return '<Feff Test Group (none)>'

    def prep(self):
        if self.test == 'scf':
            self.prep_scf()
        elif self.test == 'iorder':
            self.prep_iorder()
        else:
            raise Exception("You have not specified a valid test")

    def __target(self, which):
        target = join(self.material, self.test, which)
        if isdir(target): rmtree(target)
        makedirs(target)
        return target

    def __cull(self, which):
        owd = getcwd()
        try:
            chdir(join(self.material, self.test, which))
            feffoutput = glob.glob("*")
            for f in sorted(feffoutput):
                tosave = re.compile("feff(\d+\.dat|\.inp)|(chi|files|paths|xmu)\.dat|f85e.log")
                if not tosave.match(f): unlink(f)
        finally:
            chdir(owd)
    
    def prep_scf(self):
        if not self.material:
            raise Exception("You have not yet set the material for this test")

        ## do feff6 run
        target = self.__target('feff6')
        inpfile = join(target, 'feff.inp')
        copy(join(self.material, self.material+'.feff6'), inpfile)
        a=feffrunner(feffinp=inpfile)
        self.json['pathfinder'] = 1
        a.run(exe='feff6')
        self.__cull('feff6')

        pathsdat = join(self.material, self.test, 'feff6', 'paths.dat')
        renderer = pystache.Renderer()
        
        ## feff 8 without SCF
        target = self.__target('noSCF')
        self.json['pathfinder'] = 0
        self.json['doscf'] = '* '
        a.feffinp = join(target, 'feff.inp')
        with open(a.feffinp, 'w') as inp:
            inp.write(renderer.render_path( self.mustache, self.json ))  # mat/mat.mustache with mat/mat.json
        copy(pathsdat, join(self.material, self.test, 'noSCF'))
        a.run()
        self.__cull('noSCF')

        ## feff 8 at each of the SCF radii
        self.json['doscf'] = ''
        for r in self.json['radii']:
            this = 'withSCF_%s' % r
            target = self.__target(this)
            a.feffinp = join(target, 'feff.inp')
            self.json['scf'] = r
            with open(a.feffinp, 'w') as inp:
                inp.write(renderer.render_path( self.mustache, self.json ))  # mat/mat.mustache with mat/mat.json
            copy(pathsdat, join(self.material, self.test, this))
            a.run()
            self.__cull(this)

            
    def fits(self):
        """
        Perform a canned fit using a sequence of Feff calculations

        This is not used for unit testing feff85exafs.  It is a
        generalization of the fit() method intended for use with a
        generic testing framework, e.g. https://github.com/bruceravel/SCFtests

        Uses self.fittest, the name of a folder containing a sequence of
        Feff calculations.

        Sets self.models, a list of subfolders containing the identifying
        strings of the sequence of calculations.

        Returns a bunch of self.<id>, where <id> are feffit groups
        containing the fits in the sequence.
        """
        sys.path.append(self.material)
        module = importlib.import_module(self.material, package=None)

        if self.test is None:
            raise Exception("You must select a test folder.")

        self.models = []
        folders = ['feff6', 'noSCF']
        for r in self.json['radii']:
            folders.append('withSCF_%s' % r)
        for d in folders:
            if isdir(join(self.material, self.test, d)):
                print '>>>>>>>>> fitting with model: %s' % d
                self.models.append(d)
                this = module.do_fit(self, d, firstshell=self.firstshell, fittest=self.test)
                setattr(self, d, this)


    def plot(self, which):
        if which in self.models:
            dsets = getattr(getattr(self, which), 'datasets')
            dset = dsets[0]
            offset = 0.8 * max(dset.data.chir_mag)
            _newplot(dset.data.r,  dset.data.chir_mag+offset, xmax=6,
                     xlabel=r'$R \rm\,(\AA)$', label='data', color='blue',
                     ylabel=r'$|\chi(R)| \rm\,(\AA^{-3})$',
                     title='Fit to '+self.material+ ' using '+which, show_legend=True, _larch=self._larch)
            _plot(dset.model.r, dset.model.chir_mag+offset, label='fit', color='red', _larch=self._larch)
            _plot(dset.data.r,  dset.data.chir_re, label='', color='blue', _larch=self._larch)
            _plot(dset.model.r, dset.model.chir_re, label='', color='red', _larch=self._larch)
        else:
            raise Exception("%s is not one of the feff models for %s" % (which, self.material))
                
        
######################################################################

def ft(_larch=None, **kws):
    """
    Make a FeffTestGroup group given a folder containing a
    a testing file collection

    """
    return FeffTestGroup(_larch=_larch)
    
def registerLarchPlugin(): # must have a function with this name!
    return ('fefftest', { 'ft': ft })
    
