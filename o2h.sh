#!/bin/bash

## this requires orgmk from https://github.com/fniessen/orgmk

target=../SCFtests-ghpages

all='README use scf iorder'
for f in $all; do
    org2html -y $f.org
    ## use sed to insert links.template near the end of each html file
    sed '/class="author"/ r links.template' $f.html > __temp
    sed '/id="table-of-contents"/ r title.template' __temp > __temp2
    mv __temp2 $f.html
    rm -f __temp
done

## copy all the files over
for f in $all; do
    mv -v $f.html $target/
done
## rename README.html to index.html
mv -v $target/README.html $target/index.html
