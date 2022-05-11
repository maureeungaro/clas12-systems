from gemc_api_geometry import *

import math


def _make_full_tube(gvolume, r_in, r_out, half_length):
	gvolume.makeG4Tubs(r_in, r_out, half_length, 0.0, 360.0)


def _build_nuclear_target_foil(
			material,
			name_prefix,
			descr_prefix,
			z_center,
			half_length,
			r_in=0.0,
			r_out=5.0,
			color="aa0000",
		):

			gvolume = GVolume(f"{name_prefix}NuclearTargFoil")
			gvolume.mother = "target"
			gvolume.description = f"{descr_prefix} foil for EG2p Nuclear Targets Assembly"
			gvolume.material = material
			gvolume.color = color
			_make_full_tube(gvolume, r_in, r_out, half_length)
			gvolume.setPosition(0., 0., z_center)
			return gvolume


def build_geometry_lhydrogen(configuration):

	variation = configuration.variation
	material_varmap = {
		"lh2": "G4_lH2",
		"ld2": "LD2",
	}

	z_plane_varmap = {
		"lh2": [-140.0, 265.0, 280.0, 280.0],
		"ld2": [-140.0, 265.0, 280.0, 280.0],
	}

	def build_vacuum_container():
		n_planes = 4
		phi_start = 0
		phi_total = 360 
		z_plane 	= z_plane_varmap[variation]
		outer_radius = [50.3, 50.3, 21.1, 21.1]
		inner_radius = [0.0]*len(outer_radius)

		# Vacuum Target Container
		gvolume = GVolume('target')
		gvolume.description = f'Liquid Hydrogen Target Container for variation {variation}'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = 'G4_Galactic'	# from GEANT4 materials database
		gvolume.color = '22ff22'
		gvolume.style = 0
		return gvolume
	
	def build_target_cell():
		n_planes = 5
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-24.2, -21.2, 22.5, 23.5, 24.5]
		outer_radius = [2.5,  10.3,  7.3,  5.0,  2.5]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume("lh2")
		gvolume.mother = "target"
		gvolume.description = f'Liquid Hydrogen Target Cell for variation {variation}'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = material_varmap[variation]
		gvolume.color = 'aa0000'
		return gvolume

	for builder in [
		build_vacuum_container,
		build_target_cell
	]: 
		volume = builder()
		volume.publish(configuration)


def build_geometry_pol_targ(configuration):
	
	def build_vacuum_container():
		r_in = 0
		r_out = 44
		half_length = 130
		gvolume = GVolume("PolTarg")
		gvolume.description = "PolTarg Region"
		gvolume.color = "aaaaaa9"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Galactic"
		return gvolume
	
	def build_lhe_between_target_cells():
		z_center = 0  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 14.97  # half length along beam axis
		gvolume = GVolume("LHeVoidFill")
		gvolume.mother = "PolTarg"
		gvolume.description = "LHe between target cells"
		gvolume.color = "0000ff"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "lHeCoolant"
		return gvolume
	
	def build_upstream_nh3_target_cell():
		z_center = -25  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 9.96  # half length along beam axis
		gvolume = GVolume("NH3Targ")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 target cell"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "f000f0"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "NH3target"
		return gvolume

	def build_upstream_nh3_target_cup():
		z_center = -25
		r_in = 10.0001  # radius in mm
		r_out = 10.03  # radius in mm
		half_length = 9.75  # half length along beam axis
		gvolume = GVolume("NH3Cup")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_upstream_nh3_target_cup_downstream_ring():
		z_center = -35
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("NH3CupDSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup downstream ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_upstream_nh3_target_cup_upstream_ring():
		z_center = -15
		r_in = 10.0001  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("NH3CupUSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Upstream ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_upstream_nh3_target_cup_window_frame():
		z_center = -35
		r_in = 11.44  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 1.5875  # half length along beam axis
		gvolume = GVolume("NH3CupWindowFrame_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Window frame"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_upstream_nh3_target_cup_upstream_window():
		z_center = -35
		r_in = 0  # radius in mm
		r_out = 10  # radius in mm
		half_length = 0.025  # half length along beam axis	
		gvolume = GVolume("NH3CupUSWindow_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Upstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_upstream_nh3_target_cup_downstream_window():
		z_center = -15
		r_in = 0  # radius in mm
		r_out = 10  # radius in mm
		half_length = 0.025  # half length along beam axis
		gvolume = GVolume("NH3CupDSWindow")
		gvolume.mother = "PolTarg"
		gvolume.description = "Upstream NH3 Target cup Downstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_downstream_nd3_target_cell():
		z_center = 25  # center location of target along beam axis
		r_in = 0
		r_out = 10  # radius in mm
		half_length = 9.96  # half length along beam axis	
		gvolume = GVolume("ND3Targ")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 target cell"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "f000f0"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ND3target"
		return gvolume

	def build_downstream_nd3_target_cup():
		z_center = 25
		r_in = 10.0001  # radius in mm
		r_out = 10.03  # radius in mm
		half_length = 9.75  # half length along beam axis
		gvolume = GVolume("ND3Cup")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_downstream_nd3_target_cup_downstream_ring():
		z_center = 35
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("ND3CupDSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup downstream ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_downstream_nd3_target_cup_upstream_ring():
		z_center = 15
		r_in = 10.0001  # radius in mm
		r_out = 11.43  # radius in mm
		half_length = 0.25  # half length along beam axis
		gvolume = GVolume("ND3CupUSRing")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstrem ND3 Target cup Upstream ring"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_downstream_nd3_target_cup_window_frame():
		z_center = 15
		r_in = 11.44  # radius in mm
		r_out = 12.7  # radius in mm
		half_length = 1.5875  # half length along beam axis
		gvolume = GVolume("ND3CupWindowFrame_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup Window frame"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "ffffff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_downstream_nd3_target_cup_upstream_window():
		z_center = 35
		r_in = 0.0  # radius in mm
		r_out = 10.0  # radius in mm
		half_length = 0.025  # half length along beam axis	
		gvolume = GVolume("ND3CupUSWindow_20")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup Upstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_downstream_nd3_target_cup_downstream_window():
		z_center = 15
		r_in = 0.0  # radius in mm
		r_out = 10.0  # radius in mm
		half_length = 0.025  # half length along beam axis	
		gvolume = GVolume("ND3CupDSWindow")
		gvolume.mother = "PolTarg"
		gvolume.description = "Downstream ND3 Target cup Downstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_bath_entrance_window_part_7a():
		z_center = -37.395
		r_in = 0.0  # radius in mm
		r_out = 11.5  # radius in mm
		half_length = 0.605  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7a")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrance window part 7 a"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_bath_entrance_window_part_7b():
		z_center = -68.2
		r_in = 11.0  # radius in mm
		r_out = 11.5  # radius in mm
		half_length = 30.1  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7b")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 b"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_bath_entrance_window_part_7c():
		z_center = -98.4
		r_in = 11.5001  # radius in mm
		r_out = 14.4  # radius in mm
		half_length = 3.17  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7c")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 c"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_bath_entrance_window_part_7d():
		z_center = -102.23
		r_in = 11.0  # radius in mm
		r_out = 14.96  # radius in mm
		half_length = 0.66  # half length along beam axis
		gvolume = GVolume("InsertBathEntranceWindow_7d")
		gvolume.mother = "PolTarg"
		gvolume.description = "Insert Bath Entrence window part 7 d"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume
	
	def build_shim_coil_carrier():
		z_center = -19.3
		r_in = 28.8  # radius in mm
		r_out = 29.3  # radius in mm
		half_length = 80.95  # half length along beam axis	
		gvolume = GVolume("ShimCoilCarrier")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim coil Carrier"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_shim_up_upstream_coil():
		z_center = 43.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimUpUpS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim Up Upstream Coil"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		return gvolume

	def build_shim_upstream_coil():
		z_center = 8.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimUpS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim coil upstream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		return gvolume

	def build_shim_downstream_coil():
		z_center = -8.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimDownS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim coil downstream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		return gvolume

	def build_shim_down_downstream_coil():
		z_center = -43.5
		r_in = 29.3  # radius in mm
		r_out = 30.0  # radius in mm
		half_length = 6.0  # half length along beam axis
		gvolume = GVolume("ShimDownDownS")
		gvolume.mother = "PolTarg"
		gvolume.description = "Shim coil Down downstream"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "a00000"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		return gvolume
	
	def build_heat_shield_tube():
		z_center = -34.3
		r_in = 40.3  # radius in mm
		r_out = 41.3  # radius in mm
		half_length = 83.85  # half length along beam axis
		gvolume = GVolume("HeatShieldTube")
		gvolume.mother = "PolTarg"
		gvolume.description = "PolTarg Heat Shield Tube"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_heat_shield_halfsphere():
		z_center = 49.55
		r_in = 40.3  # radius in mm
		r_out = 41.3  # radius in mm
		gvolume = GVolume("HeatShieldSphere")
		gvolume.mother = "PolTarg"
		gvolume.description = "PolTarg Heat Shield Exit window Shere"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		gvolume.makeG4Sphere(r_in, r_out, 0, 360, 0, 90)
		gvolume.material = "G4_Al"
		return gvolume

	for builder in [
		build_vacuum_container,
		build_lhe_between_target_cells,
		build_upstream_nh3_target_cell,
		build_upstream_nh3_target_cup,
		build_upstream_nh3_target_cup_downstream_ring,
		build_upstream_nh3_target_cup_upstream_ring,
		build_upstream_nh3_target_cup_window_frame,
		build_upstream_nh3_target_cup_upstream_window,
		build_upstream_nh3_target_cup_downstream_window,
		build_downstream_nd3_target_cell,
		build_downstream_nd3_target_cup,
		build_downstream_nd3_target_cup_downstream_ring,
		build_downstream_nd3_target_cup_upstream_ring,
		build_downstream_nd3_target_cup_window_frame,
		build_downstream_nd3_target_cup_upstream_window,
		build_downstream_nd3_target_cup_downstream_window,
		build_bath_entrance_window_part_7a,
		build_bath_entrance_window_part_7b,
		build_bath_entrance_window_part_7c,
		build_bath_entrance_window_part_7d,
		build_shim_coil_carrier,
		build_shim_up_upstream_coil,
		build_shim_upstream_coil,
		build_shim_downstream_coil,
		build_shim_down_downstream_coil,
		build_heat_shield_tube,
		build_heat_shield_halfsphere,
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_bonus(configuration):

	def build_bonus_root_volume():
		r_in = 0.0 # radius in mm
		r_out = 4  # radius in mm
		half_length = 225.0  # half length along beam axis
		gvolume = GVolume("bonusTarget")
		gvolume.mother = "root"
		gvolume.description = "BONuS12 RTPC gaseous D2 Target"
		gvolume.color =  "eeeegg"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_He"
		gvolume.visible = 0
		return gvolume
	
	def build_bonus_target_gas_volume():
		r_in = 0.0
		r_out = 3.0
		half_length = 223.0  # half length
		gvolume = GVolume("gasDeuteriumTarget")
		gvolume.mother = "bonusTarget"
		gvolume.description = "7 atm deuterium target gas"
		gvolume.color =  "a54382"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "bonusTargetGas"
		return gvolume
	
	def build_bonus_target_wall():
		r_in = 3.01
		r_out = 3.056
		half_length = 223.0  # half length
		gvolume = GVolume("bonusTargetWall")
		gvolume.mother = "bonusTarget"
		gvolume.description = "Bonus Target wall"
		gvolume.color =  "330099"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_KAPTON"
		return gvolume

	def build_bonus_target_downstream_aluminum_end_cap_ring():
		r_in = 3.0561
		r_out = 3.1561
		half_length = 2.0  # half length
		z_center = 221  # z position
		gvolume = GVolume("bonusTargetEndCapRing")
		gvolume.mother = "bonusTarget"
		gvolume.description = "Bonus Target Al end cap ring"
		gvolume.color =  "000000"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_bonus_target_downstream_end_cap_ring():
		r_in = 0.0
		r_out = 3.1561
		half_length = 0.05  # half length
		z_center = 223.06  # z position
		gvolume = GVolume("bonusTargetEndCapPlate")
		gvolume.mother = "bonusTarget"
		gvolume.description = "Bonus Target Al end cap wall"
		gvolume.color =  "000000"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	for builder in [
		build_bonus_root_volume,
		build_bonus_target_gas_volume,
		build_bonus_target_wall,
		build_bonus_target_downstream_aluminum_end_cap_ring,
		build_bonus_target_downstream_end_cap_ring,
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_pb_test(configuration):

	z_shift = 40.85
	cell_half_length = 293.26 / 2

	def build_helium_bag():
		# mother is a helium bag 293.26 mm long. Its center is 40.85 mm
		r_in = 0.0
		r_out = 10.0
		z_center = cell_half_length - z_shift
		gvolume = GVolume("targetCell")
		gvolume.mother = "root"
		gvolume.description ="Helium cell"
		gvolume.color =  "5511111"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, cell_half_length)
		gvolume.material = "G4_He"
		return gvolume

	def build_pb_125_microns():
		# PB 125 microns
		r_in = 0.0
		r_out = 5.0
		z_center = z_shift - cell_half_length
		half_length = 0.0625 # (0.125 mm thick)
		gvolume = GVolume("testPbTarget")
		gvolume.mother = "targetCell"
		gvolume.description ="Pb target"
		gvolume.color =  "004488"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Pb"
		return gvolume

	def build_upstream_foil_al():
		# Upstream Foil 50 microns Aluminum at 24.8 cm
		z_center = 0.1 - cell_half_length   # upstream end
		r_in = 0.0
		r_out = 5.0 
		half_length = 0.015 # (0.030 mm thick)
		gvolume = GVolume("AlTargetFoilUpstream")
		gvolume.mother = "targetCell"
		gvolume.description ="Aluminum Upstream Foil"
		gvolume.color =  "aaaaaa"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_downstream_foil_al():
		# Downstream Foil 50 microns Aluminum at 24.8 cm
		z_center = cell_half_length - 0.1   # Downstream end
		r_in = 0.0
		r_out = 5.0
		half_length = 0.015 # (0.030 mm thick)
		gvolume = GVolume("AlTargetFoilDownstream")
		gvolume.mother = "targetCell"
		gvolume.description ="Aluminum Downstream Foil"
		gvolume.color =  "aaaaaa"
		gvolume.material = "G4_Al"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		return gvolume

	def build_flux_detector():
		# flux detector downstream of the scattering chamber
		z_center = 300.0   
		r_out = 45.0
		r_in = 0.0
		half_length = 0.015 # (0.030 mm thick)
		gvolume = GVolume("testFlux")
		gvolume.mother = "root"
		gvolume.description = "Flux detector"
		gvolume.color = "009900"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_AIR"
		gvolume.digitization = 'flux'
		gvolume.setIdentifier('id',1)
		return gvolume

	for builder in [
		build_helium_bag,
		build_pb_125_microns,
		build_upstream_foil_al,
		build_downstream_foil_al,
		build_flux_detector,
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_nd3(configuration):

	variation = configuration.variation

	def build_vacuum_container():
		r_in = 0.0
		r_out= 44.0
		half_length = 50.0  # half length
		gvolume = GVolume("scatteringChamberVacuum")
		gvolume.description = f'clas12 scattering chamber vacuum rohacell container for {variation} target'
		gvolume.color = "aaaaaa4"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "G4_Galactic"
		return gvolume

	def build_rohacell():
		r_in = 0.0
		r_out = 43.0
		half_length = 48.0  # half lSength
		gvolume = GVolume("scatteringChamber")
		gvolume.mother = "scatteringChamberVacuum"
		gvolume.description = f'clas12 rohacell scattering chamber for {variation} target'
		gvolume.color = "ee3344"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "rohacell"
		return gvolume

	def build_vacuum_container_for_plastic_cell():
		r_in = 0.0
		r_out = 40.0
		half_length = 45.0  # half length
		gvolume = GVolume("plasticCellVacuum")
		gvolume.mother = "scatteringChamber"
		gvolume.description = f'clas12 rohacell vacuum aluminum container chamber for {variation} target'
		gvolume.color = "aaaaaa4"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "G4_Galactic"
		return gvolume

	def build_helium_cylinder():
		r_in = 0.0
		r_out = 12.62
		half_length = 25.10  # half length
		gvolume = GVolume("HeliumCell")
		gvolume.mother = "plasticCellVacuum"
		gvolume.description = f'Helium volume for {variation} target'
		gvolume.color = "aaaaaa3"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "G4_He"
		return gvolume

	def build_plastic_cylinder_cell():
		r_in = 0.0
		r_out = 12.60
		half_length = 20.10  # half length
		gvolume = GVolume("plasticCell")
		gvolume.mother = "HeliumCell"
		gvolume.description = f'clas12 plastic cell for {variation} target'
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "G4_TEFLON" #using teflon which is similar to the actual cell
		return gvolume

	def build_actual_target():
		r_in = 0.0
		r_out = 12.50 # target has a 25mm diameter
		half_length = 20.00  # half length (target is 4cm long)
		gvolume = GVolume('ND3')
		gvolume.mother = "plasticCell"
		gvolume.description = f'clas12 {variation} target'
		gvolume.color = "ee8811"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material  = "solidND3"
		return gvolume

	for builder in [
		build_vacuum_container,
		build_rohacell,
		build_vacuum_container_for_plastic_cell,
		build_helium_cylinder,
		build_plastic_cylinder_cell,
		build_actual_target,
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_c12(configuration):
	def build_vacuum_container():
		n_planes = 4
		phi_start = 0
		phi_total = 360 
		z_plane 	= [-145.0,  235.0, 260.0, 370.0]
		outer_radius = [50.2,   50.2,  21.0,  21.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'C12 Target Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = 'G4_Galactic'	
		gvolume.color = '22ff22'
		gvolume.style = 0
		return gvolume

	def build_upstream_foil():
		return _build_nuclear_target_foil(
			material="G4_C",
			name_prefix="1st",
			descr_prefix="First C12",
			z_center=-25.86,
			half_length=0.86,
			color="aa0011",
		)

	def build_second_foil():
		return _build_nuclear_target_foil(
			material="G4_C",
			name_prefix="2nd",
			descr_prefix="Second C12",
			z_center=24.14,
			half_length=0.86,
			color="aa0000",
		)

	def build_downstream_foil():
		return _build_nuclear_target_foil(
			material="G4_C",
			name_prefix="3rd",
			descr_prefix="Third C12",
			z_center=74.14,
			half_length=0.86,
			color="aa0000",
		)

	for builder in [
		build_vacuum_container,
		build_upstream_foil,
		build_second_foil,
		build_downstream_foil
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_al27(configuration):

	def build_vacuum_target():	
		#Vacuum Target Container
		n_planes = 4
		phi_start = 0
		phi_total = 360 

		outer_radius = [50.2, 50.2, 21.0, 21.0]
		z_plane = [-115.0, 265.0, 290.0, 373.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.color =  "22ff22"
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		return gvolume

	def build_upstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Al",
			name_prefix="1st",
			descr_prefix="First 27Al",
			z_center=-25.29,
			half_length=0.29,
			color="aa0011",
		)

	def build_second_foil():
		return _build_nuclear_target_foil(
			material="G4_Al",
			name_prefix="2nd",
			descr_prefix="Second 27Al",
			z_center=24.71,
			half_length=0.29,
			color="aa0000",
		)

	def build_downstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Al",
			name_prefix="3rd",
			descr_prefix="Third 27Al",
			z_center=74.71,
			half_length=0.29,
			color="aa0000",
		)

	for builder in [
		build_vacuum_target,
		build_upstream_foil,
		build_second_foil,
		build_downstream_foil
	]:
		volume = builder()
		volume.publish(configuration)


def build_geometry_cu63(configuration):

	def build_vacuum_target():	
		#Vacuum Target Container
		n_planes = 4
		phi_start = 0
		phi_total = 360 

		outer_radius = [50.2, 50.2, 21.0, 21.0]
		z_plane = [-115.0,  265.0, 290.0, 373.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.color =  "22ff22"
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		return gvolume

	def build_upstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Cu",
			name_prefix="1st",
			descr_prefix="First 63Cu",
			z_center=-25.2,
			half_length=0.2,
			color="aa0011",
		)

	def build_second_foil():
		return _build_nuclear_target_foil(
			material="G4_Cu",
			name_prefix="2nd",
			descr_prefix="Second 63Cu",
			z_center=24.8,
			half_length=0.2,
			color="aa0000",
		)

	def build_downstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Cu",
			name_prefix="3rd",
			descr_prefix="Third 63Cu",
			z_center=74.8,
			half_length=0.2,
			color="aa0000",
		)

	for builder in [
		build_vacuum_target,
		build_upstream_foil,
		build_second_foil,
		build_downstream_foil
	]:
		volume = builder()
		volume.publish(configuration)

		
def build_geometry_sn118(configuration):

	def build_vacuum_target():	
		#Vacuum Target Container
		n_planes = 4
		phi_start = 0
		phi_total = 360 

		outer_radius = [50.2, 50.2, 21.0, 21.0]
		z_plane = [-115.0,  265.0, 290.0, 373.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.color =  "22ff22"
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		return gvolume

	def build_upstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Sn",
			name_prefix="1st",
			descr_prefix="First 118Sn",
			z_center=-25.15,
			half_length=0.15,
			color="aa0011",
		)

	def build_second_foil():
		return _build_nuclear_target_foil(
			material="G4_Sn",
			name_prefix="2nd",
			descr_prefix="Second 118Sn",
			z_center=24.85,
			half_length=0.2,
			color="aa0000",
		)

	def build_downstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Sn",
			name_prefix="3rd",
			descr_prefix="Third 118Sn",
			z_center=74.85,
			half_length=0.2,
			color="aa0000",
		)

	for builder in [
		build_vacuum_target,
		build_upstream_foil,
		build_second_foil,
		build_downstream_foil
	]:
		volume = builder()
		volume.publish(configuration)
		

def build_geometry_pb208(configuration):

	def build_vacuum_target():	
		#Vacuum Target Container
		n_planes = 4
		phi_start = 0
		phi_total = 360 

		outer_radius = [50.2, 50.2, 21.0, 21.0]
		z_plane = [-115.0,  265.0, 290.0, 373.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('target')
		gvolume.description = 'Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.color =  "22ff22"
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		return gvolume

	def build_upstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Pb",
			name_prefix="1st",
			descr_prefix="First 208Pb",
			z_center=-25.07,
			half_length=0.07,
			color="aa0011",
		)

	def build_second_foil():
		return _build_nuclear_target_foil(
			material="G4_Pb",
			name_prefix="2nd",
			descr_prefix="Second 208Pb",
			z_center=24.93,
			half_length=0.07,
			color="aa0000",
		)

	def build_downstream_foil():
		return _build_nuclear_target_foil(
			material="G4_Pb",
			name_prefix="3rd",
			descr_prefix="Third 208Pb",
			z_center=74.93,
			half_length=0.07,
			color="aa0000",
		)

	for builder in [
		build_vacuum_target,
		build_upstream_foil,
		build_second_foil,
		build_downstream_foil
	]:
		volume = builder()
		volume.publish(configuration)		


def build_geometry_hdice(configuration):
	def build_target_container():	
		gvolume = GVolume("hdIce_mother")
		gvolume.mother = "root"
		gvolume.description = "Target Container"
		gvolume.color =  "22ff22"
		gvolume.makeG4Box(160.0, 160.0, 800.0)
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		gvolume.mfield = "hdicefield"
		return gvolume

	for builder in [
		build_target_container
	]:
		volume = builder()
		volume.publish(configuration)

def build_geometry_longitudinal(configuration):

	def build_vacuum_target():	
		#Vacuum Target Container
		n_planes = 4
		phi_start = 0
		phi_total = 360 

		outer_radius = [50.2, 50.2, 21.0, 21.0]
		z_plane = [-115.0,  265.0, 290.0, 300.0]
		inner_radius = [0.0]*len(outer_radius)

		gvolume = GVolume('ltarget') 
		gvolume.description = 'Vacuum Container'
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.color =  "22ff22"
		gvolume.material = "G4_Galactic"
		gvolume.style = 0
		return gvolume	

	def build_aluminum_entrance_window():
		z_center = -24.2125  # center location of target along beam axis
		r_out = 5.0
		r_in = 0.0
		half_length = 0.0125
		gvolume = GVolume("al_window_entrance")
		gvolume.mother = "ltarget"
		gvolume.description = "5 mm radius aluminum window upstream"
		gvolume.color =  "aaaaff"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_aluminum_exit_window():
		z_center = 173.2825  # center location of target along beam axis
		r_out = 3.175
		r_in = 0.0
		half_length = 0.0125
		gvolume = GVolume("al_window_exit")
		gvolume.mother = "ltarget"
		gvolume.description = "1/8 in radius aluminum window downstream" 
		gvolume.color =  "aaaaff"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume
	
	for builder in [
		build_vacuum_target,
		build_aluminum_entrance_window,
		build_aluminum_exit_window
	]:
		volume = builder()
		volume.publish(configuration)

def build_geometry_transverse(configuration):

	#	half_length: 28.4 mm
	#	ID: 27.0 mm
	#	OD: 29.0
	#	Al foils: 25 um thick

	half_half_length = 14.2 # half half_length
	foil_half_half_length = 0.0125 # half half_length

	def build_target_cell_frame():	
		r_out = 14.5 
		r_in = 0.0	
		gvolume = GVolume("ttargetCellFrame")
		gvolume.mother = "root"
		gvolume.description = "Target Container"
		gvolume.color =  "222222"
		_make_full_tube(gvolume, r_in, r_out, half_half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume
		
	def build_target_cell():
		# cell
		r_out = 13.5
		r_in = 0.0	
		gvolume = GVolume("ttargetCell")
		gvolume.mother = "root"
		gvolume.description = "Target Container"
		gvolume.color =  "994422"
		_make_full_tube(gvolume, r_in, r_out, half_half_length)
		gvolume.material = "NH3target"
		return gvolume

	def build_aluminum_entrance_window():
		# downstream al window
		r_out = 13.5
		r_in = 0.0
		z_center = half_half_length + foil_half_half_length
		gvolume = GVolume("al_window_entrance")
		gvolume.mother = "root"
		gvolume.description = "25 mm thick aluminum window downstream"
		gvolume.color =  "aaaaff"
		_make_full_tube(gvolume, r_in, r_out, foil_half_half_length)
		gvolume.setPosition(0,0,z_center)
		gvolume.material = "G4_Al"
		return gvolume

	def build_aluminum_exit_window():
		# upstream al window
		r_out = 13.5
		r_in = 0.0
		z_center = -half_half_length - foil_half_half_length	
		gvolume = GVolume("al_window_exit")
		gvolume.mother = "root"
		gvolume.description = "25 mm thick aluminum window upstream"
		gvolume.color =  "aaaaff"
		_make_full_tube(gvolume, r_in, r_out, foil_half_half_length)
		gvolume.setPosition(0,0,z_center)
		gvolume.material = "G4_Al"
		return gvolume

	for builder in [
		build_target_cell,
		build_aluminum_entrance_window,
		build_aluminum_exit_window
	]:
		volume = builder()
		volume.publish(configuration)

def build_geometry_apollo(configuration):

	variation = configuration.variation
	material_varmap = {
		"apollo_nh3": "NH3target",
		"apollo_nd3": "ND3target"
	}

	name_varmap = {
		"apollo_nh3": "NH3",
		"apollo_nd3": "ND3"
	}

	volume_length = 77.0
	target_length = 50.0 #length of the NH3 target
	target_radius = 10.0 #radius of the NH3 target
	target_center = 0.0  #center of the NH3 target
	target_window_thickness = 0.02
	vacuum_radius = 51.0
	beam_window_thickness = 0.13
	bath_half_length = (target_length+target_window_thickness)/2
	bath_wall_thickness = 0.25
	bath_window_thickness = 0.13
	bath_wall_z0 = target_length/2+target_window_thickness+4+bath_window_thickness    
	bath_dx = 25.0/2
	bath_dy = 45.0/2
	bath_dz = (bath_wall_z0+volume_length)/2
	bath_z0 = (bath_wall_z0-volume_length)/2
	shim_coils_mandrel_r_in = 29.0 
	shim_coils_mandrel_r_out = 29.25
	shim_coils_length = 12.0
	shim_coils_thickness = 0.7
	shim_coils_window = 0.02
	pumping_volume_r_in = 35.5
	pumping_volume_r_out = 36.0
	pumping_volume_window = 0.13
	heat_shield_r_in = 40.75
	heat_shield_r_out = 41.25
	heat_shield_window = 0.02
	vacuum_can_r_in = vacuum_radius - 1.0
	vacuum_can_r_out = vacuum_radius
	vacuum_can_window = 0.13
	spheres_center = bath_wall_z0 + 3.0

	def build_mother_volume():
		# mother volume
		r_out = vacuum_radius
		z_length = spheres_center + vacuum_radius
		n_planes = 2
		phi_start = 0
		phi_total = 360 
		z_plane = [-volume_length, z_length]
		outer_radius = [r_out, r_out]
		inner_radius = [0.0, 0.0]
		gvolume = GVolume("PolTarg")
		gvolume.description = "PolTarg Region"
		gvolume.color = "123456"
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = "G4_AIR"
		gvolume.visible = 0 
		return gvolume

	def build_vacuum_volume():
		# vacuum volume
		r_out = vacuum_radius
		n_planes = 2
		phi_start = 0
		phi_total = 360 
		z_plane = [-volume_length, spheres_center]
		outer_radius = [r_out, r_out]
		inner_radius = [0.0, 0.0]
		gvolume = GVolume("VacuumVolume")
		gvolume.mother = "PolTarg"
		gvolume.description = "Vacuum cylindrical volume"
		gvolume.color = "ffffff"
		gvolume.setPosition(0,0,target_center)
		gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
		gvolume.material = "G4_Galactic"
		gvolume.visible = 0
		return gvolume
		
	def build_vacuum_sphere():
		# vacuum sphere
		r_out = vacuum_radius
		r_in = 0.0
		phi_start = 0
		dphi = 360
		theta_start = 0
		dtheta = 90
		gvolume = GVolume("VacuumSphere")
		gvolume.mother = "PolTarg"
		gvolume.description = "Vacuum half sphere volume"
		gvolume.setPosition(0,0,spheres_center)
		gvolume.color = "ffffff"
		gvolume.makeG4Sphere(r_in, r_out, phi_start, dphi, theta_start, dtheta)
		gvolume.material = "G4_Galactic"
		gvolume.visible = 0
		return gvolume

	def build_lhe_bath_walls():
		#LHe bath walls
		dx = bath_dx + bath_wall_thickness
		dy = bath_dy + bath_wall_thickness
		dz = bath_dz
		gvolume = GVolume("HeliumBathWalls")
		gvolume.mother = "VacuumVolume"
		gvolume.description = "LHe bath walls"
		gvolume.color = "aaaaaa"
		gvolume.makeG4Box(dx, dy, dz)
		gvolume.setPosition(0,0,bath_z0)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_lhe_bath():	
		#LHe bath
		gvolume = GVolume("HeliumBath")
		gvolume.mother = "HeliumBathWalls"
		gvolume.description = "LHe bath"
		gvolume.color = "0099ff"
		gvolume.makeG4Box(bath_dx, bath_dy, bath_dz)
		gvolume.setPosition(0,0,0)
		gvolume.material = "lHeCoolant"
		return gvolume
		
	def build_lhe_bath_window():
		#LHe bath window
		z_center = bath_dz - bath_window_thickness/2
		dz = bath_window_thickness/2
		gvolume = GVolume("HeliumBathWindow")
		gvolume.mother = "HeliumBath"
		gvolume.description = "LHe bath window"
		gvolume.color = "aaaaaa"
		gvolume.makeG4Box(bath_dx, bath_dy, dz)
		gvolume.setPosition(0,0,z_center)
		gvolume.material = "G4_Al"
		return gvolume
		
	def build_target():
		z_center = -bath_z0    # center location of target along beam axis
		r_out = target_radius    # radius in mm
		r_in = 0.0
		half_length = target_length/2  # half length along beam axis
		gvolume = GVolume(f'{name_varmap[variation]}Targ')
		gvolume.mother = "HeliumBath"
		gvolume.description = f'{name_varmap[variation]} target cell'
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.color = "f000f0"
		gvolume.material = material_varmap[variation]
		return gvolume

	def build_target_cup():
		# Target Cup
		r_in = target_radius + 0.001  # radius in mm
		r_out = target_radius + 0.03   # radius in mm
		half_length = target_length/2   # half length along beam axis
		z_center = -bath_z0    # center location of target along beam axis
		gvolume = GVolume("NH3Cup")
		gvolume.mother = "HeliumBath"
		gvolume.description = "NH3 Target cup"
		gvolume.color = "ffffff"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "AmmoniaCellWalls"
		return gvolume

	def build_target_cup_upstream_window():
		# Target Cup Up Stream Window
		z_center = -bath_z0-target_length/2-target_window_thickness/2
		r_in = 0.0 # radius in mm
		r_out = target_radius # radius in mm
		half_length = target_window_thickness/2 # half length along beam axis
		gvolume = GVolume("NH3USWindow")
		gvolume.mother = "HeliumBath"
		gvolume.description = "NH3 Target cup Upstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_target_cup_downstream_window():
		# Target Cup Downstream Stream Window
		z_center = -bath_z0+target_length/2+target_window_thickness/2
		r_in = 0.0 # radius in mm
		r_out = target_radius # radius in mm
		half_length = target_window_thickness/2  # half length along beam axis
		gvolume = GVolume("NH3DSWindow")
		gvolume.mother = "HeliumBath"
		gvolume.description = "NH3 Target cup Downstream Window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_beam_pipe():
		# Beam pipe
		r_in  = 0.0
		r_out = target_radius+1
		z1 = -bath_dz
		z2 = -bath_z0-target_length/2-target_window_thickness
		half_length = (z2-z1)/2
		z_center    = (z2+z1)/2
		gvolume = GVolume("BeamEntranceVacuum")
		gvolume.mother = "HeliumBath"
		gvolume.description = "Beam Entrance Vacuum"
		gvolume.color = "ffffff"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Galactic"
		return gvolume

	def build_beam_entrance_pipe():
		r_in  = target_radius+1
		r_out = target_radius+2
		z1 = -bath_dz
		z2 = -bath_z0-target_length/2-target_window_thickness
		half_length = (z2-z1)/2
		z_center     = (z2+z1)/2
		gvolume = GVolume("BeamEntrancePipe")
		gvolume.mother = "HeliumBath"
		gvolume.description = "Beam Entrance Pipe"
		gvolume.color = "595959"
		gvolume.setPosition(0,0,z_center)
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_beam_entrance_window():
		#  Beam Entrance Window
		z1 = -bath_dz
		z2 = -bath_z0-target_length/2-target_window_thickness
		z_half_length = (z2-z1)/2
		z_center = z_half_length-beam_window_thickness/2
		r_in = 0.0      # radius in mm
		r_out = target_radius+1    # radius in mm
		half_length = beam_window_thickness/2  # half length along beam axis
		gvolume = GVolume("BeamEntrance")
		gvolume.mother = "BeamEntranceVacuum"
		gvolume.description = "Beam entrance window"
		gvolume.setPosition(0,0,z_center)
		gvolume.color = "aaaaaa"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "G4_Al"
		return gvolume

	def build_shim_up_upstream_coil():
		return _create_shimcoil(bath_half_length - shim_coils_length / 2, 1)

	def build_shim_upstream_coil():
		return _create_shimcoil(-4.5, 2)

	def build_shim_downstream_coil():
		return _create_shimcoil(-22.5, 3)

	def build_shim_coil_carrier():
		yield from _create_spheretube_volumes(
			shim_coils_mandrel_r_in,
			shim_coils_mandrel_r_out,
			shim_coils_window,
			"ShimCoil",
			"G4_Al",
			"aaaaaa"
		)

	def build_pumping_volume():
		yield from _create_spheretube_volumes(
			pumping_volume_r_in,
			pumping_volume_r_out,
			pumping_volume_window,
			"PumpingVolume",
			"G4_Al",
			"000080"
		)

	def build_heat_shield_volume():
		yield from _create_spheretube_volumes(
			heat_shield_r_in,
			heat_shield_r_out,
			heat_shield_window,
			"HeathShield",
			"G4_Al",
			"404040",
		)

	def build_vacuum_can():
		yield from _create_spheretube_volumes(
			vacuum_can_r_in,
			vacuum_can_r_out,
			vacuum_can_window,
			"VacuumCan",
			"G4_Al",
			"0d0d0d"
		)

	def _create_spheretube_volumes(
		r_in,
		r_out,
		r_win,
		name,
		mat,
		color,
	):
		tube = GVolume(f"{name}Tube")
		tube.mother = "VacuumVolume"
		tube.description = f"{name} tube"
		tube.setPosition(0,0,target_center)
		tube.makeG4Polycone(
			0,
			360,
			2,
			[-volume_length, spheres_center],
			[r_in, r_in],
			[r_out, r_out],
		)

		theta = int(math.atan((target_radius + 1) / r_in) * 180 / math.pi) + 1
		dtheta = 90 - theta
		sphere = GVolume(f"{name}Sphere")
		sphere.mother = "VacuumSphere"
		sphere.description = f"{name} sphere"
		sphere.setPosition(0,0,0)
		sphere.makeG4Sphere(
			r_in,
			r_out,
			0,
			360,
			theta,
			dtheta,
		)
		r_out_window = r_in + r_win
		window = GVolume(f"{name}Window")
		window.description = f"{name} window"
		window.mother = "VacuumSphere"
		window.setPosition(0,0,0)
		window.makeG4Sphere(
			r_in,
			r_out_window,
			0,
			360,
			0,
			theta
		)

		for volume in [
			tube,
			sphere,
			window
		]:
			volume.material = mat
			volume.color = color
			yield volume

	def _create_shimcoil(
		z_center,
		num,
	):
		r_in = shim_coils_mandrel_r_out
		r_out = shim_coils_mandrel_r_out + shim_coils_thickness
	
		half_length = shim_coils_length / 2
		gvolume = GVolume(f"ShimCoil{num}")
		gvolume.mother = "VacuumVolume"
		gvolume.description = f"Shim Coil {num}"
		gvolume.setPosition(0, 0, z_center)
		gvolume.color = "a00000"
		_make_full_tube(gvolume, r_in, r_out, half_length)
		gvolume.material = "ShimCoil"
		return gvolume

	volumes_to_publish = []
	for builder in [
		build_mother_volume,
		build_vacuum_volume,
		build_vacuum_sphere,
		build_lhe_bath_walls,
		build_lhe_bath,
		build_lhe_bath_window,
		build_target,
		build_target_cup,
		build_target_cup_upstream_window,
		build_target_cup_downstream_window,
		build_beam_pipe,
		build_beam_entrance_pipe,
		build_beam_entrance_window,
		build_shim_up_upstream_coil,
		build_shim_upstream_coil,
		build_shim_downstream_coil,
	]:
		volumes_to_publish.append(builder())
	for multi_volume_builder in [
		# these builder functions return multiple volumes
		build_shim_coil_carrier,
		build_pumping_volume,
		build_heat_shield_volume,
		build_vacuum_can,
	]:
		volumes_to_publish.extend(multi_volume_builder())

	for volume in volumes_to_publish:
		volume.publish(configuration)


	
VARIATION_MAP = {
	"lh2": build_geometry_lhydrogen,
	"ld2": build_geometry_lhydrogen,
	"pol_targ": build_geometry_pol_targ,
	"bonus": build_geometry_bonus,
	"pb_test": build_geometry_pb_test,
	"nd3": build_geometry_nd3,

	"c12": build_geometry_c12,
	"sn118" : build_geometry_sn118,
	"pb208" : build_geometry_pb208,
	"cu63" : build_geometry_cu63,
	"al27" : build_geometry_al27,

	"hdice" : build_geometry_hdice,
	"longitudinal" : build_geometry_longitudinal,
	"transverse" : build_geometry_transverse,
	"apollo_nh3": build_geometry_apollo,
	"apollo_nd3": build_geometry_apollo,
}
