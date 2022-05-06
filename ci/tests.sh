#!/usr/bin/env zsh
set -e

# Purpose:
# this script assumes the existance of a 'tests' and 'overlaps' directory inside each detector
# containing various test jcards 

# Purpose:
# Assumptions:


Help()
{
	# Display Help
	echo
	echo "Syntax: $0 [-h|t|o]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-t runs test (other than overlaps)"
	echo "-o: runs overlaps test"
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit
fi

while getopts ":hto" option; do
   case $option in
      h)
         Help
         exit;;
      f)
         flag=yes
         echo flag: $flag
         ;;
      o)
         option=$OPTARG
         echo option: $option
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


