#!/bin/sh

all='BaZrO3 Copper FeS2 NiO UO2 bromoadamantane uranyl'  # methyltin
feff85exafs=$HOME/git/feff85exafs

for m in $all; do
    if [ -d $feff85exafs/tests/$m/baseline ]; then
	ln -sfv $feff85exafs/tests/$m/baseline $m/baseline
    else
	echo skipping $m/baseline
    fi
done
