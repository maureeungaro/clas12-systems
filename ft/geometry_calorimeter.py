from gemc_api_geometry import *
import math


from parameters import *


def buildCalorimeter(configuration):
	buildCalMotherVolume(configuration)
	buildCrystalsMother(configuration)
	buildCrystals(configuration)
	buildCalCopper(configuration)
	buildCalMotherBoard(configuration)
	buildCalLed(configuration)
	buildCalTungstenCup(configuration)
	buildCalInsulation(configuration)
	buildCalShell(configuration)
	buildCalBeamline(configuration)
	make_ft_cal_flux(configuration)
	make_ft_moellerdisk(configuration)


def make_ft_pipe(configuration):
	buildCalMotherVolume(configuration)
	buildCalBeamline(configuration)


def buildCalMotherVolume(configuration):
	z_plane_FT = [O_Shell_Z1,     2098.,  TPlate_ZM,   BLine_Z4,  BLine_Z4, BLine_Z5]
	iradius_FT = [  BLine_MR,  BLine_MR,   BLine_MR,  TPlate_MR,  BLine_OR, BLine_OR]
	oradius_FT = [     700.0,     700.0,      238.0,      238.0,     238.0,    238.0]

	gvolume = GVolume('ft_cal')

	# a G4Polycone is built with the same geant4 constructor parameters, in the same order.
	# an additional argument at the end can be given to specify the length units (default is mm)
	gvolume.makeG4Polycone('0', '360', z_plane_FT, iradius_FT, oradius_FT)
	gvolume.material     = 'G4_AIR'
	gvolume.description = 'Calorimeter Mother Volume'
	gvolume.color       = '1437f4'
	gvolume.style       = 0
	gvolume.visible     = 0
	gvolume.publish(configuration)


def buildCrystalsMother(configuration):

	z_plane_FT_CRY = [ Idisk_Z - Idisk_LT, Idisk_Z + Idisk_LT]
	iradius_FT_CRY = [           Idisk_IR,           Idisk_IR]
	oradius_FT_CRY = [           Odisk_OR,           Odisk_OR]

	gvolume = GVolume('ft_calCrystalsMother')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Calorimeter Crystal Volume'
	gvolume.makeG4Polycone('0', '360', z_plane_FT_CRY, iradius_FT_CRY, oradius_FT_CRY)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = '1437f4'
	gvolume.style       = 0
	gvolume.publish(configuration)


def buildCrystals(configuration):
	centX =  int(Nx/2)  + 0.5
	centY =  int(Ny/2)  + 0.5
	locX=0.0
	locY=0.0
	locZ=0.0
	dX=0.0
	dY=0.0
	dZ=0.0
	for iX in range(1, Nx+1):
		for iY in range(1, Ny+1):

			locX = (iX - centX)*Vwidth
			locY= (iY - centY)*Vwidth
			locR=math.sqrt(locX*locX + locY*locY)

			if(locR>60.0 and locR < Vwidth*11):

				# crystal mother volume
				dX = Vwidth/2.0
				dY = Vwidth/2.0
				dZ = Vlength/2.0
				locZ = Vfront + Vlength/2.0
				gvolume = GVolume(f'ft_cal_cr_motherVolume_h{iX}_v{iY}')
				gvolume.mother      = 'ft_calCrystalsMother'
				gvolume.description = f'Mother Volume for crystal h:{iX}, v:{iY}'
				gvolume.make_box(dX, dY, dZ)
				gvolume.material    = 'G4_AIR'
				gvolume.set_position(locX, locY, locZ)
				gvolume.color       = '838EDE'
				gvolume.style       = 0
				gvolume.publish(configuration)

				# APD housing
				dX = Swidth/2.0
				dY = Swidth/2.0
				dZ = Slength/2.0
				locZ = Sfront + Slength/2.
				gvolume = GVolume(f'ft_cal_cr_apd_h{iX}_v{iY}')
				gvolume.mother      = 'ft_calCrystalsMother'
				gvolume.description = f'apd for crystal h:{iX}, v:{iY}'
				gvolume.make_box(dX, dY, dZ)
				gvolume.material    = 'ft_peek'
				gvolume.set_position(locX, locY, locZ)
				gvolume.color       = '99CC66'
				gvolume.publish(configuration)

				# Wrapping Volume
				dX = Wwidth/2.0
				dY = Wwidth/2.0
				dZ = Vlength/2.0
				locX=0.0
				locY=0.0
				locZ=0.0
				gvolume = GVolume(f'ft_cal_cr_wrap_h{iX}_v{iY}')
				gvolume.mother      = f'ft_cal_cr_motherVolume_h{iX}_v{iY}'
				gvolume.description = f'wrapping for crystal h:{iX}, v:{iY}'
				gvolume.make_box(dX, dY, dZ)
				gvolume.material    = 'G4_MYLAR'
				gvolume.set_position(locX, locY, locZ)
				gvolume.color       = '838EDE'
				gvolume.publish(configuration)

				# PbWO4 Crystal
				dX = Cwidth/2.0
				dY = Cwidth/2.0
				dZ = Clength/2.0
				locX=0.0
				locY=0.0
				locZ = Flength/2.
				gvolume = GVolume(f'ft_cal_cr_h{iX}_v{iY}')
				gvolume.mother       = f'ft_cal_cr_wrap_h{iX}_v{iY}'
				gvolume.description  = f'PbWO4 crystal h:{iX}, v:{iY}'
				gvolume.make_box(dX, dY, dZ)
				gvolume.material     = 'G4_PbWO4'
				gvolume.set_position(locX, locY, locZ)
				gvolume.color        = '836FFF'
				gvolume.digitization = 'ft_cal'
				gvolume.set_identifier('ih', iX, 'iv', iY)
				gvolume.publish(configuration)

				# LED housing
				dX = Fwidth/2.0
				dY = Fwidth/2.0
				dZ = Flength/2.0
				locX=0.0
				locY=0.0
				locZ = -Vlength/2.0 + Flength/2.0
				gvolume = GVolume(f'ft_cal_cr_ledHousing_h{iX}_v{iY}')
				gvolume.mother      = f'ft_cal_cr_wrap_h{iX}_v{iY}'
				gvolume.description = f'Led Housing for crystal h:{iX}, v:{iY}'
				gvolume.make_box(dX, dY, dZ)
				gvolume.material    = 'ft_peek'
				gvolume.set_position(locX, locY, locZ)
				gvolume.color       = 'EEC900'
				gvolume.publish(configuration)


def buildCalCopper(configuration):
	# back
	gvolume = GVolume('ft_cal_back_copper')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'ft calorimeter back copper'
	gvolume.make_tube(Bdisk_IR, Bdisk_OR, Bdisk_TN, 0.0, 360.0)
	gvolume.material    = 'G4_Cu'
	gvolume.set_position(0, 0, Bdisk_Z)
	gvolume.color       = 'CC6600'
	gvolume.publish(configuration)
	# front
	gvolume = GVolume('ft_cal_front_copper')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'calorimeter front copper'
	gvolume.make_tube(Fdisk_IR, Fdisk_OR, Fdisk_TN, 0.0, 360.0)
	gvolume.material    = 'G4_Cu'
	gvolume.set_position(0, 0, Fdisk_Z)
	gvolume.color       = 'CC6600'
	gvolume.publish(configuration)
	# inner
	gvolume = GVolume('ft_cal_inner_copper')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'calorimeterinnerouter copper'
	gvolume.make_tube(Idisk_IR, Idisk_OR, Idisk_LT, 0.0, 360.0)
	gvolume.material    = 'G4_Cu'
	gvolume.set_position(0, 0, Odisk_Z)
	gvolume.color       = 'CC6600'
	gvolume.publish(configuration)
	# outer
	gvolume = GVolume('ft_cal_outer_copper')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'calorimeter outer copper'
	gvolume.make_tube(Odisk_IR, Odisk_OR, Odisk_LT, 0.0, 360.0)
	gvolume.material    = 'G4_Cu'
	gvolume.set_position(0, 0, Odisk_Z)
	gvolume.color       = 'CC6600'
	gvolume.publish(configuration)
	# Preamp Space
	gvolume = GVolume('ft_cal_back_plate')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'calorimeter preamp space back_plate'
	gvolume.make_tube(BPlate_IR, BPlate_OR, BPlate_TN, 0.0, 360.0)
	gvolume.material    = 'G4_AIR'
	gvolume.set_position(0, 0, BPlate_Z)
	gvolume.color       = '7F9A65'
	gvolume.publish(configuration)

def buildCalMotherBoard(configuration):
	# MotherBoard
	gvolume = GVolume('ft_cal_back_mtb')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'calorimeter back motherboard'
	gvolume.make_tube(Bmtb_IR, Bmtb_OR, Bmtb_TN, 0.0, 360.0)
	gvolume.material    = 'pcboard'
	gvolume.set_position(0, 0, Bmtb_Z)
	gvolume.color       = '0B3B0B'
	gvolume.publish(configuration)

	for i in range(4):
		Bmtb_hear_DX =  (Bmtb_OR + Bmtb_hear_LN - Bmtb_hear_D0)*math.cos(Bmtb_angle[i]/degrad)
		Bmtb_hear_DY = -(Bmtb_OR + Bmtb_hear_LN - Bmtb_hear_D0)*math.sin(Bmtb_angle[i]/degrad)
		gvolume = GVolume(f'ft_cal_back_mtb_h{i}')
		gvolume.mother      = 'ft_cal'
		gvolume.description = f'back motherboard  h:{i}'
		gvolume.make_box(Bmtb_hear_LN, Bmtb_hear_WD, Bmtb_TN)
		gvolume.material    = 'pcboard'
		gvolume.set_position(Bmtb_hear_DX, Bmtb_hear_DY, Bmtb_Z)
		gvolume.set_rotation(0, 0, Bmtb_angle[i])
		gvolume.color       = '0B3B0B'
		gvolume.publish(configuration)


def buildCalLed(configuration):
	# LED assembly
	gvolume = GVolume('ft_cal_led')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'ft calorimeter LED Assembly'
	gvolume.make_tube(LED_IR, LED_OR, LED_TN, 0.0, 360.0)
	gvolume.material    = 'ft_peek'
	gvolume.set_position(0, 0, LED_Z)
	gvolume.color       = '333333'
	gvolume.publish(configuration)


def buildCalTungstenCup(configuration):

	z_plane_TCup = [  BCup_Z1, BCup_ZM]
	iradius_TCup = [ BCup_IRM, BCup_IRM]
	oradius_TCup = [ BCup_OR1, BCup_ORM]

	gvolume = GVolume('ft_cal_tcup_back')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'tungsten cup and cone at the back of the ft, back part'
	gvolume.makeG4Polycone('0', '360', z_plane_TCup, iradius_TCup, oradius_TCup)
	gvolume.material    = 'ft_W'
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)


	z_plane_TCup = [  BCup_ZM, BCup_ZE]
	iradius_TCup = [ I_Ins_OR, I_Ins_OR]
	oradius_TCup = [ BCup_ORM, BCup_ORE]

	gvolume = GVolume('ft_cal_tcup_plate')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'stainless steel plate at the back of the ft'
	gvolume.makeG4Polycone('0', '360', z_plane_TCup, iradius_TCup, oradius_TCup)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.color       = 'cccccc'
	gvolume.publish(configuration)

	z_plane_TCup = [  BCup_ZB, BCup_Z2]
	iradius_TCup = [ BCup_IRM, BCup_IRM]
	oradius_TCup = [ BCup_ORB, BCup_OR2]

	gvolume = GVolume('ft_cal_tcup_front')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'tungsten cup and cone at the back of the ft, front part'
	gvolume.makeG4Polycone('0', '360', z_plane_TCup, iradius_TCup, oradius_TCup)
	gvolume.material    = 'ft_W'
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)


	z_plane_TCup = [  BCup_Z1, BCup_Z2]
	iradius_TCup = [ BCup_IRM, BCup_IRM]
	oradius_TCup = [ BCup_OR1, BCup_OR2]

	for i in range(4):

		biangle = BCup_iangle[i]
		bdangle = BCup_dangle[i]

		gvolume = GVolume(f'ft_cal_tcup_m{i+1}')
		gvolume.mother      = 'ft_cal'
		gvolume.description = f'tungsten cup and cone at the back of the ft, medium part {i+1}'
		gvolume.makeG4Polycone(biangle, bdangle, z_plane_TCup, iradius_TCup, oradius_TCup)
		gvolume.material    = 'ft_W'
		gvolume.color       = 'ff0000'
		gvolume.publish(configuration)


def make_ft_cal_flux(configuration):
	# flux on the back of the crystals
	Flux_TN = Sgap/2         # flux detector half thickness defined as a function of the gap between sensor and crystals
	Flux_IR = Bdisk_IR       # inner radius is defined equal to copper back disk
	Flux_OR = Bdisk_OR       # outer radius is defined equal to copper front disk
	Flux_Z =  Vfront + Vlength + Flux_TN
	gvolume = GVolume('ft_cal_flux')
	gvolume.mother      = 'ft_calCrystalsMother'
	gvolume.description = 'ft flux'
	gvolume.make_tube(Flux_IR, Flux_OR, Flux_TN, 0.0, 360.0)
	gvolume.material    = 'G4_Galactic'
	gvolume.set_position(0, 0, Flux_Z)
	gvolume.color       = 'aa0088'
	gvolume.set_identifier('id', 3)  # identifier for ft_cal_flux
	gvolume.digitization = 'flux'
	gvolume.publish(configuration)


def make_ft_moellerdisk(configuration):


	# flux in front of tagger
	disk_zpos    = [ 281.0 , O_Shell_Z1 - 0.05 ]
	disk_iradius = [   2.0 ,   56.0 ]
	disk_oradius = [ 150.0 ,  150.0 ]

	for n in range(1,2):

		idisk = n + 1

		gvolume = GVolume(f'moller_disk_{n}')
		gvolume.mother      = 'root'
		gvolume.description = f'Moller disk {n}'
		gvolume.make_tube(disk_iradius[n], disk_oradius[n], 0.05, 0.0, 360.0)
		gvolume.material    = 'G4_Galactic'
		gvolume.set_position(0, 0, disk_zpos[n])
		gvolume.color       = 'aa0088'
		gvolume.visible     = 0
		gvolume.set_identifier('id', idisk)  # identifier for moller_disk
		gvolume.digitization = 'flux'
		gvolume.publish(configuration)



# Calorimeter Insulation
def buildCalInsulation(configuration):
	
	# inner
	gvolume = GVolume('ft_cal_inner_ins')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Inner Insulation'
	gvolume.make_tube(I_Ins_IR, I_Ins_OR, I_Ins_LT, 0.0, 360.0)
	gvolume.material    = 'insfoam'
	gvolume.set_position(0, 0, I_Ins_Z)
	gvolume.color       = 'F5F6CE'
	gvolume.publish(configuration)

	# outer front
	z_plane_O_Ins = [ O_Ins_Z1, O_Ins_Z2, O_Ins_Z2, O_Ins_Z3, O_Ins_Z4 ]
	iradius_O_Ins = [ O_Ins_I1, O_Ins_I1, O_Ins_I2, O_Ins_I3, O_Ins_I4 ]
	oradius_O_Ins = [ O_Ins_O1, O_Ins_O2, O_Ins_O2, O_Ins_O3, O_Ins_O4 ]
	gvolume = GVolume('ft_cal_outer_ins_f')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Outer Insulation front'
	gvolume.makeG4Polycone(0, 360, z_plane_O_Ins, iradius_O_Ins, oradius_O_Ins)
	gvolume.material    = 'insfoam'
	gvolume.color       = 'F5F6CE'
	gvolume.publish(configuration)

	# outer back
	z_plane_O_Ins = [ O_Ins_Z5, O_Ins_Z6, O_Ins_Z7, O_Ins_Z8, O_Ins_Z8, O_Ins_Z9, O_Ins_Z10, O_Ins_Z11 ]
	iradius_O_Ins = [ O_Ins_I5, O_Ins_I6, O_Ins_I7, O_Ins_I8, O_Ins_I9, O_Ins_I9, O_Ins_I10, O_Ins_I11 ]
	oradius_O_Ins = [ O_Ins_O5, O_Ins_O6, O_Ins_O7, O_Ins_O8, O_Ins_O8, O_Ins_O9, O_Ins_O10, O_Ins_O11 ]
	gvolume = GVolume('ft_cal_outer_ins_b')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Outer Insulation back'
	gvolume.makeG4Polycone(0, 360, z_plane_O_Ins, iradius_O_Ins, oradius_O_Ins)
	gvolume.material    = 'insfoam'
	gvolume.color       = 'F5F6CE'
	gvolume.publish(configuration)

	# outer medium
	z_plane_O_Ins = [ O_Ins_Z5, O_Ins_Z4 ]
	iradius_O_Ins = [ O_Ins_I5, O_Ins_I4 ]
	oradius_O_Ins = [ O_Ins_O5, O_Ins_O4 ]

	for i in range(4):
		gvolume = GVolume(f'ft_cal_outer_ins_m{i+1}')
		gvolume.mother      = 'ft_cal'
		gvolume.description = f'Outer Insulation medium {i+1}'
		biangle = BCup_iangle[i]
		bdangle = BCup_dangle[i]
		gvolume.makeG4Polycone(biangle, bdangle, z_plane_O_Ins, iradius_O_Ins, oradius_O_Ins)
		gvolume.material    = 'insfoam'
		gvolume.color       = 'F5F6CE'
		gvolume.publish(configuration)




# Outer Shell
def buildCalShell(configuration):
	# outer front
	z_plane_O_Shell = [ O_Shell_Z1, O_Shell_Z2, O_Shell_Z2, O_Shell_Z3, O_Shell_Z4 ]
	iradius_O_Shell = [ O_Shell_I1, O_Shell_I1, O_Shell_I2, O_Shell_I3, O_Shell_I4 ]
	oradius_O_Shell = [ O_Shell_O1, O_Shell_O2, O_Shell_O2, O_Shell_O3, O_Shell_O4 ]
	gvolume = GVolume('ft_cal_outer_shell_f')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Outer Shell front'
	gvolume.makeG4Polycone(0, 360, z_plane_O_Shell, iradius_O_Shell, oradius_O_Shell)
	gvolume.material    = 'carbonFiber'
	gvolume.color       = 'F5DA81'
	gvolume.publish(configuration)

	# outer back
	z_plane_O_Shell = [ O_Shell_Z5, O_Shell_Z6, O_Shell_Z7, O_Shell_Z8, O_Shell_Z9, O_Shell_Z10, O_Shell_Z11, O_Shell_Z12, O_Shell_Z13 ]
	iradius_O_Shell = [ O_Shell_I5, O_Shell_I6, O_Shell_I7, O_Shell_I8, O_Shell_I9, O_Shell_I10, O_Shell_I11, O_Shell_I12, O_Shell_I13 ]
	oradius_O_Shell = [ O_Shell_O5, O_Shell_O6, O_Shell_O7, O_Shell_O8, O_Shell_O9, O_Shell_O10, O_Shell_O11, O_Shell_O12, O_Shell_O13 ]
	gvolume = GVolume('ft_cal_outer_shell_b')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'Outer Shell back'
	gvolume.makeG4Polycone(0, 360, z_plane_O_Shell, iradius_O_Shell, oradius_O_Shell)
	gvolume.material    = 'carbonFiber'
	gvolume.color       = 'F5DA81'
	gvolume.publish(configuration)

	# outer medium
	z_plane_O_Shell = [ O_Shell_Z5, O_Shell_Z4 ]
	iradius_O_Shell = [ O_Shell_I5, O_Shell_I4 ]
	oradius_O_Shell = [ O_Shell_O5, O_Shell_O4 ]
	for i in range(4):
		gvolume = GVolume(f'ft_cal_outer_shell_m{i+1}')
		gvolume.mother      = 'ft_cal'
		gvolume.description = f'Outer Shell medium{i+1}'
		biangle = BCup_iangle[i]
		bdangle = BCup_dangle[i]
		gvolume.makeG4Polycone(biangle, bdangle, z_plane_O_Shell, iradius_O_Shell, oradius_O_Shell)
		gvolume.material    = 'carbonFiber'
		gvolume.color       = 'F5DA81'
		gvolume.publish(configuration)


def buildCalBeamline(configuration):
	TPlate_IR= BLine_IR + BLine_TN
	TPlate_OR= TPlate_Z1*BCup_tang

	z_plane_TPlate = [ TPlate_Z1, TPlate_ZM, TPlate_Z2 ]
	iradius_TPlate = [ TPlate_IR, TPlate_IR, TPlate_MR ]
	oradius_TPlate = [ TPlate_OR, TPlate_OR, TPlate_OR ]

	gvolume = GVolume('ft_cal_tplate')
	gvolume.mother      = 'ft_cal'
	gvolume.description = 'ft tungsten plate'
	gvolume.makeG4Polycone(0, 360, z_plane_TPlate, iradius_TPlate, oradius_TPlate)
	gvolume.material    = 'ft_W'
	gvolume.color       = 'ff0000'
	gvolume.publish(configuration)


