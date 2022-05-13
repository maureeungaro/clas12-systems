#!/bin/tcsh -f

set COATJAVA = 6.6.1
set REPO     = https://clasweb.jlab.org/clas12offline/distribution/coatjava
set COATFILE = coatjava-$COATJAVA".tar.gz"
rm -rf clas12-offline-software

# Linux: -c = do not get file if already done.
if (`uname` == "Linux") then
	set mwget = "wget -c -nv --no-check-certificate"
# Mac: makes it quite and show nice progress
else if (`uname` == "Darwin") then
	set mwget = "wget -qc --show-progress --no-check-certificate"
endif

# Notice: no need to set COATJAVA env as the groovy script will pick up the relative location
rm -rf coat*jar jcsg*jar vecmath*jar

echo Dowloading $COATFILE version $COATJAVA":"  $REPO/$COATFILE
$mwget  --trust-server-names $REPO/$COATFILE -O $COATFILE

echo Unpacking $COATFILE
tar -xf $COATFILE
cp coatjava/lib/clas/* .

./ci/build.sh -a
