#!/bin/zsh

# Purpose: install the libraries / geometry / jcards needed to xcode-run gemc + clas12 systems

# defined in xcode settings
MYBUILDDIR=/Users/ungaro/builds
CONFIGURATION_BUILD_DIR=$MYBUILDDIR

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
