from   os.path   import join
from   shutil  import copy
import sys, subprocess, glob, pystache, json, re

from larch import (Group, Parameter, isParameter, param_value, use_plugin_path, isNamedClass, Interpreter)
use_plugin_path('xafs')
from feffrunner import feffrunner


def prep(fefftest):
    """
    Run feff for each of the models considered in the SCF test.
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

    ## make a pystache renderer, which will be used to generate the rest of the feff.inp files
    renderer = pystache.Renderer()
    
    ## feff 8 without SCF and without PLASMON
    target = fefftest.target('single') # make the folder for the single run
    fefftest.json['pathfinder'] = 0
    fefftest.json['iplsmn'] = 0
    fefftest.json['doscf'] = '* '
    runner.feffinp = join(target, 'feff.inp')
    with open(runner.feffinp, 'w') as inp:
        inp.write(renderer.render_path( fefftest.mustache, fefftest.json ))  # mat/mat.mustache with mat/mat.json
    copy(pathsdat, join(fefftest.material, fefftest.test, 'single')) #  use the feff6 paths.dat
    runner.run()
    fefftest.models.append('single')
    fefftest.cull('single')
    
    ## feff 8 without SCF and with PLASMON
    target = fefftest.target('multi') # make the folder for the multi run
    fefftest.json['pathfinder'] = 0
    fefftest.json['iplsmn'] = 1
    fefftest.json['doscf'] = '* '
    runner.feffinp = join(target, 'feff.inp')
    runner.mpse = True
    with open(runner.feffinp, 'w') as inp:
        inp.write(renderer.render_path( fefftest.mustache, fefftest.json ))  # mat/mat.mustache with mat/mat.json
    copy(pathsdat, join(fefftest.material, fefftest.test, 'multi')) #  use the feff6 paths.dat
    copy(join(fefftest.material, fefftest.material+'.exc'), join(fefftest.material, fefftest.test, 'multi', 'exc.inp')) #  use the feff6 paths.dat
    runner.run()
    fefftest.models.append('multi')
    fefftest.cull('multi')
