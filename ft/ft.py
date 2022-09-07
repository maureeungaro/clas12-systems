#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
import logging
import subprocess
from gemc_api_utils import GConfiguration
from gemc_api_geometry import *

from geometry_calorimeter import buildCalorimeter, make_ft_pipe
from geometry_hodoscope import buildHodoscope
from geometry_tracker import buildTracker

from materials import define_materials

_logger = logging.getLogger("ft")

VARIATIONS = {
    "FTOn",
    "FTOff",
    "KPP",
}


def main():
	logging.basicConfig(level=logging.DEBUG)
	
	# Provides the -h, --help message
	desc_str = "   Will create the Forward Tagger Calorimeter (ft_cal), Hodoscope (ft_hodo) and Tracker (ft_trk) systems\n"
	parser = argparse.ArgumentParser(description=desc_str)
	args = parser.parse_args()

	# loop over all the defined builder functions
	for variation in VARIATIONS:
		
		_logger.info(f"Building ft for variation {variation}")
		# Define GConfiguration name, factory and description.
		configuration = GConfiguration('ft', 'TEXT', 'The CLAS12 Forward Tagger Calorimeter, Hodoscope and Tracker')
		configuration.setVariation(variation)
		configuration.init_geom_file()
	
		# define materials
		configuration.init_mats_file()
		define_materials(configuration)
	
		# build geometry
		if variation == "KPP" :
			make_ft_pipe(configuration)
		else:
			buildCalorimeter(configuration)
			buildHodoscope(configuration)
			if variation == "FTOn" :
				buildTracker(configuration)

		# print out the GConfiguration
		configuration.printC()


if __name__ == "__main__":
	main()






