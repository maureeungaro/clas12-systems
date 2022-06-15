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

	# pcb-FR4
	# found in geant4 examples:
	# http://www.phenix.bnl.gov/~suhanov/ncc/geant/rad-source/src/ExN03DetectorConstruction.cc
	gmaterial = GMaterial("myFR4")
	gmaterial.description = "ft pcb-FR4 1.86 g/cm3"
	gmaterial.density = 1.86
	gmaterial.addMaterialWithFractionalMass("G4_C",  0.4355)
	gmaterial.addMaterialWithFractionalMass("G4_H",  0.0365)
	gmaterial.addMaterialWithFractionalMass("G4_Si", 0.2468)
	gmaterial.addMaterialWithFractionalMass("G4_O",  0.2812)
	gmaterial.publish(configuration)

	# micromegas gas: Ar/Isobutane for now, but not sure what will be used
	mmgasdensity = (1.662*0.95+2.489*0.05)*0.001
	gmaterial = GMaterial("mmgas")
	gmaterial.description = "ft micromegas gas"
	gmaterial.density = mmgasdensity
	gmaterial.addMaterialWithFractionalMass("G4_Ar", 0.95)
	gmaterial.addMaterialWithFractionalMass("G4_H",  0.0086707)
	gmaterial.addMaterialWithFractionalMass("G4_C",  0.0413293)
	gmaterial.publish(configuration)

   # micromegas strips
	mmstriptransparency = 459./559. # strips filling fraction
	mmstripdensity      = 8.96*mmstriptransparency*(15./12.) # 3 extra microns for connecting strips underneath
	ResistPasteTransparency_Density = 0.81*1.33
	gmaterial = GMaterial("mmstrips")
	gmaterial.description = "ft micromegas strips"
	gmaterial.density = mmstripdensity
	gmaterial.addMaterialWithFractionalMass("G4_Cu",  1)
	gmaterial.publish(configuration)

	# resistive strips
	# for fmt: 81% filling fraction, 1.33 density from excel file;
	# from Cern mail 12/06/16, suppose 50% C / 50% epoxy;
	# adopt C at above density.
	# thickness almost negligible, so not crucial to be exact.
	ResistPasteTransparency_Density = 0.81*1.33
	gmaterial = GMaterial("ResistPaste")
	gmaterial.description = "ft micromegas resistive strips"
	gmaterial.density = ResistPasteTransparency_Density
	gmaterial.addMaterialWithFractionalMass("G4_C",  1)
	gmaterial.publish(configuration)


	# micromegas mesh
	mmmeshtransparency = 0.55
	mmmeshdensity = 7.93*mmmeshtransparency
	gmaterial = GMaterial("mmmesh")
	gmaterial.description = "ft micromegas mesh"
	gmaterial.density = mmmeshdensity
	gmaterial.addMaterialWithFractionalMass("G4_Mn",  0.02)
	gmaterial.addMaterialWithFractionalMass("G4_Si",  0.01)
	gmaterial.addMaterialWithFractionalMass("G4_Cr",  0.19)
	gmaterial.addMaterialWithFractionalMass("G4_Ni",  0.10)
	gmaterial.addMaterialWithFractionalMass("G4_Fe",  0.68)
	gmaterial.publish(configuration)

	PhotoResist_Density = 1.42
	gmaterial = GMaterial("myPhRes")
	gmaterial.description = "ft micromegas PhotoResist"
	gmaterial.density = PhotoResist_Density
	gmaterial.addMaterialWithFractionalMass("G4_C",  1)
	gmaterial.publish(configuration)
