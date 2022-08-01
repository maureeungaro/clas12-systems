#!/usr/bin/env zsh

# Purpose:
# Runs gemc using the jcards inside 'tests' and 'overlaps' directory (if existing)
#   inside each detector subdirs
# Assumptions: the names of the tests and overlaps directories.

# Container run:
# docker run -it --rm jeffersonlab/gemc:3.0-clas12 sh
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# git clone http://github.com/maureeungaro/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/tests.sh -s ftof -o

if [[ -z "${G3CLAS12_VERSION}" ]]; then
	# load environment if we're on the container
	# notice the extra argument to the source command
	TERM=xterm # source script use tput for colors, TERM needs to be specified
	FILE=/etc/profile.d/jlab.sh
	test -f $FILE && source $FILE keepmine
else
  echo clas12-systems ci/tests: environment already defined
fi

Help()
{
	# Display Help
	echo
	echo "Syntax: tests.sh [-h|t|o|d|s]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-t: runs detector test. 'tests' directory must contain jcards."
	echo "-o: runs overlaps test. 'overlaps' directory must contain jcards."
	echo "-d: runs dawn screenshot. 'dawn' directory must contain jcards."
	echo "-s <System>: build geometry and plugin for <System>"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

while getopts ":htods:" option; do
   case $option in
      h)
         Help
         exit
         ;;
      t)
         testType=tests
         ;;
      d)
         testType=dawn
         ;;
      o)
         testType=overlaps
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

TestTypeNotDefined() {
	echo "Test type is not set. Exiting"
	Help
	exit 2
}

TestTypeDirNotExisting() {
	echo Test Type dir: $detector/$testType not existing
	Help
	exit 2
}

JcardsToRun () {
	test -d $detector/$testType && echo Test Type dir: $detector/$testType || TestTypeDirNotExisting

	jcards=`ls $detector/$testType/*.jcard`

	echo
	echo List of jcards in $testType: $=jcards
}


# need to check code twice
# This was done by this one liner:
# [[ $testType == 'dawn' ]] && gemc $jc -dawn || gemc $jc
# but the exist code of that is the test [[ $testType == 'dawn' ]] not the gemc run

RunGemc () {
	if [[ $testType == 'dawn' ]]; then
		gemc $1 -dawn ||
		exitCode=$?
		if [[ $exitCode != 0 ]]; then
			cat *.err
			exit $exitCode
		fi
	else
		gemc $1
		exitCode=$?
		if [[ $exitCode != 0 ]]; then
			cat *.err
			exit $exitCode
		fi
	fi
}

PublishDawn () {
	jcardRoot=$(echo $1 | awk -F'.jcard' '{print $1}')
	pdfFileName=$jcardRoot".pdf"
	echo
	echo Converting g4_0000.eps to $pdfFileName
	gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=$pdfFileName g4_0000.eps
	echo Content after conversion:
	ls -lrt
	rm g4_0000.*
}

[[ -v testType ]] && echo Running $testType tests || TestTypeNotDefined

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
cp $GLIBRARY/lib/gstreamer*.gplugin $GPLUGIN_PATH
jcards=no

./ci/build.sh -s $detector
if [ $? -ne 0 ]; then
	echo building system $detector failed
	exit 1
fi

# sets the list of jcards to run
JcardsToRun

# for some reason DYLD_LIBRARY_PATH is not passed to this script
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH

# location of database
export GEMCDB_ENV=systemsTxtDB

for jc in $=jcards
do
	echo Running gemc using jcards $jc
	RunGemc $jc

	[[ $testType == 'dawn' ]] && PublishDawn $jc || exit 0

done
