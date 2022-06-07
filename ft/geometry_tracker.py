from gemc_api_geometry import *
import math

from parameters import *


def buildTracker(configuration):
	make_ft_trk_mother(configuration)
	place_assembly(configuration)
	make_ft_trk_fee_boxes(configuration)
	for l in range(nlayer):
		layer_no = l + 1
		for t in range(2):
			type = t + 1
			# type 1: X layer type ? beam enters disk on drift side
			# type 2: Y layer type ? beam enters disk on bulk side
			place_epoxy(configuration, l, type)
			place_pcboard(configuration, l, type)
			place_strips(configuration, l, type)
			place_kapton(configuration, l, type)
			place_resiststrips(configuration, l, type)
			place_gas1(configuration, l, type)
			place_photoresist(configuration, l, type)
			place_mesh(configuration, l, type)
			place_gas2(configuration, l, type)
			place_driftelectrode(configuration, l, type)
			place_drift(configuration, l, type)
			place_rings(configuration, l, type)
		

def make_ft_trk_mother(configuration):
	gvolume = GVolume('ft_trk')
	gvolume.makeG4Polycone('0', '360', MVftt_zpos, MVftt_iradius, MVftt_oradius)
	gvolume.material     = 'G4_AIR'
	gvolume.description = 'FT Tracker Micromegas'
	gvolume.color       = 'aaaaff'
	gvolume.visible     = 0
	gvolume.publish(configuration)
	
	for ring in range(4):
		ring_no = ring + 1
		zmin    = CenteringSupportRing_zmin[ring]
		zmax    = CenteringSupportRing_zmax[ring]
		PDz     = 0.5*(zmax-zmin)
		zpos    = 0.5*(zmax+zmin)
		PRmin   = CenteringSupportRing_Rmin[ring]
		PRmax   = CenteringSupportRing_Rmax[ring]

		gvolume = GVolume(f'ft_trk_support_R{ring_no}')
		gvolume.mother      = 'ft_trk'
		gvolume.description = f'ft tracker centering support for ring {ring_no}'
		gvolume.makeG4Tubs(PRmin, PRmax, PDz, 0.0, 360.0)
		gvolume.material    = 'G4_Al'
		gvolume.setPosition(0, 0, zpos)
		gvolume.color       = alu_color
		gvolume.publish(configuration)



def place_assembly(configuration):
	PRMin     = [ 60.0, 158.7, 163.5 ]
	PRMax     = [ 67.0, 163.5, 170.0 ]
	PDz       = [AssemblyRing1_Dz, AssemblyRing2_Dz, AssemblyRing3_Dz ]
	zmin      = zrel[9]
	zmax      = zmin + 2.*PDz[2]
	z         = z0[0] + 0.5*(zmin+zmax)
	PSPhi     = 0.0
	PDPhi     = 360.0

	for ring in range(3):
		ring_no = ring + 1
		gvolume = GVolume(f'ft_trk_assembly_R{ring_no}')
		gvolume.mother      = 'ft_trk'
		gvolume.description = f'ft tracker assembly for ring {ring_no}'
		gvolume.makeG4Tubs(PRMin[ring], PRMax[ring], PDz[ring], PSPhi, PDPhi)
		gvolume.material    = 'G4_Al'
		gvolume.setPosition(0, 0, z)
		gvolume.color       = alu_color
		gvolume.publish(configuration)

	Px = 0.5*(158.69 - 67.0)
	Py = 0.5*3.0
	Pz = PDz[0]
	
	ang_offset = 0.
	# an overall rotation will have to be added to position correctly the 3 branches
	for branch in range(3):
		branch_no = branch + 1
		rot = branch*120.0 + ang_offset
		x   = (67.0 + Px)*math.cos(rot*math.pi/180.0)
		y   = (67.0 + Px)*math.sin(rot*math.pi/180.0)
		
		gvolume = GVolume(f'ft_trk_assembly_B{branch_no}')
		gvolume.mother      = 'ft_trk'
		gvolume.description = f'ft tracker assembly for branch {ring_no}'
		gvolume.setPosition(x, y, z)
		gvolume.setRotation(0, 0, -rot)
		gvolume.makeG4Box(Px, Py, Pz)
		gvolume.material    = 'G4_Al'
		gvolume.color       = alu_color
		gvolume.publish(configuration)


def make_ft_trk_fee_boxes(configuration):
	z_FEE_Disk = [ BLine_Z5 + 0.1, BLine_Z5 + 0.1 + FEE_Disk_LN ]

	# create arms
	for i in range(3):
		FEE_ARM_X =   (FEE_Disk_OR+ 2.+ FEE_ARM_LN*math.cos(FEE_polar_angle/degrad))*math.cos(FEE_azimuthal_angle[i]/degrad)
		FEE_ARM_Y = - (FEE_Disk_OR+ 2.+ FEE_ARM_LN*math.cos(FEE_polar_angle/degrad))*math.sin(FEE_azimuthal_angle[i]/degrad)
		FEE_ARM_Z = z_FEE_Disk[0] + FEE_Disk_LN/2. + FEE_ARM_LN*math.sin(FEE_polar_angle/degrad)
		FEE_R = (FEE_ARM_LN - FEE_HT)*math.cos(FEE_polar_angle/degrad) + (FEE_LN+FEE_Disk_LN+0.2)*math.sin(FEE_polar_angle/degrad)
		FEE_X = FEE_ARM_X + FEE_R*math.cos(FEE_azimuthal_angle[i]/degrad)
		FEE_Y = FEE_ARM_Y - FEE_R*math.sin(FEE_azimuthal_angle[i]/degrad)
		FEE_Z=  FEE_ARM_Z + (FEE_ARM_LN - FEE_HT)*math.sin(FEE_polar_angle/degrad) - (FEE_LN+FEE_Disk_LN+0.2)*math.cos(FEE_polar_angle/degrad)-50.

		gvolume = GVolume(f'ft_trk_fee_box_{i}')
		gvolume.mother      = 'ft_cal'
		gvolume.description = f'ft tracker fee box {i}'
		gvolume.setPosition(FEE_X, FEE_Y, FEE_Z)
		gvolume.setRotation(FEE_azimuthal_angle[i], 0, 0, order='zyx')
		gvolume.makeG4Box(FEE_HT, FEE_WD, FEE_LN)
		gvolume.material    = 'G4_Al'
		gvolume.color       = '999999'
		gvolume.publish(configuration)

		gvolume = GVolume(f'ft_trk_fee_air_{i}')
		gvolume.mother      = f'ft_trk_fee_box_{i}'
		gvolume.description = f'ft tracker fee air in box {i}'
		gvolume.makeG4Box(FEE_A_HT, FEE_A_WD, FEE_A_LN)
		gvolume.material    = 'G4_AIR'
		gvolume.color       = 'CCFFFF'
		gvolume.publish(configuration)

		flux_FEE_TN = 0.5
		flux_FEE_HT = FEE_A_HT - 2.*flux_FEE_TN
		flux_FEE_WD = FEE_A_WD - 2.*flux_FEE_TN
		flux_FEE_LN = flux_FEE_TN
		flux_FEE_Z  = -FEE_A_LN + flux_FEE_TN
		gvolume = GVolume(f'ft_trk_fee_flux_1_{i}')
		gvolume.mother      = f'ft_trk_fee_air_{i}'
		gvolume.description = f'ft tracker fee flux 1 in air in box {i}'
		gvolume.makeG4Box(flux_FEE_HT, flux_FEE_WD, flux_FEE_LN)
		gvolume.setPosition(0, 0, flux_FEE_Z)
		gvolume.material    = 'G4_Galactic'
		gvolume.color       = 'aa0088'
		gvolume.setIdentifier('id', 4)  
		gvolume.digitization = 'flux'
		gvolume.publish(configuration)

		flux_FEE_HT = FEE_A_HT - 2.*flux_FEE_TN
		flux_FEE_WD = flux_FEE_TN
		flux_FEE_LN = FEE_A_LN - 2.*flux_FEE_TN
		flux_FEE_Y  = - FEE_WD*0.6
		gvolume = GVolume(f'ft_trk_fee_flux_2_{i}')
		gvolume.mother      = f'ft_trk_fee_air_{i}'
		gvolume.description = f'ft tracker fee flux 2 in air in box {i}'
		gvolume.makeG4Box(flux_FEE_HT, flux_FEE_WD, flux_FEE_LN)
		gvolume.setPosition(0, flux_FEE_Y, 0)
		gvolume.material    = 'G4_Galactic'
		gvolume.color       = 'aa0088'
		gvolume.setIdentifier('id', 5)
		gvolume.digitization = 'flux'
		gvolume.publish(configuration)

		dose_FEE_TN = 5.
		dose_FEE_HT = FEE_A_HT - dose_FEE_TN
		dose_FEE_WD = dose_FEE_TN
		dose_FEE_LN = FEE_A_LN - dose_FEE_TN
		dose_FEE_Y  = 0.
		gvolume = GVolume(f'ft_trk_fee_dose_{i}')
		gvolume.mother      = f'ft_trk_fee_air_{i}'
		gvolume.description = f'ft tracker fee dose in air in box {i}'
		gvolume.makeG4Box(dose_FEE_HT, dose_FEE_WD, dose_FEE_LN)
		gvolume.setPosition(0, dose_FEE_Y, 0)
		gvolume.material    = 'scintillator'
		gvolume.color       = '003300'
		gvolume.publish(configuration)



def place_epoxy(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[0] + zrel[1])
		vname       = f'ft_trk_epoxy_X_L{layer_no}'
		descriptio  = f'epoxy X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[0] + zrel[1])
		vname       = f'ft_trk_epoxy_Y_L{layer_no}'
		descriptio  = f'epoxy Y, layer {layer_no}'

	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.makeG4Tubs(InnerRadius, OuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = epoxy_material
	gvolume.setPosition(0, 0, z)
	gvolume.color       = epoxy_color
	gvolume.publish(configuration)

	
def place_pcboard(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = PCB_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[1] + zrel[2])
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[1] + zrel[2])
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.makeG4Tubs(InnerRadius, OuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = pcboard_material
	gvolume.setPosition(0, 0, z)
	gvolume.color       = pcboard_color
	gvolume.publish(configuration)


def place_strips(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_kapton(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_resiststrips(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_gas1(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_photoresist(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_mesh(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_gas2(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_driftelectrode(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_drift(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

def place_rings(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Epoxy_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		vname       = f'ft_trk_pcboard_X_L{layer_no}'
		descriptio  = f'pc board X, layer {layer_no}'

	elif type == 2:
		vname       = f'ft_trk_pcboard_Y_L{layer_no}'
		descriptio  = f'pc board Y, layer {layer_no}'

