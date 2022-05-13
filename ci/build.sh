#!/usr/bin/env zsh

# Purpose: runs the geometry building scripts for the selected detector
# Assumptions:
# 1. The python sci-g main python filename must match the containing dir name
# 2. The plugin directory, if existing, must be named 'plugin'

# Container run example:
# docker run -it --rm jeffersonlab/gemc:3.0-clas12 bash
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/build.sh -s ft/ft_cal

# load environment if we're on the container
# notice the extra argument to the source command
TERM=xterm # source script use tput for colors, TERM needs to be specified
FILE=/etc/profile.d/jlab.sh
test -f $FILE && source $FILE keepmine

Help()
{
	# Display Help
	echo
	echo "Syntax: build.sh [-h|s]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-s <System>: build geometry and plugin for <System>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

while getopts ":hs:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      s)
         detector=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit 1
         ;;
   esac
done

DetectorNotDefined () {
	echo "Detector is not set."
	Help
	exit 2
}

# exit if detector var is not defined
[[ -v detector ]] && echo "Building $detector" || DetectorNotDefined

DefineScriptName() {
	subDir=$(basename $detector)
	script="./"$subDir".py"
}


CreateAndCopyDetectorTXTs() {
	echo
	echo Running $script
	$script
	ls -ltrh ./
	filesToCopy=$(git status -s | grep \? | awk '{print $2}' | grep -v \/ | grep \.txt)
	echo
	echo Moving $=filesToCopy to $GPLUGIN_PATH and cleaning up
	echo
	mv $=filesToCopy $GPLUGIN_PATH
	# cleaning up
	test -d __pycache__ && rm -rf __pycache__
	echo
	echo $GPLUGIN_PATH content:
	ls -ltrh $GPLUGIN_PATH
}

CompileAndCopyPlugin() {
	echo "Compiling plugin for "$detector
	echo
	cd plugin
	scons -j4 OPT=1
	echo Moving plugins to $GPLUGIN_PATH
	mv *.gplugin $GPLUGIN_PATH
	scons -c
	# cleaning up
	rm -rf .sconsign.dblite
	cd -
}

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
script=no

DefineScriptName $detector

echo
echo Building geometry for $detector. GPLUGIN_PATH is $GPLUGIN_PATH
echo
cd $detector
CreateAndCopyDetectorTXTs
test -d plugin && CompileAndCopyPlugin || echo "No plugin to build."

