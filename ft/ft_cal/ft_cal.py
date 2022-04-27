#!/usr/bin/env python3

import sys, os, argparse

# define system configurations and various utilities
from gemc_api_utils import *
from gemc_api_geometry import *


# This section handles checking for the required configuration filename argument
# and also provides help and usage messages
# Add options as needed
desc_str = "   Will create the Forward Tagger Calorimeter (FT_CAL) geometry\n"
parser = argparse.ArgumentParser(description=desc_str)
args = parser.parse_args()

# Define configuration
configuration = GConfiguration("ft_cal", "TEXT", "The Forward Tagger Calorimeter")

# initialize geometry file
# this is only necessary for TEXT or JSON confgurations
configuration.init_geom_file()


# build the geometry using the local geometry file
from geometry import *

buildCalorimeter(configuration)
buildHodoscope(configuration)

# print out the GConfiguration
configuration.printC()

