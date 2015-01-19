#!/usr/bin/python

import sys, subprocess, glob, re
from   os      import unlink, makedirs, chdir
from   os.path import isdir,  realpath, join
from   shutil  import rmtree, copy
import pystache, json

import argparse
parser = argparse.ArgumentParser(description="Organize Feff calculations for testing")
parser.add_argument("-f", "--folder", dest="folder", required=True,
                    help="perform test for FOLDER", metavar="FOLDER")

parser.add_argument("-t", "--test", dest="fittest",
                    choices = ['scf', 'iorder'], default =  'scf',
                    help="name of fit test (scf|iorder)", metavar="FOLDER")

parser.add_argument("-s", "--scf",
                    action="store_true", dest="doscf", default=False,
                    help="perform Feff calculation with SCF (default is no SCF)")

parser.add_argument("-r", "--rsfc", dest="rscf", default=0,
                    help="set the SCF radius")

parser.add_argument("-6", "--six", 
                    action="store_true", dest="six", default=False,
                    help="perform Feff 6 calculation")

parser.add_argument("-d", "--dopathfinder", 
                    action="store_true", dest="dopathfinder", default=False,
                    help="flag to run pathfinder during Feff run")

parser.add_argument("-i", "--iorder", dest="iorder", default=2, type=int,
                    help="set the iorder parameter")

parser.add_argument("-n", "--dryrun", 
                    action="store_true", dest="dryrun", default=False,
                    help="make workspace, write feff.inp, but don't run feff")
options = parser.parse_args()



repotop = '/home/bruce/git/feff85exafs'  # realpath(join('..','..'))
if options.folder[-1] == '/': options.folder = options.folder[:-1]


mat_json = json.load(open(join(options.folder, options.folder + '.json')))
mat_json['iorder'] = options.iorder

mat_json['doscf']='* '
if options.doscf: mat_json['doscf']=''

## workspace logic:
##  workspace name is determined sequentially based on flags provided
##    1. scf is the default (specified as '-t scf')
##    2. workspace is "noSCF" without '-r' flag
##    3. workspace is "withSCF_XX" with '-r XX'
##    4. workspace is "iorder_N" with '-t iorder' and '-i N'
##    5. workspace is "feff6" with -6

workspace = 'noSCF'
if options.doscf: workspace = 'withSCF'

if options.rscf and options.doscf:
    mat_json['scf'] = options.rscf
    workspace = workspace+'_'+str(mat_json['scf'])

if options.fittest == 'iorder':
    workspace = 'iorder_%2.2d' % mat_json['iorder']

if options.six:
    workspace = 'feff6'
    options.fittest = 'scf'
    mat_json['iorder'] = 2

target = join(options.folder, options.fittest, workspace)
if isdir(target): rmtree(target)
makedirs(target)

## copy over the paths.dat file -- this guarantees that each calculation uses the same path list 
if workspace != 'feff6':
    if options.dopathfinder:
        mat_json['pathfinder'] = 1
    else:
        copy(join(options.folder, options.folder+'.paths'), join(target, 'paths.dat'))
        mat_json['pathfinder'] = 0

## write the feff.inp file
if options.six:
    copy(join(options.folder, options.folder+'.feff6'), join(target, 'feff.inp'))
else:
    renderer = pystache.Renderer()
    with open(join(target,'feff.inp'), 'w') as inp:
        inp.write(renderer.render_path( join(options.folder, options.folder + '.mustache'), # mat/mat.mustache
                                        mat_json ))                                         # mat/mat.json


## stop here with -n flag
if options.dryrun: sys.exit(1)

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
