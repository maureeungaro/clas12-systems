#!/usr/bin/env zsh
set -e

# Purpose: runs the geometry building scripts for the selected detector
# Assumptions: the script name has the same name as the containing dir

startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB
script=no

ScriptName() {
	subDir=$(basename $1)
	script="./"$subDir".py"
}

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
         ScriptName $detector
         ;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


# load environment if we're on the container
FILE=/etc/profile.d/jlab.sh
if test -f "$FILE"; then
    source "$FILE"
fi


echo
echo Building geometry for $detector, running $script
echo
cd $detector
$script

