
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
from feffit import feffit_report
use_plugin_path('wx')
from plotter import (_newplot, _plot)


import tabulate
bs=u'\\ '
bs=bs[0:1]
tabulate.LATEX_ESCAPE_RULES[bs]=bs
tabulate.LATEX_ESCAPE_RULES[u'{']=u'{'
tabulate.LATEX_ESCAPE_RULES[u'}']=u'}'
tabulate.LATEX_ESCAPE_RULES[u'^']=u'^'
tabulate.LATEX_ESCAPE_RULES[u'_']=u'_'
tabulate.LATEX_ESCAPE_RULES[u'$']=u'$'


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
        self.tests        = ('scf', 'iorder')
        self.__material   = None
        self.__test       = None
        self.testmodule   = None

        self.json         = None
        self.mustache     = None
        self.dryrun       = False
        self.dopathfinder = False
        self.tableformat  = 'pipe' # 'plain', 'simple', 'grid', 'fancy_grid', 'pipe', 'orgtbl'
                                   # 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs'

        ## some things to make the cohabitation with f85ut happy
        self.doplot       = False
        self.verbose      = False
        self.firstshell   = False
        self.folder       = None
        self.path         = None
        
    @property
    def material(self):
        return self.__material
    @material.setter
    def material(self, value):
        if self.__test == None:
            raise Exception("You must set the test BEFORE you set the material")
        if value in self.materials:
            self.__material = value
            self.folder = value
            self.path = realpath(self.folder)
            self.json = json.load(open(join(value, value + '.json')))
            self.mustache = join(value, value + '.mustache')
            self.models = self.__previous(value)
        else:
            self.__material = None
            self.folder = None
            self.path = None
            self.json = None
            self.mustache = None
            self.models = []
            
    @property
    def test(self):
        return self.__test
    @test.setter
    def test(self, value):
        if value in self.tests:
            self.__test = value
            ## load the prep() method from the chosen test
            sys.path.append('fefftests')
            self.testmodule = importlib.import_module(value, package=None)
        else:
            self.__test = None
            self.testmodule   = None
            string = ', '.join(map(str, self.tests))
            raise Exception("you said '%s' -- the valid tests are: %s" % (value, string))

    def __repr__(self):
        if not self.material:
            return '<Feff Test Group (none)>'
        if self.material is not None:
            return '<Feff Test Group: %s>' % self.material
        return '<Feff Test Group (none)>'

    def prep(self):
        if not self.test:
            raise Exception("You have not specified a valid test")
        self.testmodule.prep(self)

    def __previous(self, material):
        """
        Fetch the list of models for which feff has already been run.  This will
        be an empty list if feff has not yet been run.
        """
        list = []
        testdir = join(material, self.test)
        if isdir(testdir):
            for f in sorted(listdir(testdir)):
                for sf in ('feff6', 'noSCF', 'withSCF'): # <============ other tests?
                    if f.startswith(sf):   list.append(f)
        return list
        
    def target(self, which):
        """
        Determine the name of the working directory of the current testing
        model and initialize it.
        """
        target = join(self.material, self.test, which)
        if isdir(target): rmtree(target)
        makedirs(target)
        return target

    def cull(self, which):
        """
        Clean up files from the Feff run which are not needed for testing.
        """
        owd = getcwd()
        try:
            chdir(join(self.material, self.test, which))
            feffoutput = glob.glob("*")
            for f in sorted(feffoutput):
                tosave = re.compile("feff(\d+\.dat|\.inp)|(chi|files|paths|xmu)\.dat|f85e.log")
                if not tosave.match(f): unlink(f)
        finally:
            chdir(owd)
    
    def fits(self):
        """
        Perform a canned fit using a sequence of Feff calculations

        Uses self.test, the name of a folder containing a sequence of
        Feff calculations.

        Sets self.models, a list of subfolders containing the identifying
        strings of the sequence of calculations.

        Returns a bunch of self.<id>, where <id> are feffit groups
        containing the fits in the sequence.
        """
        sys.path.append(self.material)
        module = importlib.import_module(self.material, package=None)

        if self.test is None:
            raise Exception("You must select a test.")

        for d in self.models:
            if isdir(join(self.material, self.test, d)):
                print '>>>>>>>>> fitting with model: %s' % d
                this = module.do_fit(self, d, firstshell=self.firstshell, fittest=self.test)
                setattr(self, d, this)


    def table(self):
        variables = getattr(getattr(getattr(self, self.models[0]), 'params'), 'covar_vars')

        prefix = ''             # \\num{
        postfix = ''            # }
        chisqr = 'chi-square'   # $\chi^2$
        chinu = 'chi-reduced'   # $\chi^2_\\nu$
        rfactor = 'R-factor'    # $\mathcal{R}$
        paramheader = 'Best fit values'
        statsheader = 'Statistics'
        if self.tableformat.startswith('latex'):
            prefix = '\\num{'
            postfix = '}'
            chisqr = '$\chi^2$'
            chinu = '$\chi^2_\\nu$'
            rfactor = '$\mathcal{R}$'
            paramheader = '\\subsection{Best fit values}\n'
            statsheader = '\\subsection{Statistics}\n'
            
        
        table = []
        for d in self.models:
            dd=d
            if "_" in dd : dd=d.replace("_", "(") + ")"
            inner = [dd,]
            for var in variables:
                if var in ('amp', 'enot', 'nu'):
                    fmt = "%s%.2f(%d)%s"
                    mult = 100
                elif var in ('thetad'):
                    fmt = "%s%.0f(%d)%s"
                    mult = 1
                elif var.startswith('dr'):
                    fmt = "%s%.3f(%d)%s"
                    mult = 1000
                elif var.startswith('e'):
                    fmt = "%s%.3f(%d)%s"
                    mult = 1000
                else:
                    fmt = "%s%.5f(%d)%s"
                    mult = 100000
                val = fmt % (prefix,
                             getattr(getattr(getattr(getattr(self, d), 'params'), var), 'value'),
                             int(mult*getattr(getattr(getattr(getattr(self, d), 'params'), var), 'stderr')),
                             postfix)
                inner.append( val )
            table.append(inner)

        result = "\n%s\n\n" % paramheader
        result = result + "%s\n\n" % tabulate.tabulate(table, headers=['model',]+variables,
                                                       tablefmt=self.tableformat)

        table = []
        for d in self.models:
            dd=d
            if "_" in dd : dd=d.replace("_", "(") + ")"
            inner = [dd,]
            for stat in ('chi_square', 'chi_reduced', 'rfactor'):
                inner.append( getattr(getattr(getattr(self, d), 'params'), stat) )
            table.append(inner)
        result = result + "%s\n\n" % statsheader
        result = result + "%s\n" % tabulate.tabulate(table, headers=['model',chisqr, chinu, rfactor],
                                                     floatfmt=".4f", tablefmt=self.tableformat)

        return result
        
    def compare(self, param):
        for m in self.models:
            this=getattr(self, m)
            if param in getattr(getattr(this, 'params'), 'covar_vars'):
                print "%12s: %.5f +/- %.5f" % (m,
                                               getattr(getattr(getattr(this, 'params'), param), 'value'),
                                               getattr(getattr(getattr(this, 'params'), param), 'stderr'))
            elif param in ('chi_reduced', 'chi_square', 'rfactor'):
                print "%12s: %.5f" % (m, getattr(getattr(this, 'params'), param))
            else:
                print '%s is not one of the parameters of this fit' % param

                
    def plot(self, which):
        """
        Make a plot of one of the fitting results.  The argument is the name
        of the fit.  Alternatively, which can be in integer denoting
        the place in the list of models.

        For example, for the SCF tests, the names are "feff6",
        "noSCF", or "withSCF_N" where N is the radius of the
        self-consistency cluster.  1 is always "feff6", 2 is always
        "noSCF", 3+ are the "withSCF" calculations in order of
        increasing radius.
        """
        if isinstance(which, int):
            which = self.models[which-1]
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
            raise Exception("%s is not one of the feff models for the %s test" % (which, self.test))
                
    def png(self, which):
        """
        Call gnuplot to generate a PNG file with the result of the fit using the specified model.
        """
        if isinstance(which, int):
            which = self.models[which-1]
        if which in self.models:
            subprocess.call(['gnuplot', join(self.material, self.test, 'fit_%s.gp' % which)])
        else:
            raise Exception("%s is not one of the feff models for the %s test" % (which, self.test))
            
    def report(self, which):
        if isinstance(which, int):
            which = self.models[which-1]
        if which in self.models:
            this = getattr(self, which)
            print feffit_report(this, _larch=self._larch)
        else:
            raise Exception("%s is not one of the feff models for the %s test" % (which, self.test))


######################################################################

def ft(_larch=None, **kws):
    """
    Make a FeffTestGroup group given a folder containing a
    a testing file collection

    """
    return FeffTestGroup(_larch=_larch)
    
def registerLarchPlugin(): # must have a function with this name!
    return ('fefftest', { 'ft': ft })
    
