#!/usr/bin/python

import sys, subprocess, glob, re
from   os      import unlink, makedirs, chdir
from   os.path import isdir,  realpath, join
from   shutil  import rmtree, copy
import pystache, json

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--folder", dest="folder",
                  help="perform test for FOLDER", metavar="FOLDER")

parser.add_option("-s", "--scf",
                  action="store_true", dest="doscf", default=False,
                  help="perform Feff calculation with SCF (default is no SCF)")

parser.add_option("-r", "--rsfc", dest="rscf", default=0,
                  help="set the SCF radius")

parser.add_option("-6", "--six", 
                  action="store_true", dest="six", default=False,
                  help="perform Feff 6 calculation")


(options, args) = parser.parse_args()

scf = 'noSCF'
if options.doscf: scf = 'withSCF'

repotop = '/home/bruce/git/feff85exafs'  # realpath(join('..','..'))
if options.folder[-1] == '/': options.folder = options.folder[:-1]

mat_json = json.load(open(join(options.folder, options.folder + '.json')))

mat_json['doscf']='* '
if options.doscf: mat_json['doscf']=''

if options.rscf and options.doscf:
    mat_json['scf'] = options.rscf
    scf = scf+'_'+str(options.rscf)

if options.six:
    scf = 'feff6'

## write the feff.inp file
target = join(options.folder, 'baseline', scf)


if isdir(target): rmtree(target)
makedirs(target)

if options.six:
    copy(join(options.folder, options.folder+'.feff6'), join(target, 'feff.inp'))
else:
    renderer = pystache.Renderer()
    with open(join(target,'feff.inp'), 'w') as inp:
        inp.write(renderer.render_path( join(options.folder, options.folder + '.mustache'), # material/material.mustache
                                        mat_json ))                                         # material/material.json


chdir(target)


if options.six:
    subprocess.call('feff6');
else:
    ## location of script for running a version of feff85exafs from the
    ## beginning of unit test developments,
    ## https://github.com/xraypy/feff85exafs/commit/cac0f8c90749ce52581a658c5a6c8ae144cc2211
    f85escript = join(repotop, 'bin', 'f85e')
    ## run the f85e shell script, which emulates the behavior of the monolithic Feff application
    subprocess.call(f85escript);

## cull the files we don't need for testing
feffoutput = glob.glob("*")
for f in sorted(feffoutput):
    tosave = re.compile("feff(\d+\.dat|\.inp)|(chi|files|paths|xmu)\.dat|f85e.log")
    if not tosave.match(f): unlink(f)
