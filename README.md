# clas12-systems

Software to build CLAS12 systems geometry and digitization plugins

## Geometry service

CLAS12 systems that use the coatjava geometry service to share geometry between simulation and recontruction 
use groovy to import the geometry parameters. To install coatjava:

- Download coatjava:

  `installClas12Coatjava.sh`

To create volume parameters for a system, run the groovy scripts through the runFactories script:

  `cd groovyFactories` 
  
  `runFactories.sh systemName`


## CLAS12 Systems Validation

The validation performed for the CLAS12 systems includes the following workflows

- Geometry and plugin builds
- Overlap tests
- Tests specific to each system
- Validation against gemc2 geometry 

[![Build Geo](https://github.com/gemc/clas12-systems/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/build.yml)
[![Test Overlaps](https://github.com/gemc/clas12-systems/actions/workflows/overlaps.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/overlaps.yml)
[![CLAS12 Tests](https://github.com/gemc/clas12-systems/actions/workflows/tests.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/tests.yml)
[![Validate Geometry](https://github.com/gemc/clas12-systems/actions/workflows/validate.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/validate.yml)

### GEMC validation

[![Compile GEMC](https://github.com/gemc/src/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build.yml)
[![Compile GLibrary](https://github.com/gemc/glibrary/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/glibrary/actions/workflows/build.yml)

