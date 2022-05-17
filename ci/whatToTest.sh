#!/usr/bin/env bash
# Using bash instead of zsh so we do not have to apt-get install zsh in ci

# Purpose: echo the list of systems changed by the last commit
# This could come from a push or a pull requrest.
#
# If the changes were made to groovyFactories, ci, returns all supported systems

Help()
{
	# Display Help
	echo
	echo "Syntax: whatToTest.sh [-h|b|c|g]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-b <GITHUB_BASE_REF>: sets the name of the base ref or target branch of the pull request"
	echo "-c <GITHUB_SHA>: sets the name of the commit SHA that triggered the workflow"
	echo "-g <GITHUB_BEFORE>: sets the name of the previous commit"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

# available systems
# ordered by z position
allSystems=(targets fc ft/ft_cal ftof)

# GITHUB_BASE_REF and LASTCOMMIT may be passed empty (for example -b -c ccc -g ggg)
# This ensures that they are not assigned the other flags
while getopts ":hb:c:g:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      b)
         GITHUB_BASE_REF=$OPTARG
			[[ $GITHUB_BASE_REF == "-g" ]] && GITHUB_BASE_REF=no
			[[ $GITHUB_BASE_REF == "-c" ]] && GITHUB_BASE_REF=no
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
	echo
	[[ $GITHUB_BASE_REF == "no" && $GITHUB_BEFORE == "no" ]] && NoRef
	[[ $GITHUB_SHA      == "no" ]]                          && NoCommit
}

echo GITHUB_BASE_REF $GITHUB_BASE_REF
echo GITHUB_BEFORE $GITHUB_BEFORE
echo GITHUB_SHA $GITHUB_SHA

CheckCommit

# Pull Request
if [ $GITHUB_BASE_REF != "no" ]; then
	git fetch origin $GITHUB_BASE_REF --depth=1
	echo git diff --name-only origin/$GITHUB_BASE_REF $GITHUB_SHA
	#GITDIFF=$( git diff --name-only origin/$GITHUB_BASE_REF $GITHUB_SHA )
else # Push
	git fetch origin $GITHUB_BEFORE --depth=1
	echo git diff --name-only $GITHUB_BEFORE $GITHUB_SHA
	#GITDIFF=$( git diff --name-only $$LASTCOMMIT $GITHUB_SHA )
fi
 
echo $GITDIFF
