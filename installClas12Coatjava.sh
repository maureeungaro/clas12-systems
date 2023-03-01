#!/bin/zsh

COATJAVA=6.6.1
REPO=https://clasweb.jlab.org/clas12offline/distribution/coatjava
COATFILE=coatjava-$COATJAVA".tar.gz"

rm -rf clas12-offline-software
rm -rf coat*jar jcsg*jar vecmath*jar
echo

if [[ `uname` == "Linux" ]]; then
    mwget="wget -c -nv --no-check-certificate"
elif [[ `uname` == "Darwin" ]]; then
    mwget="wget -qc --show-progress --no-check-certificate"
fi

echo "Downloading $COATFILE version $COATJAVA:  $REPO/$COATFILE"
$mwget --trust-server-names $REPO/$COATFILE -O $COATFILE

echo
echo Unpacking $COATFILE
tar -xf $COATFILE
cp coatjava/lib/clas/* .

#./ci/build.sh -a
