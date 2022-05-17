# clas12-systems

Software to build CLAS12 systems geometry and digitization plugins

## To Run

- Download coatjava:

  `installClas12Coatjava.sh`

- Run script to create volume parameters for a system:

  `cd groovyFactories` 
  
  `runFactories.sh systemName`


## Validation

The validation performed for the CLAS12 systems includes:

- Overlap test
- Tests specific to each system
- Validation against gemc2 geometry (in progress)

<!---
Obtained by Action > Job > ... > Create status badge

TODO:

- validate geometry against gemc2

-->

[![build](https://github.com/maureeungaro/clas12-systems/actions/workflows/build.yml/badge.svg)](https://github.com/maureeungaro/clas12-systems/actions/workflows/build.yml)

[![overlaps](https://github.com/maureeungaro/clas12-systems/actions/workflows/overlaps.yml/badge.svg)](https://github.com/maureeungaro/clas12-systems/actions/workflows/overlaps.yml)

[![tests](https://github.com/maureeungaro/clas12-systems/actions/workflows/tests.yml/badge.svg)](https://github.com/maureeungaro/clas12-systems/actions/workflows/tests.yml)

[![validate](https://github.com/maureeungaro/clas12-systems/actions/workflows/validate.yml/badge.svg)](https://github.com/maureeungaro/clas12-systems/actions/workflows/validate.yml)
