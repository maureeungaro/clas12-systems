#!/usr/bin/env bash
set -e

# Purpose: compares the geometry implemented in gemc3 to the geometry in gemc2 for selected detector
# Assumptions:
# 

# Container run example:
# docker run -it --rm jeffersonlab/gemc:3.0-clas12 bash
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/build.sh -s ft/ft_cal

# load environment if we're on the container
# notice the extra argument to the source command
TERM=xterm # source script use tput for colors, TERM needs to be specified
FILE=/etc/profile.d/jlab.sh
test -f $FILE && source $FILE keepmine

GEMC2_DATA_DIR=/jlab/clas12Tags

ls -ltrh $GEMC2_DATA_DIR
startDir=`pwd`
GEMC3_DATA_DIR=$startDir/systemsTxtDB

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

gemc2_files_dir=$detector
case $detector in
	targets)
		subsystem_template_name="target"
		gemc2_filename_prefix="target"
		gemc3_filename_prefix="target"
		;;
	fc)
		subsystem_template_name="forward_carriage"
		gemc2_filename_prefix="forwardCarriage"
		gemc3_filename_prefix="forwardCarriage"
		;;
	ft/ft_cal)
		subsystem_template_name="ft_cal"
		gemc2_filename_prefix="ft"
		gemc3_filename_prefix="ft_cal"
		gemc2_files_dir='ft'
		;;
	ftof)
		subsystem_template_name=$detector
		gemc2_filename_prefix=$detector
		gemc3_filename_prefix=$detector
		;;
	*) # Invalid option
    	echo "Detector not supported"
    	exit 1
        ;;
   esac


function get_gemc2_data_for_comparison {

	echo "Cloning GEMC2 repository $GEMC2_DATA_CLONE_URL to $GEMC2_DATA_CLONE_DIR to use for comparison"

	git clone --quiet "$GEMC2_DATA_CLONE_URL" "$GEMC2_DATA_CLONE_DIR"
}

function run_comparison {

	local _gemc2_files_path="$GEMC2_DATA_DIR/5.1/experiments/clas12/$gemc2_files_dir"
	local _gemc3_files_path="$GEMC3_DATA_DIR"

	echo "gemc2 files directory is: $_gemc2_files_path"
	
	ls -ltrh $_gemc2_files_path

	echo "gemc3 files directory is: $_gemc3_files_path"

	ls -ltrh $_gemc3_files_path

	echo "Running gemc2 - gemc3 geometry comparison for ${detector}"

	./compare_geometry.py --template-subsystem "$subsystem_template_name" --gemc2-path "${_gemc2_files_path}/${gemc2_filename_prefix}__geometry_{}.txt" --gemc3-path "${_gemc3_files_path}/${gemc3_filename_prefix}__geometry_{}.txt"
}


echo
echo "Comparing gemc2 and gemc3 geometry for $detector" 
echo
run_comparison

