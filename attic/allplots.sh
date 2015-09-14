#!/bin/bash

all='BaZrO3 Copper FeS2 NiO UO2 bromoadamantane uranyl'  # methyltin
test=scf

for m in $all; do
    for f in `ls $m/$test/*.gp`; do
	echo $m/$test : $f
	gnuplot $f
    done
done
