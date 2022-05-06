#!/usr/bin/env zsh
set -e

# Purpose: runs the geometry building scripts for the selected detector
# Assumptions:
# 1. the python sci-g main filename has the same name as the containing dir
# 2. the plugin directory is named 'plugin'

# Container run example:
# docker run -it --rm jeffersonlab/gemc:3.0-clas12 bash
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/build.sh -d ft/ft_cal

Help()
{
	# Display Help
	echo
	echo "Syntax: $0 [-h|d]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-d <Detector>: build geometry and plugin for <Detector>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit
fi

while getopts ":hd:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      d)
         detector=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
script=no

ScriptName() {
	subDir=$(basename $1)
	script="./"$subDir".py"
}


createAndCopyDetectorTXTs() {
	$script
	filesToCopy=$(git status -s | grep \? | awk '{print $2}' | grep -v \/ | grep \.txt)
	echo moving $=filesToCopy to $GPLUGIN_PATH
	mv $=filesToCopy $GPLUGIN_PATH
	# cleaning up
	rm -rf __pycache__
}

compileAndCopyPlugin() {
	cd plugin
	scons -j4 OPT=1
	echo moving plugins to $GPLUGIN_PATH
	mv *.gplugin $GPLUGIN_PATH
	scons -c
	# cleaning up
	rm -rf .sconsign.dblite
	cd -
}

# load environment if we're on the container
FILE=/etc/profile.d/jlab.sh
if test -f "$FILE"; then
    source "$FILE"
fi

ScriptName $detector

echo
echo Building geometry for $detector, running $script
echo
cd $detector
createAndCopyDetectorTXTs
test -d plugin && compileAndCopyPlugin

