#!/usr/bin/env bash
# Using bash instead of zsh so we do not have to apt-get install zsh in ci

# Purpose: echo the list of systems changed by the last commit
# This could come from a push or a pull requrest.
#
# If the changes were made to the directories groovyFactories, ci, returns all supported systems
# 
Help()
{
	# Display Help
	echo
	echo "Syntax: whatToTest.sh [-h|f|d|b|c|g]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-b <GITHUB_BASE_REF>: sets the name of the base ref or target branch of the pull request"
	echo "-c <GITHUB_SHA>: sets the name of the commit SHA that triggered the workflow"
	echo "-g <GITHUB_BEFORE>: sets the name of the previous commit"
	echo "-d: debug mode (print the passed quantities)"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

MDEBUG=0

# GITHUB_BASE_REF and LASTCOMMIT may be passed empty (for example -b -c ccc -g ggg)
# This ensures that they are not assigned the other flags
while getopts ":dfhb:c:g:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      b)
         GITHUB_BASE_REF=$OPTARG
			[[ $GITHUB_BASE_REF == "-c" ]] && GITHUB_BASE_REF=no
			[[ $GITHUB_BASE_REF == "-g" ]] && GITHUB_BASE_REF=no
         ;;
      c)
         GITHUB_SHA=$OPTARG
			[[ $GITHUB_SHA == "-b" ]] && GITHUB_SHA=no
			[[ $GITHUB_SHA == "-g" ]] && GITHUB_SHA=no
         ;;
      g)
         GITHUB_BEFORE=$OPTARG
			[[ $GITHUB_BEFORE == "-c" ]] && GITHUB_BEFORE=no
			[[ $GITHUB_BEFORE == "-b" ]] && GITHUB_BEFORE=no
         ;;
		d)
		   MDEBUG=1
			;;
		\?) # Invalid option
         echo "Error: Invalid option"
         exit 1
         ;;
   esac
done

NoRef() {
	echo One of -b or -g options must be used
	Help
	exit 2
}

NoCommit() {
	echo The option -c is mandatory
	Help
	exit 2
}

# exit if both GITHUB_BASE_REF and LASTCOMMIT are not set
CheckCommit() {
	[[ $GITHUB_BASE_REF == "no" && $GITHUB_BEFORE == "no" ]] && NoRef
	[[ $GITHUB_SHA      == "no" ]]                           && NoCommit
}

PrintFlag () {
	echo $VALIDJOB
	exit
}

# put same-root longer names first to avoid abcde triggering the abc system
# for example ftof changes would trigger ft if 'ft' is placed before ftof
allSystems=( targets beamline ftof ft fc pcal ) # available systems ordered by z position
systemsChanged=()                 # list of system changed in last PR or push
breakLoop=0                       # set in CheckSystem to break main loop if changes in the core files are detected

# if the base name dir contains one of the system, add that system
CheckSystem () {
	filenName=$1
	bdir=$(dirname $filenName)

	if [[ $bdir == "ci" || $bdir == "groovyFactories" || $bdir == ".github/workflows" || $filenName == "compare_geometry.py" ]];
	then
		systemsChanged=("${allSystems[@]}")
		breakLoop=1
	else
		for ss in ${allSystems[*]}
		do
			systemPresent=$( echo $bdir | grep $ss | wc | awk '{print $1}' )
			(( $systemPresent == 1 )) && systemsChanged=($systemsChanged $ss)
		done
	fi
}

CheckCommit

# Pull Request
if [[ $GITHUB_BASE_REF != "no" ]]; then
	git fetch origin $GITHUB_BASE_REF --depth=1 -q
	FILESCHANGED=$( git diff --name-only origin/$GITHUB_BASE_REF $GITHUB_SHA )
# Push
else 
	git fetch origin $GITHUB_BEFORE --depth=1 -q
	FILESCHANGED=$( git diff --name-only $GITHUB_BEFORE $GITHUB_SHA  )
fi

for f in $FILESCHANGED
do
	CheckSystem $f
	(( $breakLoop == 1 )) && break
done

uniqueSystemsChanged=$( printf "%s\n" "${systemsChanged[@]}" | sort -u )

(( $MDEBUG == 1 )) && echo GITHUB_BASE_REF: $GITHUB_BASE_REF  GITHUB_SHA: $GITHUB_SHA GITHUB_BEFORE: $GITHUB_BEFORE  uniqueSystemsChanged: ${uniqueSystemsChanged[*]}

(( ${#systemsChanged[@]} )) || uniqueSystemsChanged=(irrelevant)

echo "{\"include\":["
for s in ${uniqueSystemsChanged[*]}
do
	[[ $s == ${uniqueSystemsChanged[${#uniqueSystemsChanged[@]}-1]} ]] && echo  "{\"detector\": \"$s\"}" || echo  "{\"detector\": \"$s\"},"
done
echo "]}"
