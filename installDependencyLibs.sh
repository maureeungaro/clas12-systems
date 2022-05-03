#!/bin/zsh

MYBUILDDIR=/Users/ungaro/builds
CONFIGURATION_BUILD_DIR=$MYBUILDDIR

# Purpose: install to libraries needed to run gemc + clas12 systems in $CONFIGURATION_BUILD_DIR

## XCODE

cd ft/ft_cal/
./ft_cal.py
cd -

cp $CLHEP_BASE_DIR/lib/libCLHEP-2.4.4.2.dylib $CONFIGURATION_BUILD_DIR
cp $XERCESCROOT/lib/libxerces-c-3.2.dylib     $CONFIGURATION_BUILD_DIR
cp $G4ROOT/$GEANT4_VERSION/lib/libG4*.dylib   $CONFIGURATION_BUILD_DIR
cp $GLIBRARY/lib/*.dylib                      $CONFIGURATION_BUILD_DIR
cp $CCDB_HOME/lib/*.dylib                     $CONFIGURATION_BUILD_DIR
cp ft/ft_cal/ft_cal.jcard                     $CONFIGURATION_BUILD_DIR
cp ft/ft_cal/ft_cal__geometry_default.txt     $CONFIGURATION_BUILD_DIR

echo
echo Remember to Ccompile the ft_cal and the streamers plugins from XCode
echo

## GNU

cd ft/ft_cal/plugin
scons -j4 OPT=1
cd -
cp ft/ft_cal/plugin/ft_cal.gplugin $GPLUGIN_PATH
cp $GLIBRARY/lib/gstreamer*        $GPLUGIN_PATH
