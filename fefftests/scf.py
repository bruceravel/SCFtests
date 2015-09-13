from   os.path   import join
from   shutil  import copy
import sys, subprocess, glob, pystache, json, re

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass, Interpreter)
use_plugin_path('xafs')
from feffrunner import feffrunner


def prep(fefftest):
    """
    Run feff for each of the models considered in a test.
    """
    if not fefftest.material:
        raise Exception("You have not yet set the material for this test")
    
    ## do feff6 run
    fefftest.models = []
    target = fefftest.target('feff6') # make the folder for the feff6 run
    inpfile = join(target, 'feff.inp')
    copy(join(fefftest.material, fefftest.material+'.feff6'), inpfile)
    runner=feffrunner(feffinp=inpfile)
    fefftest.json['pathfinder'] = 1
    runner.run(exe='feff6')
    fefftest.models.append('feff6') # keep a list of model names
    fefftest.cull('feff6')

    ## note the paths.dat file so it can be copied to each of the following test folders
    pathsdat = join(fefftest.material, fefftest.test, 'feff6', 'paths.dat')

    ## make dicts for holding the convergence data for each feff8 run
    fefftest.threshold = {'feff6': []}
    fefftest.chargetransfer = {'feff6': []}
    runner.threshold = []
    runner.chargetransfer = []

    ## make a pystache renderer, which will be used to generate the rest of the feff.inp files
    renderer = pystache.Renderer()
    
    ## feff 8 without SCF
    target = fefftest.target('noSCF') # make the folder for the noSCF run
    fefftest.json['pathfinder'] = 0
    fefftest.json['doscf'] = '* '
    runner.feffinp = join(target, 'feff.inp')
    with open(runner.feffinp, 'w') as inp:
        inp.write(renderer.render_path( fefftest.mustache, fefftest.json ))  # mat/mat.mustache with mat/mat.json
    copy(pathsdat, join(fefftest.material, fefftest.test, 'noSCF')) #  use the feff6 paths.dat
    runner.run()
    fefftest.models.append('noSCF')
    fefftest.threshold['noSCF'] = runner.threshold
    fefftest.chargetransfer['noSCF'] = list([])
    runner.threshold = []
    runner.chargetransfer = []
    fefftest.cull('noSCF')

    ## feff 8 at each of the SCF radii
    fefftest.json['doscf'] = ''
    for r in fefftest.json['radii']:
        this = 'withSCF_%s' % r
        target = fefftest.target(this) # make the folder for this feff8 run with SCF
        runner.feffinp = join(target, 'feff.inp')
        fefftest.json['scf'] = r
        with open(runner.feffinp, 'w') as inp:
            inp.write(renderer.render_path( fefftest.mustache, fefftest.json ))  # mat/mat.mustache with mat/mat.json
        copy(pathsdat, join(fefftest.material, fefftest.test, this)) # use the feff6 paths.dat
        runner.run()
        fefftest.models.append(this)
        fefftest.threshold[this] = runner.threshold
        fefftest.chargetransfer[this] = runner.chargetransfer
        runner.threshold = []
        runner.chargetransfer = []
        fefftest.cull(this)
