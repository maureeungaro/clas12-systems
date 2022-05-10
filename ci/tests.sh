#!/usr/bin/env zsh

# Purpose:
# runs gemc using the gcards inside 'tests' and 'overlaps' directory (if existing)
# inside each detector subdirs
# Assumptions: the names of the tests and overlaps directories.

# Container run example:
# docker run -it --rm jeffersonlab/gemc:3.0-clas12 bash
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/tests.sh -s ft/ft_cal

# load environment if we're on the container
TERM=xterm # source script use tput for colors, TERM needs to be specified
FILE=/etc/profile.d/jlab.sh

# notice the extra argument to the source command
test -f $FILE && source $FILE keepmine

Help()
{
	# Display Help
	echo
	echo "Syntax: tests.sh [-h|t|o|s]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-t: runs detector test"
	echo "-o: runs overlaps test"
	echo "-s <System>: build geometry and plugin for <System>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit
fi

while getopts ":htos:" option; do
   case $option in
      h)
         Help
         exit;;
      t)
         testType=tests
         ;;
      o)
         testType=overlaps
         ;;
      s)
         detector=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

TestTypeNotDefined() {
	echo "Test type is not set. Exiting"
	Help
	exit
}

[[ -v testType ]] && echo Running $testType tests || TestTypeNotDefined

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
gcards=no

./ci/build.sh -s $detector

