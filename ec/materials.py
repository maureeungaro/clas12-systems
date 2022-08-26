
from gemc_api_materials import GMaterial

def define_materials(configuration):

    gmaterial = GMaterial("scintillator")
    gmaterial.description = "ec scintillator material"
    gmaterial.density = 1.032
    gmaterial.addNAtoms("C", 9)
    gmaterial.addNAtoms("H", 10)
    gmaterial.publish(configuration)

    # From $CLAS_PACK/gsim/init_ec.F
	# See also http://galileo.phys.Virginia.EDU/~lcs1h/gsim/archive/ecsim.html
	# note 240 mg/cm3 is 15 lb/ft3, which is the recommended density for bulkheads
	# See: http://www.generalplastics.com/products/rigid-foams/fr-7100

    gmaterial = GMaterial("LastaFoam")
    gmaterial.description = "ec foam material"
    gmaterial.density = 0.24
    gmaterial.addMaterialWithFractionalMass('G4_C', 0.4045)
    gmaterial.addMaterialWithFractionalMass('G4_H', 0.0786)
    gmaterial.addMaterialWithFractionalMass('G4_N', 0.1573)
    gmaterial.addMaterialWithFractionalMass('G4_O', 0.3596)
    gmaterial.publish(configuration)



