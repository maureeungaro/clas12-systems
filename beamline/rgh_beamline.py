from gemc_api_geometry import *
import math

def build_rgh_beamline(configuration):

	# inside hdIce_mother
	pipeLength    = 72.5
	zpos          = 727.5
	firstVacuumIR = 33.325
	firstVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe1_1')
	gvolume.mother      = 'hdIce_mother'
	gvolume.description = 'first straightVacuumPipe 2.75 inch OD 0.065 thick '
	gvolume.makeG4Tubs(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe1_1')
	gvolume.mother      = 'vacuumPipe1_1'
	gvolume.description = 'first straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, firstVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# in "root" the second part of the pipe is straight until torus
	pipeLength    = 728.4
	zpos = 1528.4
	secondVacuumIR = 33.325
	secondVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe1_2')
	gvolume.description = 'second straightVacuumPipe steel'
	gvolume.makeG4Tubs(0, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe1_2')
	gvolume.mother      = 'vacuumPipe1_2'
	gvolume.description = 'second straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, secondVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)

	# vacuumPipe2
	pipeLength = 132.235
	zpos = 2621.735
	secondVacuumIR = 33.275
	secondVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe2')
	gvolume.description = 'vacuumPipe2 straightVacuumPipe steel'
	gvolume.makeG4Tubs(0, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside
	gvolume = GVolume('vacuumInPipe2')
	gvolume.mother      = 'vacuumPipe2'
	gvolume.description = 'vacuumPipe2 straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, secondVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# vacuumPipe3
	pipeLength = 38.15
	zpos = 2451.15
	secondVacuumIR = 33.375
	secondVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe3')
	gvolume.description = 'vacuumPipe3 straightVacuumPipe steel'
	gvolume.makeG4Tubs(secondVacuumIR, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside,  this is inside ROOT
	secondVacuumIR = 28.52
	gvolume = GVolume('vacuumInPipe3')
	gvolume.description = 'vacuumPipe3 straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, secondVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# sst pipe
	z_plane_vbeam  =  [ 2754.17,        5016,           5064,   5732 ]
	vradius_vbeam  =  [       0,           0,              0,      0 ]
	iradius_vbeam  =  [  33.274,      33.274,         60.325, 60.325 ]
	oradius_vbeam  =  [  34.925,      34.925,           63.5, 63.5   ]
	gvolume = GVolume('vacuumPipe')
	gvolume.mother      = 'fc'
	gvolume.description = 'vacuumPipe steel'
	gvolume.makeG4Polycone('0', '360', z_plane_vbeam, vradius_vbeam, oradius_vbeam)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside
	gvolume = GVolume('vacuumInPipe')
	gvolume.mother      = 'vacuumPipe'
	gvolume.description = 'vacuumPipe vacuum'
	gvolume.makeG4Polycone('0', '360', z_plane_vbeam, vradius_vbeam, iradius_vbeam)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# pipe to alcove
	pipeLength = 1829.4
	zpos = 7570.4
	thirdPipeIR = 64
	thirdPipeOR = 68

	gvolume = GVolume('vacuumPipeToAlcove')
	gvolume.mother      = 'fc'
	gvolume.description = 'vacuumPipeToAlcove steel'
	gvolume.makeG4Tubs(0, thirdPipeOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipeToAlcove')
	gvolume.mother      = 'vacuumPipeToAlcove'
	gvolume.description = 'vacuumPipeToAlcove vacuum inside'
	gvolume.makeG4Tubs(0, thirdPipeIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)

	# lead inside apex
	# apex cad model not filled with lead.
	apexIR = 140
	apexOR = 190
	apexLength = 1000
	zpos = 6372
	
	gvolume = GVolume('leadInsideApex')
	gvolume.mother      = 'fc'
	gvolume.description = 'lead inside apex'
	gvolume.makeG4Tubs(apexIR, apexOR, apexLength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '4499ff'
	gvolume.publish(configuration)


	# airpipes to account for change in volume size from target to "root" within a magnetic field
	iradius_airpipe  =  [       0,      0,      0,    0 ]
	oradius_airpipe  =  [    30.0,   30.0,  25.46, 41.2 ]
	z_plane_airpipe  =  [  280.71, 384.98, 384.98,  570 ]


	gvolume = GVolume('Airpipe')
	gvolume.mother      = 'hdIce_mother'
	gvolume.description = 'airgap between target and shield to limit e- steps'
	gvolume.makeG4Polycone('0', '360', z_plane_airpipe, iradius_airpipe, oradius_airpipe)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)


	# Shield is made of the tips cones

	# Tungsten Tip
	zpos = 643.21
	gvolume = GVolume('Tungstentip')
	gvolume.mother      = 'hdIce_mother'
	gvolume.description = 'AngelaBrenna Tungsten Tip'
	gvolume.makeG4Cons(39, 41.2, 39.0, 54.02, 73.21, 0, 360)
	gvolume.material    = 'G4_W'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'f69552'
	gvolume.publish(configuration)


	zpos = 758.21
	gvolume = GVolume('Cone1_1')
	gvolume.mother      = 'hdIce_mother'
	gvolume.description = 'AngelaBrenna Cone1_1'
	gvolume.makeG4Cons(38.1, 54.02, 38.1, 61.3313, 41.79, 0, 360)
	gvolume.material    = 'G4_W'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'dd8648'
	gvolume.publish(configuration)

	zpos = 1013.25
	gvolume = GVolume('Cone1_2')
	gvolume.description = 'AngelaBrenna Cone1_2'
	gvolume.makeG4Cons(38.1, 61.3313, 38.1, 98.64, 213.25, 0, 360)
	gvolume.material    = 'G4_W'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'dd8648'
	gvolume.publish(configuration)

	zpos = 1290.05
	gvolume = GVolume('Cone2')
	gvolume.description = 'AngelaBrenna Cone2'
	gvolume.makeG4Cons(47.62, 98.64, 47.62, 109.76, 63.55, 0, 360)
	gvolume.material    = 'G4_W'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'dd8648'
	gvolume.publish(configuration)


	# Lead Cylinders differ for configurations 'rghFTOut' and 'rghFTOn'

	zpos    = 1797.755
	clength = 444.155

	if configuration.variation == 'rghFTOn':
		zpos    = 1556.8
		clength = 203.2

	gvolume = GVolume('Cylinder')
	gvolume.description = 'AngelaBrenna Moller Shield Pb pipe on beamline, NW80 flange is 2.87 inch inner diameter'
	gvolume.makeG4Cons(47.63, 109.76, 47.63, 109.76, clength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'c57742'
	gvolume.publish(configuration)


	zpos    = 1743.2
	clength = 516.7

	if configuration.variation == 'rghFTOn':
		zpos    = 1493.25
		clength = 266.75

	gvolume = GVolume('SupportTube')
	gvolume.description = 'AngelaBrenna 2nd Moller Shield Cone outside beam pipe '
	gvolume.makeG4Cons(38.1, 47.6, 38.1, 47.6, clength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'ac6839'
	gvolume.publish(configuration)

	zpos    = 2018.765
	clength = 241.135

	if configuration.variation == 'rghFTOut':

		gvolume = GVolume('FTPreShieldCylinder')
		gvolume.description = 'AngelaBrenna Shield before FT on beamline '
		gvolume.makeG4Cons(35.0, 108.5, 35.0, 108.5, clength, 0, 360)
		gvolume.material    = 'G4_Pb'
		gvolume.setPosition(0, 0, zpos)
		gvolume.color       = '945931'
		gvolume.publish(configuration)



	zpos    = 2300.0
	clength = 41.3

	if configuration.variation == 'rghFTOn':
		zpos    = 2305.45
		clength = 35.85

	gvolume = GVolume('FTflangeShieldCylinder')
	gvolume.description = 'AngelaBrenna Shield around beam pipe flange '
	gvolume.makeG4Cons(125.4, 130, 125.4, 130.0, clength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '999966'
	gvolume.publish(configuration)


	zpos    = 2550.0
	gvolume = GVolume('TorusConnector')
	gvolume.description = 'AngelaBrenna Shield around Shield support before FT on beamline '
	gvolume.makeG4Cons(97, 104, 97, 104.0, 101.3, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '999966'
	gvolume.publish(configuration)
