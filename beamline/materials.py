from gemc_api_materials import GMaterial

def define_materials(configuration): 
	# tungsten alloy
	gmaterial = GMaterial('beamline_W')
	gmaterial.description = 'beamline tungsten alloy 17.6 g/cm3'
	gmaterial.density = 17.6
	gmaterial.addMaterialWithFractionalMass('G4_Fe', 0.08)
	gmaterial.addMaterialWithFractionalMass('G4_W',  0.92)
	gmaterial.publish(configuration)
