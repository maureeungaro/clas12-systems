#!/bin/zsh

green=`tput setaf 2`
yellow=`tput setaf 3`

declare -A variations

variations[dc]='default'
variations[ftof]='default rga_spring2018 rga_fall2018'

# Use the = parameter expansion specified to apply IFS word splitting.
# For example $=foo splits at whitespace as determined by IFS.

echo
for det in dc ftof
do
	thisVariations=${variations[$det]}
	for variation in $=thisVariations
	do
		echo $green$det$reset $yellow$variation$reset
		groovy -cp "..:../*" $det".groovy" --variation $variation --runnumber 11
		toMove=$det"__volumes_$variation.txt"
		[ -f $toMove ] && mv $toMove ../systems
		toMove=$det"__parameters_$variation.txt"
		[ -f $toMove ] && mv $toMove ../systems
	done
done
echo
echo


