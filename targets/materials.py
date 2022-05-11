from gemc_api_materials import *

def define_materials(configuration):

	# rohacell
	gmaterial = GMaterial('rohacell')
	gmaterial.description = 'target rohacell scattering chamber material'
	gmaterial.density = 0.1 #100 mg/cm3
	gmaterial.addMaterialWithFractionalMass('G4_C', 0.6465)
	gmaterial.addMaterialWithFractionalMass('G4_H', 0.0784)
	gmaterial.addMaterialWithFractionalMass('G4_N', 0.0839)
	gmaterial.addMaterialWithFractionalMass('G4_O', 0.1912)
	gmaterial.publish(configuration)

	# epoxy
	gmaterial = GMaterial('epoxy')
	gmaterial.description = 'epoxy glue 1.16 g/cm3'
	gmaterial.density = 1.16
	gmaterial.addNAtoms('H', 32)
	gmaterial.addNAtoms('N', 2)
	gmaterial.addNAtoms('O', 4)
	gmaterial.addNAtoms('C', 15)
	gmaterial.publish(configuration)

	# carbon_fiber
	gmaterial = GMaterial('carbonFiber')
	gmaterial.description = 'carbon fiber material is epoxy and carbon - 1.75g/cm3'
	gmaterial.density = 1.75
	gmaterial.addMaterialWithFractionalMass('G4_C', 0.745)
	gmaterial.addMaterialWithFractionalMass('epoxy', 0.255)
	gmaterial.publish(configuration)

	# HDIce
	H_atomic_weight = 1.00784
	D_atomic_weight = 2.014
	H_mass_fraction = H_atomic_weight/(H_atomic_weight+D_atomic_weight)
	D_mass_fraction = D_atomic_weight/(H_atomic_weight+D_atomic_weight)
	gmaterial = GMaterial('HDIce')
	gmaterial.description = 'solid HD ice'
	gmaterial.density = 0.147
	gmaterial.addMaterialWithFractionalMass('G4_H', H_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('DeuteriumGas', D_mass_fraction)
	gmaterial.publish(configuration)

	#HDIce+Al
	HD_mass_fraction = 1 - (0.175-0.147)/(2.7-0.147)
	Al_mass_fraction = (0.175-0.147)/(2.7-0.147)
	gmaterial = GMaterial('solidHD')
	gmaterial.description = 'solidHD target material - HDIce + Al'
	gmaterial.density =0.175
	gmaterial.addMaterialWithFractionalMass('HDIce', HD_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_Al', Al_mass_fraction)
	gmaterial.publish(configuration)

	#MgB2
	Mg_atomic_weight = 24.305
	B_atomic_weight = 10.811
	Mg_mass_fraction = Mg_atomic_weight/(Mg_atomic_weight+2*B_atomic_weight)
	B_mass_fraction = 2*B_atomic_weight/(Mg_atomic_weight+2*B_atomic_weight)
	gmaterial = GMaterial('MgB2')
	gmaterial.description = 'MgB2'
	gmaterial.density = 2.57
	gmaterial.addMaterialWithFractionalMass('G4_Mg', Mg_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_B', B_mass_fraction)
	gmaterial.publish(configuration)

	#Alloy of Cu-Ni
	my_density = 8.95
	Cu_mass_fraction=0.7
	Ni_mass_fraction=0.3
	gmaterial = GMaterial('Cu70Ni30')
	gmaterial.description = 'Cupronickel 70-30'
	gmaterial.density = my_density
	gmaterial.addMaterialWithFractionalMass('G4_Cu', Cu_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_Ni', Ni_mass_fraction)
	gmaterial.publish(configuration)	

	#Polarized He3 (longitudinal target)
	gmaterial = GMaterial('polarizedHe3')
	gmaterial.description = 'polarizedHe3 target material'
	gmaterial.density = 0.000748
	gmaterial.addMaterialWithFractionalMass('Helium3Gas', 1)
	gmaterial.publish(configuration)

	# lHe coolant
	gmaterial = GMaterial('lHeCoolant')
	gmaterial.description = 'liquid He coolant for the polarized target cell'
	gmaterial.density = 0.146  
	gmaterial.addMaterialWithFractionalMass('G4_He', 1)
	gmaterial.publish(configuration)

	# NH3
	NH3_density = 0.867
	N_mass_fraction=15/18
	H_mass_fraction=3/18
	gmaterial = GMaterial('NH3')
	gmaterial.description = 'NH3 material'
	gmaterial.density = NH3_density 
	gmaterial.addMaterialWithFractionalMass('G4_N', N_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_H', H_mass_fraction)
	gmaterial.publish(configuration)

	# NH3 target with lHe3 coolant
	NH3trg_density = 0.6*0.867+0.4*0.145 # 60% of NH3 and 40% of liquid-helium
	NH3_mass_fraction=0.6*0.867/NH3trg_density 
	lHe_mass_fraction=0.4*0.145/NH3trg_density
	gmaterial = GMaterial('NH3target')
	gmaterial.description = 'solid NH3 target material'
	gmaterial.density =  NH3trg_density
	gmaterial.addMaterialWithFractionalMass('NH3', NH3_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('lHeCoolant', lHe_mass_fraction)
	gmaterial.publish(configuration)

	# G10 fiberglass
	gmaterial = GMaterial('G10')
	gmaterial.description = 'G10 - 1.70 g/cm3'
	gmaterial.density =  1.70
	gmaterial.addMaterialWithFractionalMass('G4_Si', 0.283)
	gmaterial.addMaterialWithFractionalMass('G4_O', 0.323)
	gmaterial.addMaterialWithFractionalMass('G4_C', 0.364)
	gmaterial.addMaterialWithFractionalMass('G4_H', 0.030)
	gmaterial.publish(configuration)

	# lHe gas
	gmaterial = GMaterial('HeGas')
	gmaterial.description = 'Upstream He gas'
	gmaterial.density =  0.000164  # 0.164 kg/m3 
	gmaterial.addMaterialWithFractionalMass('G4_He', 1)
	gmaterial.publish(configuration)

	# Al target cell(s)
	gmaterial = GMaterial('AlCell')
	gmaterial.description = 'Aluminum for target cells '
	gmaterial.density =  2.70  # 2.7 g/cm3 
	gmaterial.addMaterialWithFractionalMass('G4_Al', 1)
	gmaterial.publish(configuration)

	# Shim coils, need to confirm mass fractions and density
	NbTi_density=6.63
	ShimCoil_density=(1.3*8.96+NbTi_density)/2.3
	Cu_mass_fraction=29/(29+41+22)
	Nb_mass_fraction=41/(29+41+22)
	Ti_mass_fraction=22/(29+41+22)
	gmaterial = GMaterial('ShimCoil')
	gmaterial.description = 'Cu/NbTi correction coils ratio is 1.3 Cu  to 1 NbTi'
	gmaterial.density =  ShimCoil_density  #Cu=8.96 g/cm3 NbTi= 4.5 g/cm3 = Nb-47.5 wt % Ti 47.5% of the materials weight is Nb 
	gmaterial.addMaterialWithFractionalMass('G4_Cu', Cu_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_Nb', Nb_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_Ti', Ti_mass_fraction)
	gmaterial.publish(configuration)

	# Target cup walls with holes, need to confirm mass ratios
	my_density = 2.135 # 2 C, 3 F, 1 Cl
	C_mass_fraction=2*12/(2*12+3*19+35)
	F_mass_fraction=3*19/(2*12+3*19+35)
	Cl_mass_fraction=35/(2*12+3*19+35)
	gmaterial = GMaterial('AmmoniaCellWalls')
	gmaterial.description = 'PCTFE target cell walls with holes C_2ClF_3'
	gmaterial.density =  my_density  #2.10-2.17 g/cm3  has a dipole moment 
	gmaterial.addMaterialWithFractionalMass('G4_C', C_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_Cl', Cl_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('G4_F', F_mass_fraction)
	gmaterial.publish(configuration)

	# ND3 target with lHe3 coolant
	ND3targ_density = 0.6*1.007+0.4*0.145 # 60% of ND3 and 40% of liquid-helium
	ND3_mass_fraction=0.6*1.007/ND3targ_density
	lHe_mass_fraction=0.4*0.145/ND3targ_density
	gmaterial = GMaterial('ND3target')
	gmaterial.description = 'solid ND3 target'
	gmaterial.density =  ND3targ_density
	gmaterial.addMaterialWithFractionalMass('ND3', ND3_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('lHeCoolant', lHe_mass_fraction)
	gmaterial.publish(configuration)

	#liquid helium 0.145 g/cm3
	gmaterial = GMaterial('lHe')
	gmaterial.description = 'liquid helium'
	gmaterial.density =  0.145  # 0.145 g/cm3 
	gmaterial.addMaterialWithFractionalMass('G4_He',1)
	gmaterial.publish(configuration)
	
	#solid ND3 target
	my_density = 0.6*1.007+0.4*0.145 # 60% of ND3 and 40% of liquid-helium
	ND3_mass_fraction=0.6*1.007/my_density
	lHe_mass_fraction=0.4*0.145/my_density
	gmaterial = GMaterial('solidND3')
	gmaterial.description = 'solid ND3 target'
	gmaterial.density =  my_density
	gmaterial.addMaterialWithFractionalMass('ND3',ND3_mass_fraction)
	gmaterial.addMaterialWithFractionalMass('lHe',lHe_mass_fraction)
	gmaterial.publish(configuration)

	# TargetbonusGas
	gmaterial = GMaterial('bonusTargetGas')
	gmaterial.description = '7 atm deuterium gas'
	gmaterial.density =  0.00126  # in g/cm3
	gmaterial.addMaterialWithFractionalMass('DeuteriumGas',1)
	gmaterial.publish(configuration)