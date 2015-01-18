#!/bin/bash

##
## This script organizes the running of a sequence of feff
## calculations, 1 feff6, 1 feff85exafs without SCF, and a sequence of
## SCF calculations with increasingly large SCF radii.  This must be
## run before the fitcompare larch script can be used.
##

## use first command line argument or default to Copper
material=$1
if [ -z $1 ]; then
    material='Copper'
fi

## strip trailing slash
if [[ $material == *"/" ]]; then
    b=${material:0:-1}
    material=$b
fi


case $material in
    "Copper")
        ./models.py -f Copper -6        # feff6
        ./models.py -f Copper           # feff8 no self-consistency
        ./models.py -f Copper -s -r 3   # feff8 SCF 1 shell
        ./models.py -f Copper -s -r 4   # feff8 SCF 2 shell
        #./models.py -f Copper -s -r 5   # feff8 SCF 3 shell
        #./models.py -f Copper -s -r 5.5 # feff8 SCF 4 shell
        #./models.py -f Copper -s -r 6   # feff8 SCF 5 shell
        ;;
    "NiO")
        ./models.py -f NiO -6           # feff6
        ./models.py -f NiO              # feff8 no self-consistency
        ./models.py -f NiO -s -r 2.5    # feff8 SCF 1 shell
        ./models.py -f NiO -s -r 3      # feff8 SCF 2 shell
        ./models.py -f NiO -s -r 3.7    # feff8 SCF 3 shell
        #./models.py -f NiO -s -r 4.2    # feff8 SCF 4 shell
        #./models.py -f NiO -s -r 4.7    # feff8 SCF 5 shell
        ;;
    "UO2")
        ./models.py -f UO2 -6           # feff6
        ./models.py -f UO2              # feff8 no self-consistency
        ./models.py -f UO2 -s -r 3      # feff8 SCF 1 shell
        ./models.py -f UO2 -s -r 4      # feff8 SCF 2 shell
        ./models.py -f UO2 -s -r 5      # feff8 SCF 3 shell
        ./models.py -f UO2 -s -r 5.5    # feff8 SCF 4 shell
        ./models.py -f UO2 -s -r 6      # feff8 SCF 5 shell
        ;;
    "uranyl")
        ./models.py -f uranyl -6        # feff6
        ./models.py -f uranyl           # feff8 no self-consistency
        ./models.py -f uranyl -s -r 2.5 # feff8 SCF 1 shell
        ./models.py -f uranyl -s -r 2.9 # feff8 SCF 2 shell
        ./models.py -f uranyl -s -r 4.0 # feff8 SCF 3 shell
        ./models.py -f uranyl -s -r 5.2 # feff8 SCF more shells
        ./models.py -f uranyl -s -r 6.8 # feff8 SCF all the way to the U neighbor

        ./models.py -f uranyl -s -r 2.9 -t iorder -i 1  # iorder 1
        ./models.py -f uranyl -s -r 2.9 -t iorder -i 2  # iorder 2
        ./models.py -f uranyl -s -r 2.9 -t iorder -i 3  # iorder 3
        ./models.py -f uranyl -s -r 2.9 -t iorder -i 4  # iorder 4
        ./models.py -f uranyl -s -r 2.9 -t iorder -i 10 # iorder 10

        ;;
    "BaZrO3")
        ./models.py -f BaZrO3 -6        # feff6
        ./models.py -f BaZrO3           # feff8 no self-consistency
        ./models.py -f BaZrO3 -s -r 3   # feff8 SCF 1 shell
        ./models.py -f BaZrO3 -s -r 4   # feff8 SCF 2 shell
        ./models.py -f BaZrO3 -s -r 5.5 # feff8 SCF 3 shell
        ./models.py -f BaZrO3 -s -r 5   # feff8 SCF 4 shell
        ./models.py -f BaZrO3 -s -r 6   # feff8 SCF 5 shell
        ;;
    "bromoadamantane")
        ./models.py -f bromoadamantane -6       # feff6
        ./models.py -f bromoadamantane          # feff8 no self-consistency
        ./models.py -f bromoadamantane -s -r 8  # feff8 SCF the whole molecule
        ;;
    "methyltin")
        ./models.py -f methyltin -6             # feff6
        ./models.py -f methyltin                # feff8 no self-consistency
        ./models.py -f methyltin -s -r 8        # feff8 SCF the whole molecule
        ;;
    "FeS2")
        ./models.py -f FeS2 -6               # feff6
        ./models.py -f FeS2                  # feff8 no self-consistency
        ./models.py -f FeS2 -s -r 3          # feff8 SCF 1st shell
        ./models.py -f FeS2 -s -r 3.6        # feff8 SCF 2nd+3rd
        #./models.py -f FeS2 -s -r 4          # feff8 SCF 4th
        #./models.py -f FeS2 -s -r 5.3        # feff8 SCF 5th+6th+7th
        #./models.py -f FeS2 -s -r 5.5        # feff8 SCF 8th
        ;;
    *)
        echo "$material is not a material"
esac


