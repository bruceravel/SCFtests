#!/usr/bin/env bash

colorecho () {
    declare -A colors=( ["black"]='\033[1;30m' ["red"]='\033[1;31m'     ["green"]='\033[1;32m' ["yellow"]='\033[1;33m'
			["blue"]='\033[1;34m'  ["magenta"]='\033[1;35m' ["cyan"]='\033[1;36m'  ["white"]='\033[1;37m' )
    COLOR=${colors["white"]}
    if [[ ${colors["$2"]} != "" ]]; then COLOR=${colors["$2"]}; fi
    NC='\033[0m'
    echo -e "${COLOR}$1${NC}"
}


## this requires orgmk from https://github.com/fniessen/orgmk
if ! [ -x "$(command -v org2html)" ]; then
    colorecho "Need to install orgmk from https://github.com/fniessen/orgmk" red
    exit 1
fi

## ----- configuration -----------------------------------------------------------
all='README use scf iorder'
target=../SCFtests-ghpages
## ----- configuration -----------------------------------------------------------

for f in $all; do
    colorecho "Converting $f.org to HTML" "green"
    org2html -y $f.org
    ## use sed to insert a couple templates at the correct places in the html files
    sed -i '/class="author"/ r links.template' $f.html
    sed -i '/id="table-of-contents"/ r title.template' $f.html
    echo ""
done

if [[ ! -d $target ]]; then
    colorecho "The $target directory does not exist" red
    exit
fi
colorecho "Moving HTML files to $target" "green"
## copy all the files over
for f in $all; do
    mv -vf $f.html $target/
done
## rename README.html to index.html
mv -vf $target/README.html $target/index.html

