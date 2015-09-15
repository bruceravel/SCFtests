#!/bin/bash

## this requires orgmk from https://github.com/fniessen/orgmk

target=../SCFtests-ghpages

all='README use scf iorder'
for f in $all; do
    org2html -y $f.org
    ## use sed to insert links.template near the end of each html file
    sed '/class="author"/ r links.template' $f.html > __temp
    mv __temp $f.html
done

## copy all the files over
for f in $all; do
    cp -v $f.html $target/
done
## rename README.html to index.html
mv $target/README.html $target/index.html
