from   os.path   import join, isfile, isdir
from   shutil  import copy
import sys, subprocess, glob, pystache, json, re

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass, Interpreter)
use_plugin_path('xafs')
from feffrunner import feffrunner


def prep(fefftest):
    """
    Run feff for each of the models considered in the iorder test.
    """
    if not fefftest.material:
        raise Exception("You have not yet set the material for this test")
    
    fefftest.models = []        # this will be a list of the model names
    inpfile = join(fefftest.material, 'scf', 'feff6', 'feff.inp')
    runner=feffrunner(feffinp=inpfile)

    ## note the paths.dat file so it can be copied to each of the following test folders
    pathsdat = join(fefftest.material, 'scf', 'feff6', 'paths.dat')
    if not isfile(pathsdat):    # make it if it's not there
        fefftest.test = 'scf'
        target = fefftest.target('feff6') # make the folder for the feff6 run
        inpfile = join(target, 'feff.inp')
        copy(join(fefftest.material, fefftest.material+'.feff6'), inpfile)
        runner=feffrunner(feffinp=inpfile)
        fefftest.json['pathfinder'] = 1
        runner.run(exe='feff6')
        fefftest.cull('feff6')
        fefftest.test = 'iorder'

    ## make dicts for holding the convergence data for each feff8 run
    fefftest.threshold = dict()
    fefftest.chargetransfer = dict()
    runner.threshold = []
    runner.chargetransfer = []

    ## make a pystache renderer, which will be used to generate the rest of the feff.inp files
    renderer = pystache.Renderer()

    ## feff 8 with each iorder using the second shortest SCF radius
    fefftest.json['pathfinder'] = 0
    fefftest.json['doscf'] = ''
    fefftest.json['scf'] = fefftest.json['radii'][0] # unless there is only 1 SCF radius
    if len(fefftest.json['radii']) > 1:
        fefftest.json['scf'] = fefftest.json['radii'][1]

    for i in fefftest.json['iorders']:
        this = 'iorder_%2.2d' % i
        target = fefftest.target(this) # make the folder for this feff8 run with SCF
        runner.feffinp = join(target, 'feff.inp')
        fefftest.json['iorder'] = i
        with open(runner.feffinp, 'w') as inp:
            inp.write(renderer.render_path( fefftest.mustache, fefftest.json ))  # mat/mat.mustache with mat/mat.json
        copy(pathsdat, join(fefftest.material, fefftest.test, this)) # use the feff6 paths.dat
        runner.run()
        fefftest.models.append(this) # keep a tally of the model names
        ## add the current convergence results
        fefftest.threshold[this] = runner.threshold
        fefftest.chargetransfer[this] = runner.chargetransfer
        ## and reinitialize the convergence attributes in feffrunner
        runner.threshold = []
        runner.chargetransfer = []
        fefftest.cull(this)
