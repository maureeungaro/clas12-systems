#!/bin/zsh

# log eye candy
green=`tput setaf 2`
yellow=`tput setaf 3`

# variation dictionary
declare -A variations
variations[bst]='default'
variations[dc]='default'
variations[ftof]='default rga_spring2018 rga_fall2018'
variations[ec]='default rga_fall2018'
variations[pcal]='default rga_spring2018 rga_fall2018'

# available system
availableSystems=(bst dc ftof ec pcal)


# do not edit below this point
txtDbOutputDir=../systemsTxtDB/
systemsToRun=()
availableLog="Available systems: 'all' or one of $availableSystems"

if [ -z "$1" ]; then
	echo
	echo "No system supplied. "$availableLog
	echo
	exit
fi

matchedSystem () {
	system=$1

	for s in $availableSystems
	do
		if [[ $system == $s ]]; then
			systemsToRun=$system
			echo Systems set to: $systemsToRun
			echo
		fi
	done

	if [[ $system == "all" ]]; then
		systemsToRun=("${availableSystems[@]}")
		echo Systems set to: $green$systemsToRun$reset
	fi
	if [[ ${#systemsToRun[@]} == 0 ]]; then
		echo
		echo "System $system not available. "$availableLog
		echo
		exit
	fi
}

# check that argument is 'all' or one of the available systems
matchedSystem $1

echo
for det in $systemsToRun
do
	thisVariations=${variations[$det]}
	for variation in $=thisVariations
	do
		logFile=$det"__groovyLog_"$variation".txt"
		echo $green$det$reset $yellow$variation$reset, log to $logFile
		groovy -cp "..:../*" $det".groovy" --variation $variation --runnumber 11 > $logFile
		toMove=$det"__volumes_$variation.txt"
		[ -f $toMove ] && mv $toMove $txtDbOutputDir
		toMove=$det"__parameters_$variation.txt"
		[ -f $toMove ]  && mv $toMove $txtDbOutputDir
		[ -f $logFile ] && mv $logFile $txtDbOutputDir
	done
	echo $green$det$reset done
	echo
done
echo
echo


