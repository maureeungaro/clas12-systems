#!/bin/zsh

# Purpose: install geometry and plugins onto systemsTxtDB ($GPLUGIN_PATH)

export startDir=`pwd`
GPLUGIN_PATH=$startDir/systemsTxtDB

# Native API detectors


# FT

cd ft/ft_cal/
./ft_cal.py
cd plugin
scons -j4 OPT=1
cd $startDir
cp ft/ft_cal/plugin/ft_cal.gplugin         $GPLUGIN_PATH
cp ft/ft_cal/ft_cal__geometry_default.txt  $GPLUGIN_PATH
