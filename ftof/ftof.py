#!/usr/bin/env python3

# imports: do not edit these lines
import sys, os, argparse
import logging
import subprocess
from gemc_api_utils import GConfiguration
from gemc_api_geometry import *

from geometry import apply_configuration
from materials import define_materials


_logger = logging.getLogger("ftof")

VARIATION_MAP = {
    "default": "ftof__volumes_default.txt",
    "rga_fall2018": "ftof__volumes_rga_fall2018.txt",
}

def main():
    logging.basicConfig(level=logging.DEBUG)

    # Provides the -h, --help message
    desc_str = "   Will create the clas12 FTOF configuration\n"
    parser = argparse.ArgumentParser(description=desc_str)

    # loop over all the defined builder functions
    for var_key, file_name in VARIATION_MAP.items():

        basepath = os.environ["GPLUGIN_PATH"]

        _logger.info(f"Building FTOF configuration for variation {var_key}")
        # Define GConfiguration name, factory and description. Initialize it.
        configuration = GConfiguration('FTOF', 'TEXT', 'CLAS12 FTOF')
        configuration.setVariation(var_key)
        configuration.init_geom_file()
        configuration.init_mats_file()

        # define materials
        define_materials(configuration)

        # run geometry file bulder for selected variation
        apply_configuration(f'{basepath}/{file_name}', configuration)
        # print out the GConfiguration
        configuration.printC()


if __name__ == "__main__":
    main()
