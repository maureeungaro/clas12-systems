#!/usr/bin/env zsh

# Purpose: compares the geometry implemented in gemc3 to the geometry in gemc2 for selected detector

# Container run:
# docker run -it --rm jeffersonlab/gemc3:1.0c12s sh
# git clone http://github.com/gemc/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# git clone http://github.com/maureeungaro/clas12-systems /root/clas12-systems && cd /root/clas12-systems
# ./ci/validateAgainstGemc2.sh -s ftof

# if we are in the docker container, we need to load the modules
if [[ -z "${DISTTAG}" ]]; then
    echo "\nNot in container"
else
    echo "\nIn container: ${DISTTAG}"
    source  /app/localSetup.sh
fi


startDir=`pwd`
GEMC3_DATA_DIR=$startDir/systemsTxtDB

Help()
{
	# Display Help
	echo
	echo "Syntax: validateAgainstGemc2.sh [-h|s|p]"
	echo
	echo "Options:"
	echo
	echo "-h: Print this Help."
	echo "-s <System>: compare geometry for <System>"
	echo "-p <path>: path to GEMC2 CLAS12 Geometry Directory"
	echo "-v: Verbose mode. Prints volumes and file paths."
	echo
}

if [ $# -eq 0 ]; then
	Help
	exit 1
fi

verbosity=""
while getopts ":hvs:p:" option; do
   case $option in
      h) # display Help
         Help
         exit
         ;;
      s)
         detector=$OPTARG
         ;;
      p)
         G2_PATH=$OPTARG
         ;;
      v)
         verbosity="-v"
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

PathNotDefined () {
	echo "CLAS12 GEMC2 geometry path is not set or does not exist."
	Help
	exit 2
}

CheckPath () {
	test -d $G2_PATH && echo Path to GEMC2 CLAS12 Geometry Directory: $G2_PATH || PathNotDefined
}

# exit if detector var is not defined
[[ -v detector ]] && echo "\nValidating $detector" || DetectorNotDefined 
[[ -v G2_PATH ]]  && CheckPath                     || PathNotDefined

gemc2_files_dir=$detector

case $detector in
	fc)
		subsystem_template_name="forward_carriage"
		gemc2_filename_prefix="forwardCarriage"
		gemc3_filename_prefix="clas12ForwardCarriage"
		;;
	ft)
		subsystem_template_name="ft"
		gemc2_filename_prefix="ft"
		gemc3_filename_prefix="ft"
		gemc2_files_dir='ft'
		;;
	ftof)
		subsystem_template_name=$detector
		gemc2_filename_prefix=$detector
		gemc3_filename_prefix=$detector
		;;
	targets)
		subsystem_template_name="target"
		gemc2_filename_prefix="target"
		gemc3_filename_prefix="clas12Target"
		;;
	pcal)
		subsystem_template_name=$detector
		gemc2_filename_prefix=$detector
		gemc3_filename_prefix=$detector
		;;
	ec)
		subsystem_template_name=$detector
		gemc2_filename_prefix=$detector
		gemc3_filename_prefix=$detector
		;;
	beamline)
		subsystem_template_name=$detector
		gemc2_filename_prefix=$detector
		gemc3_filename_prefix=$detector
		;;
	*) # Invalid option
		# Order of choices is along z direction
    	echo Detector $detector not supported. Possible choices: targets, beamline, ft, fc, ftof, pcal, ec
    	exit 1
        ;;
   esac

function run_comparison {

	local _gemc2_files_path="$G2_PATH/$gemc2_files_dir"
	local _gemc3_files_path="$GEMC3_DATA_DIR"

	echo "gemc2 files directory $_gemc2_files_path  content:\n"
	
	ls -ltrh $_gemc2_files_path

	echo "\ngemc3 files directory $_gemc3_files_path content:\n"

	ls -ltrh $_gemc3_files_path

	echo "\nRunning gemc2 - gemc3 geometry comparison for ${detector}"

	./compare_geometry.py --template-subsystem "$subsystem_template_name" \
								 --gemc2-path "${_gemc2_files_path}/${gemc2_filename_prefix}__geometry_{}.txt" \
								 --gemc3-path "${_gemc3_files_path}/${gemc3_filename_prefix}__geometry_{}.txt" -v
}

./ci/build.sh -s $detector


echo
echo "Comparing gemc2 and gemc3 geometry for $detector" 
echo
run_comparison
if [ $? -ne 0 ]; then
	echo "Comparing gemc2 and gemc3 geometry for $detector failed"
	exit 1
fi
