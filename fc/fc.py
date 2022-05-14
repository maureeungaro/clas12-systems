#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
from gemc_api_utils import *
from gemc_api_geometry import *

# build the geometry using the local geometry file
from geometry import VARIATION_MAP

def main():
    # Provides the -h, --help message
    desc_str = "   Will create the clas12 forward carriage geometry\n"
    parser = argparse.ArgumentParser(description=desc_str)
    args = parser.parse_args()

    # loop over all the defined builder functions
    for mfield_key, builder in VARIATION_MAP.items():
        print(f"Building forward carriage geometry with {mfield_key} magnetic field")
        # Define GConfiguration name, factory and description. Initialize it.
        configuration = GConfiguration('clas12ForwardCarriage', 'TEXT', 'CLAS12 Forward Carriage')
        configuration.setVariation(mfield_key)
        configuration.init_geom_file()

        # run the selected builder function
        builder(configuration)
        # print out the GConfiguration
        configuration.printC()

if __name__ == '__main__':
    main()


