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
	gvolume.make_polycone('0', '360', MVftt_zpos, MVftt_iradius, MVftt_oradius)
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
		gvolume.make_tube(PRmin, PRmax, PDz, 0.0, 360.0)
		gvolume.material    = 'G4_Al'
		gvolume.set_position(0, 0, zpos)
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
		gvolume.make_tube(PRMin[ring], PRMax[ring], PDz[ring], PSPhi, PDPhi)
		gvolume.material    = 'G4_Al'
		gvolume.set_position(0, 0, z)
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
		gvolume.set_position(x, y, z)
		gvolume.set_rotation(0, 0, -rot)
		gvolume.make_box(Px, Py, Pz)
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
		gvolume.set_position(FEE_X, FEE_Y, FEE_Z)
		gvolume.set_rotation(FEE_azimuthal_angle[i], 0, 0, order='zyx')
		gvolume.make_box(FEE_HT, FEE_WD, FEE_LN)
		gvolume.material    = 'G4_Al'
		gvolume.color       = '999999'
		gvolume.publish(configuration)

		gvolume = GVolume(f'ft_trk_fee_air_{i}')
		gvolume.mother      = f'ft_trk_fee_box_{i}'
		gvolume.description = f'ft tracker fee air in box {i}'
		gvolume.make_box(FEE_A_HT, FEE_A_WD, FEE_A_LN)
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
		gvolume.make_box(flux_FEE_HT, flux_FEE_WD, flux_FEE_LN)
		gvolume.set_position(0, 0, flux_FEE_Z)
		gvolume.material    = 'G4_Galactic'
		gvolume.color       = 'aa0088'
		gvolume.set_identifier('id', 4)  
		gvolume.digitization = 'flux'
		gvolume.publish(configuration)

		flux_FEE_HT = FEE_A_HT - 2.*flux_FEE_TN
		flux_FEE_WD = flux_FEE_TN
		flux_FEE_LN = FEE_A_LN - 2.*flux_FEE_TN
		flux_FEE_Y  = - FEE_WD*0.6
		gvolume = GVolume(f'ft_trk_fee_flux_2_{i}')
		gvolume.mother      = f'ft_trk_fee_air_{i}'
		gvolume.description = f'ft tracker fee flux 2 in air in box {i}'
		gvolume.make_box(flux_FEE_HT, flux_FEE_WD, flux_FEE_LN)
		gvolume.set_position(0, flux_FEE_Y, 0)
		gvolume.material    = 'G4_Galactic'
		gvolume.color       = 'aa0088'
		gvolume.set_identifier('id', 5)
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
		gvolume.make_box(dose_FEE_HT, dose_FEE_WD, dose_FEE_LN)
		gvolume.set_position(0, dose_FEE_Y, 0)
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
	gvolume.make_tube(InnerRadius, OuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = epoxy_material
	gvolume.set_position(0, 0, z)
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
	gvolume.make_tube(InnerRadius, OuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = pcboard_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = pcboard_color
	gvolume.publish(configuration)


def place_strips(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Strips_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[2] + zrel[3])
		vname       = f'ft_trk_strips_X_L{layer_no}'
		descriptio  = f'strips X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[2] + zrel[3])
		vname       = f'ft_trk_strips_Y_L{layer_no}'
		descriptio  = f'strips Y, layer {layer_no}'

	# notice different IR and OR from above
	SInnerRadius = 70.43
	SOuterRadius = 143.66
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(SInnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = strips_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = strips_color
	gvolume.publish(configuration)

def place_kapton(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	zmin      = [     zrel[3], zrel[11] ]
	zmax      = [     zrel[4], zrel[12] ]
	PRMin     = [ InnerRadius, InnerRadius ]
	PRMax     = [ OuterRadius, 158.5 ]


	for ring in range(2):

		PDz = 0.5*( -zmin[ring] + zmax[ring] )
		ring_no = ring + 1

		if type == 1:
			z           = z0[l] - 0.5*(zmin[ring]+zmax[ring])
			vname       = f'ft_trk_kapton_X_L{layer_no}_R{ring_no}'
			descriptio  = f'kapton X, layer {layer_no}, ring {ring_no}'

		elif type == 2:
			z           = z0[l] + 0.5*(zmin[ring]+zmax[ring])
			vname       = f'ft_trk_kapton_Y_L{layer_no}_R{ring_no}'
			descriptio  = f'kapton Y, layer {layer_no}, ring {ring_no}'

		gvolume = GVolume(vname)
		gvolume.description = descriptio
		gvolume.mother      = 'ft_trk'
		gvolume.make_tube(PRMin[ring], PRMax[ring], PDz, PSPhi, PDPhi)
		gvolume.material    = kapton_material
		gvolume.set_position(0, 0, z)
		gvolume.color       = pcboard_color
		gvolume.publish(configuration)

def place_resiststrips(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = ResistStrips_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[4] + zrel[5])
		vname       = f'ft_trk_resiststrips_X_L{layer_no}'
		descriptio  = f'resistive strips X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[4] + zrel[5])
		vname       = f'ft_trk_resiststrips_Y_L{layer_no}'
		descriptio  = f'resistive strips Y, layer {layer_no}'

	# notice different IR and OR from above
	SInnerRadius = 70.43
	SOuterRadius = 143.66
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(SInnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = resistive_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = strips_color
	gvolume.publish(configuration)

def place_gas1(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Gas1_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[5] + zrel[6])
		vname       = f'ft_trk_gas1_X_L{layer_no}'
		descriptio  = f'gas1 X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[5] + zrel[6])
		vname       = f'ft_trk_gas1_Y_L{layer_no}'
		descriptio  = f'gas1 Y, layer {layer_no}'

	# notice different IR and OR from above
	SInnerRadius = 71.43
	SOuterRadius = 143.16
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(SInnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = gas_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = gas_color
	gvolume.publish(configuration)

def place_photoresist(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	zmin      = [     zrel[5],     zrel[5],                zrel[7], zrel[7] ]
	zmax      = [     zrel[6],     zrel[6], zrel[9]-2.*AluRings_Dz, zrel[9]-2.*AluRings_Dz ]
	PRMin     = [ InnerRadius,      143.16,            InnerRadius, 143.16 ]
	PRMax     = [       71.43, OuterRadius,                  71.43, OuterRadius ]


	for ring in range(4):

		ring_no = ring + 1
		PDz = 0.5*( -zmin[ring] + zmax[ring] )

		if type == 1:
			z           = z0[l] - 0.5*(zmin[ring]+zmax[ring])
			vname       = f'ft_trk_phrst_X_L{layer_no}_R{ring_no}'
			descriptio  = f'photoresist X, layer {layer_no}, ring {ring_no}'

		elif type == 2:
			z           = z0[l] + 0.5*(zmin[ring]+zmax[ring])
			vname       = f'ft_trk_phrst_Y_L{layer_no}_R{ring_no}'
			descriptio  = f'photoresist Y, layer {layer_no}, ring {ring_no}'


		gvolume = GVolume(vname)
		gvolume.description = descriptio
		gvolume.mother      = 'ft_trk'
		gvolume.make_tube(PRMin[ring], PRMax[ring], PDz, PSPhi, PDPhi)
		gvolume.material    = photoresist_material
		gvolume.set_position(0, 0, z)
		gvolume.color       = photoresist_color
		gvolume.publish(configuration)

def place_mesh(configuration, l, type):
	layer_no   = l + 1
	z          = 0.0
	PDz        = Mesh_Dz
	PSPhi      = 0.0
	PDPhi      = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[6] + zrel[7])
		vname       = f'ft_trk_mesh_X_L{layer_no}'
		descriptio  = f'mesh X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[6] + zrel[7])
		vname       = f'ft_trk_mesh_Y_L{layer_no}'
		descriptio  = f'mesh Y, layer {layer_no}'

	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(InnerRadius, OuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = mesh_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = mesh_color
	gvolume.publish(configuration)

def place_gas2(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = Gas2_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[7] + zrel[8] + 2*Photoresist_Dz)
		vname       = f'ft_trk_gas2_X_L{layer_no}'
		descriptio  = f'gas1 X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[7] + zrel[8] + 2*Photoresist_Dz)
		vname       = f'ft_trk_gas2_Y_L{layer_no}'
		descriptio  = f'gas1 Y, layer {layer_no}'

	# notice different IR and OR from above
	SInnerRadius = 67.0
	SOuterRadius = 151.5
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(SInnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = gas_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = gas_color
	gvolume.digitization = 'ft_trk'
	gvolume.set_identifier('superlayer', layer_no, 'type', type, 'segment', 1, 'strip', 1)
	gvolume.publish(configuration)

def place_driftelectrode(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = DriftElectrode_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[8] + zrel[9])
		vname       = f'ft_trk_driftel_X_L{layer_no}'
		descriptio  = f'drift electrode X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[8] + zrel[9])
		vname       = f'ft_trk_driftel_Y_L{layer_no}'
		descriptio  = f'drift electrode Y, layer {layer_no}'

	# notice different IR and OR from above
	SInnerRadius = 70.43
	SOuterRadius = 143.66
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(SInnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = 'G4_Cu'
	gvolume.set_position(0, 0, z)
	gvolume.color       = strips_color
	gvolume.publish(configuration)

def place_drift(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = DriftPCB_Dz
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	if type == 1:
		z           = z0[l] - 0.5*(zrel[9] + zrel[10])
		vname       = f'ft_trk_drift_X_L{layer_no}'
		descriptio  = f'drift X, layer {layer_no}'

	elif type == 2:
		z           = z0[l] + 0.5*(zrel[9] + zrel[10])
		vname       = f'ft_trk_drift_Y_L{layer_no}'
		descriptio  = f'drift Y, layer {layer_no}'

	# notice different OR from above
	SOuterRadius = 158.5
	gvolume = GVolume(vname)
	gvolume.description = descriptio
	gvolume.mother      = 'ft_trk'
	gvolume.make_tube(InnerRadius, SOuterRadius, PDz, PSPhi, PDPhi)
	gvolume.material    = pcboard_material
	gvolume.set_position(0, 0, z)
	gvolume.color       = pcboard_color
	gvolume.publish(configuration)

def place_rings(configuration, l, type):
	layer_no   = l + 1
	z         = 0.0
	PDz       = 0.5*5.0
	PSPhi     = 0.0
	PDPhi     = 360.000
	vname      = 'no'
	descriptio = 'no'

	zmin      = zrel[7] + 2*Photoresist_Dz
	zmax      = zrel[9]
	PRMin     = [ 60.0, 151.5 ]
	PRMax     = [ 67.0, 158.5 ]


	for ring in range(2):
		ring_no = ring + 1

		if type == 1:
			z           = z0[l] - 0.5*(zmin + zmax)
			vname       = f'ft_trk_ring_X_L{layer_no}_R{ring_no}'
			descriptio  = f'ring X, layer {layer_no}, ring {ring_no}'

		elif type == 2:
			z           = z0[l] + 0.5*(zmin + zmax)
			vname       = f'ft_trk_ring_Y_L{layer_no}_R{ring_no}'
			descriptio  = f'ring Y, layer {layer_no}, ring {ring_no}'

		gvolume = GVolume(vname)
		gvolume.description = descriptio
		gvolume.mother      = 'ft_trk'
		gvolume.make_tube(PRMin[ring], PRMax[ring], PDz, PSPhi, PDPhi)
		gvolume.material    = 'G4_Al'
		gvolume.set_position(0, 0, z)
		gvolume.color       = alu_color
		gvolume.publish(configuration)

	ang_offset = 0.0
	for ext in range(25):
		ext_no = ext + 1
		PSPhi    = - 0.5*4.9 + ext*15.0 + ang_offset
		PDPhi    = 4.9

		# an overall rotation will have to be added to place correctly
		# extensions 24 and 25 which break cylindrical symmetry
		if ext_no == 24:
			PSPhi = PSPhi - 5.0
		if ext_no == 25:
			PSPhi = PSPhi - 15.0 + 5.0

		if type == 1:
			vname       = f'ft_trk_ring_X_L{layer_no}_E{ext_no}'
			descriptio  = f'ring Y, layer {layer_no}, extension {ext_no}'
		elif type == 2:
			vname       = f'ft_trk_ring_Y_L{layer_no}_E{ext_no}'
			descriptio  = f'ring Y, layer {layer_no}, extension {ext_no}'

		gvolume = GVolume(vname)
		gvolume.description = descriptio
		gvolume.mother      = 'ft_trk'
		gvolume.make_tube(PRMax[1], OuterRadius, PDz, PSPhi, PDPhi)
		gvolume.material    = 'G4_Al'
		gvolume.set_position(0, 0, z)
		gvolume.color       = alu_color
		gvolume.publish(configuration)

