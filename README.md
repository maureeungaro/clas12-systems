Software to build CLAS12 systems geometry and digitization plugins

## Geometry service

CLAS12 systems that use the coatjava geometry service to share geometry between simulation and recontruction 
use groovy to import the geometry parameters. To install coatjava:

- Download coatjava:

  `installClas12Coatjava.sh`

To create volume parameters for a system, run the groovy scripts through the runFactories script:

  `cd groovyFactories` 
  
  `runFactories.sh systemName`

<br/> 


## CLAS12 Screenshots

The ci produce a pdf screenshot for each variations in all systems:

- Targets

  | [al27](screenshots/targets/al27.pdf) | [apollo_nd3](screenshots/targets/apollo_nd3.pdf) | [apollo_nh3](screenshots/targets/apollo_nh3.pdf) | [bonus](screenshots/targets/bonus.pdf) | [c12](screenshots/targets/c12.pdf) | [cu63](screenshots/targets/cu63.pdf) | [hdice](screenshots/targets/hdice.pdf) | [ld2](screenshots/targets/ld2.pdf) | [lh2](screenshots/targets/lh2.pdf) | [longitudinal](screenshots/targets/longitudinal.pdf) | [nd3](screenshots/targets/nd3.pdf) | [nh3](screenshots/targets/nh3.pdf) | [pb208](screenshots/targets/pb208.pdf) | [pb_test](screenshots/targets/pb_test.pdf) | [pol_targ](screenshots/targets/pol_targ.pdf) | [sn118](screenshots/targets/sn118.pdf) | [transverse](screenshots/targets/transverse.pdf) |

<br/>


- Beamline

  | [ELMO](screenshots/beamline/ELMO.pdf) | [FTOff](screenshots/beamline/FTOff.pdf) | [FTOn](screenshots/beamline/FTOn.pdf) | [TransverseUpstreamBeampipe](screenshots/beamline/TransverseUpstreamBeampipe.pdf) | [rghFTOn](screenshots/beamline/rghFTOn.pdf) | [rghFTOut](screenshots/beamline/rghFTOut.pdf) |

<br/>


- Ft

  | [FTOff](screenshots/ft/FTOff.pdf) | [FTOn](screenshots/ft/FTOn.pdf) | [KPP](screenshots/ft/KPP.pdf) |

<br/>


- Fc

  | [fast_field](screenshots/fc/fast_field.pdf) | [original](screenshots/fc/original.pdf) | [torus_symmetric](screenshots/fc/torus_symmetric.pdf) |

<br/>


- Ftof

  | [rga_fall2018](screenshots/ftof/rga_fall2018.pdf) |

<br/>


- Pcal

  | [rga_fall2018](screenshots/pcal/rga_fall2018.pdf) |

<br/>


- Ec

  | [rga_fall2018](screenshots/ec/rga_fall2018.pdf) |

<br/>

## CLAS12 Systems Validation

The validation performed for the CLAS12 systems includes the following workflows

- Geometry and plugin builds
- Overlap tests
- Tests specific to each system
- Validation against gemc2 geometry 
- Run dawn and archive a pdf screenshot for each variations in all systems


[![Build Geo](https://github.com/gemc/clas12-systems/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/build.yml)
[![Test Overlaps](https://github.com/gemc/clas12-systems/actions/workflows/overlaps.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/overlaps.yml)
[![CLAS12 Tests](https://github.com/gemc/clas12-systems/actions/workflows/tests.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/tests.yml)
[![Validate Geometry](https://github.com/gemc/clas12-systems/actions/workflows/validate.yml/badge.svg)](https://github.com/gemc/clas12-systems/actions/workflows/validate.yml)
[![Dawn Screenshot](https://github.com/maureeungaro/clas12-systems/actions/workflows/dawn.yml/badge.svg)](https://github.com/maureeungaro/clas12-systems/actions/workflows/dawn.yml)


<br/> 

### GEMC / Glibrary code validation

[![Compile GEMC](https://github.com/gemc/src/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/src/actions/workflows/build.yml)
[![Compile GLibrary](https://github.com/gemc/glibrary/actions/workflows/build.yml/badge.svg)](https://github.com/gemc/glibrary/actions/workflows/build.yml)

