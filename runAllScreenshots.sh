#!/usr/bin/env zsh

# Purpose:
# Runs all detector dawn test
# Produce a log with the links to paste onto the README

allSystems=( targets beamline ) # available systems ordered by z position
#allSystems=( targets beamline ftof ft fc pcal ) # available systems ordered by z position

for s in $=allSystems
do

	echo Running dawn for $s
	./ci/tests.sh -s $s -d

done

for s in $allSystems
do
	echo
	echo "- ${(C)s}"
	echo
	echo -n "  | "
	jcards=`ls $s/dawn/*.jcard`
	for jc in $=jcards
	do
		v=$(echo $jc | awk -F'dawn\/' '{print $2}' | awk -F. '{print $1}')
		echo -n "[$v](screenshots/$s/$v.pdf) | "
	done
	echo
	echo
done
echo
echo
