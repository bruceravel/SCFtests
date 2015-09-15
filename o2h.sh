#!/bin/bash

## this requires orgmk from https://github.com/fniessen/orgmk

target=../SCFtests-ghpages

all='README use scf iorder'
for f in $all; do
    org2html -y $f.org
    sed '/class="author"/ r links.template' $f.html > __temp
    mv __temp $f.html
done

for f in $all; do
    cp -v $f.html $target/
done
mv $target/README.html $target/index.html
