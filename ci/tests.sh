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
# ./ci/tests.sh -s ftof -t
# ./ci/tests.sh -s ftof -d

# if we are in the docker container, we need to load the modules
if [[ -z "${DISTTAG}" ]]; then
    echo "\nNot in container"
else
    echo "\nIn container: ${DISTTAG}"
    TERM=xterm # source script use tput for colors, TERM needs to be specified
    source  /app/localSetup.sh
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

PublishDawn () {
	outputScreenshotDir=screenshots/$detector
	[[ ! -d $outputScreenshotDir ]] && mkdir -p $outputScreenshotDir
	jcardRoot=$(echo $1 | awk -F'.jcard' '{print $1}' | awk -F\/ '{print $NF}')
	pdfFileName=$outputScreenshotDir/$jcardRoot".pdf"
	echo
	echo Converting g4_0000.eps to $pdfFileName
	gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=$pdfFileName g4_0000.eps
	rm g4_0000.*
	
	echo Content of screenshots:
	ls -lrt screenshots
	echo Content of $outputScreenshotDir:
	ls -lrt $outputScreenshotDir
	
}

[[ -v testType ]] && echo Running $testType tests || TestTypeNotDefined

./ci/build.sh -s $detector

# for some reason DYLD_LIBRARY_PATH is not passed to this script
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH

# location of geometry database - notice we need to set it here again
startDir=`pwd`
export GEMCDB_ENV="$(pwd)/systemsTxtDB"

echo "TEST.SH: GLIBRARY is $GLIBRARY, GPLUGIN_PATH is $GPLUGIN_PATH, GEMCDB_ENV is $GEMCDB_ENV"

# sets the list of jcards to run
jcards=no
JcardsToRun

for jc in $=jcards
do
	echo
	echo Running gemc using jcards $jc
	if [[ $testType == 'dawn' ]]; then
		gemc $jc -dawn
		exitCode=$?
	else
		gemc $jc
		exitCode=$?
	fi
	
	echo
	echo exitCode: $exitCode
	echo
	
	if [[ $exitCode != 0 ]]; then
		ls -l MasterGeant4.err MasterGeant4.log
		cat MasterGeant4.log MasterGeant4.err
		exit $exitCode
	fi

	[[ $testType == 'dawn' ]] && PublishDawn $jc || echo gemc run using jcards $jc completed
	echo

done
