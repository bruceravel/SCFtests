#!/bin/bash

all='BaZrO3 Copper FeS2 NiO UO2 bromoadamantane uranyl'  # methyltin


for m in $all; do
    for f in `ls $m/*.gp`; do
	echo $m : $f
	gnuplot $f
    done
done
