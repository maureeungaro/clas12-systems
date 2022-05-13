from gemc_api_geometry import *

def build_geometry_forward_carriage(configuration):

	variation = configuration.variation

	mfield_varmap = {
		"original": "clas12-torus-big",
		"fast_field": "clas12-torus-bigRK",
		"torus_symmetric": "TorusSymmetric",
	}

	microgap = 0.1
	torus_z_start = 2754.17 - microgap # from drawings
	fc_end = 9500
	fc_max_radius = 5000

	n_planes = 6

	# Notice:
	# The FC coordinates are the same as CLAS12 target center
	z_plane = [1206.0, 1556.0, 2406.0, torus_z_start, torus_z_start,fc_end]
	inner_radius = [2575.0, 2000.0,  132.0, 132.0, 0, 0]
	outer_radius = [2575.0, fc_max_radius, fc_max_radius, fc_max_radius, fc_max_radius, fc_max_radius]
	phi_start = 0
	phi_total = 360

	gvolume = GVolume('fc')
	gvolume.mother = "root"
	gvolume.description = 'Forward Carriage (FC) detector envelope to hold the torus magnet and the FC detectors'
	gvolume.makeG4Polycone(phi_start, phi_total, n_planes, z_plane, inner_radius, outer_radius)
	gvolume.material = "G4_AIR"
	gvolume.color = '88aa88'
	gvolume.visible = 0
	gvolume.style = 0
	gvolume.mfield = mfield_varmap[variation]
	gvolume.publish(configuration)

VARIATION_MAP = {
	"original": build_geometry_forward_carriage,
	"fast_field": build_geometry_forward_carriage,
	"torus_symmetric": build_geometry_forward_carriage,
}