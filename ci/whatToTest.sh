#!/usr/bin/env bash

# Purpose: echo the list of systems changed by the last commit
# If the changes were made to groovyFactories, ci, returns all supported systems

# load environment if we're on the container
# notice the extra argument to the source command
TERM=xterm # source script use tput for colors, TERM needs to be specified

Help()
{
	# Display Help
	echo
	echo "Syntax: build.sh [-h|c|c|g]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-b <GITHUB_BASE_REF>: sets the name of the base ref or target branch of the pull request"
	echo "-c <GITHUB_SHA>: sets the name of the commit SHA that triggered the workflow"
	echo "-g <LASTCOMMIT>: sets the name of the previous commit"
	echo
}

echo $#

if [ $# -eq 3 ]; then
	Help
	exit 1
fi


# available systems
# ordered by z position
allSystems=(targets fc ft/ft_cal ftof)

while getopts ":hb:c:g:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      b)
         GITHUB_BASE_REF=$OPTARG
      c)
         GITHUB_SHA=$OPTARG
      g)
         LASTCOMMIT=$OPTARG
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit 1
         ;;
   esac
done

