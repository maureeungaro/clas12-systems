from gemc_api_materials import GMaterial

def define_materials(configuration): 
	
	gmaterial = GMaterial("ft_peek")
	gmaterial.description = "ft peek plastic 1.31 g/cm3"
	gmaterial.density = 1.31
	gmaterial.addMaterialWithFractionalMass("G4_C", 0.76)
	gmaterial.addMaterialWithFractionalMass("G4_H", 0.08)
	gmaterial.addMaterialWithFractionalMass("G4_O", 0.16)
	gmaterial.publish(configuration)
	
	gmaterial = GMaterial("pcboard")
	gmaterial.description = "ft pcb 1.86 g/cm3"
	gmaterial.density = 1.86
	gmaterial.addMaterialWithFractionalMass("G4_Fe", 0.3)
	gmaterial.addMaterialWithFractionalMass("G4_C",  0.4)
	gmaterial.addMaterialWithFractionalMass("G4_Si", 0.3)
	gmaterial.publish(configuration)
	
	gmaterial = GMaterial("insfoam")
	gmaterial.description = "ft insulation foam 34 kg/m3"
	gmaterial.density = 0.034
	gmaterial.addMaterialWithFractionalMass("G4_C", 0.6)
	gmaterial.addMaterialWithFractionalMass("G4_H", 0.1)
	gmaterial.addMaterialWithFractionalMass("G4_N", 0.1)
	gmaterial.addMaterialWithFractionalMass("G4_O", 0.2)
	gmaterial.publish(configuration)
	
	gmaterial = GMaterial("ft_W")
	gmaterial.description = "ft tungsten alloy 17.6 g/cm3"
	gmaterial.density = 17.6
	gmaterial.addMaterialWithFractionalMass("G4_Fe", 0.08)
	gmaterial.addMaterialWithFractionalMass("G4_W",  0.92)
	gmaterial.publish(configuration)

	gmaterial = GMaterial("carbonFiber")
	gmaterial.description = "ft carbon fiber material is epoxy and carbon - 1.75g/cm3"
	gmaterial.density = 1.75
	gmaterial.addMaterialWithFractionalMass("G4_C",  0.745)
	gmaterial.addMaterialWithFractionalMass("epoxy", 0.255)
	gmaterial.publish(configuration)

	gmaterial = GMaterial("epoxy")
	gmaterial.description = "epoxy glue 1.16 g/cm3"
	gmaterial.density = 1.16
	gmaterial.addNAtoms("H",  32)
	gmaterial.addNAtoms("N",   2)
	gmaterial.addNAtoms("O",   4)
	gmaterial.addNAtoms("C",  15)
	gmaterial.publish(configuration)

	gmaterial = GMaterial("scintillator")
	gmaterial.description = "ft scintillator material C9H10 1.032 g/cm3"
	gmaterial.density = 1.032
	gmaterial.addNAtoms("C",  9)
	gmaterial.addNAtoms("H",  10)
	gmaterial.publish(configuration)
