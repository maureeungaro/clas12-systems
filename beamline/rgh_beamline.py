from gemc_api_geometry import *
import math

def build_rgh_beamline(configuration):

	# inside hdIce_mother
	pipeLength    = 72.5
	zpos          = 727.5
	firstVacuumIR = 33.325
	firstVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe1')
	gvolume.description = 'first straightVacuumPipe steel'
	gvolume.makeG4Tubs(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe1')
	gvolume.mother      = 'vacuumPipe1'
	gvolume.description = 'first straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, firstVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# in "root" the second part of the pipe is straight until torus
	pipeLength = (torusStart - mediumStarts) / 2.0 - 0.1
	zpos = mediumStarts + pipeLength
	secondVacuumIR = 33.275
	secondVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe2')
	gvolume.description = 'second straightVacuumPipe steel'
	gvolume.makeG4Tubs(0, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe2')
	gvolume.mother      = 'vacuumPipe2'
	gvolume.description = 'second straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, secondVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)

	# added SST piece on top of Al junction
	pipeLength = ( mediumStarts - pipeFirstStep ) / 2.0 - 0.1
	zpos = pipeFirstStep + pipeLength
	connectingIR = secondVacuumIR + 0.1

	gvolume = GVolume('vacuumPipe3')
	gvolume.description = 'third straightVacuumPipe steel'
	gvolume.makeG4Tubs(connectingIR, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside,  this is inside ROOT
	gvolume = GVolume('vacuumInPipe3')
	gvolume.description = 'third straightVacuumPipe vacuum inside'
	gvolume.makeG4Tubs(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '000000'
	gvolume.publish(configuration)


	# sst pipe
	z_plane_vbeam  =  [ torusStart, mediumPipeEnd, bigPipeBegins, pipeEnds  ]
	vradius_vbeam  =  [      0,           0,              0        , 0 ]
	iradius_vbeam  =  [ 33.274,      33.274,         60.325        , 60.325 ]
	oradius_vbeam  =  [ 34.925,      34.925,         63.5          , 63.5   ]
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
	pipeLength = (alcovePipeEnds - alcovePipeStarts) / 2.0 - 0.1
	zpos = alcovePipeStarts + pipeLength
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
	apexPos = 5372
	zpos = apexPos + apexLength
	
	gvolume = GVolume('leadInsideApex')
	gvolume.mother      = 'fc'
	gvolume.description = 'lead inside apex'
	gvolume.makeG4Tubs(apexIR, apexOR, apexLength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '4499ff'
	gvolume.publish(configuration)


	gapZpos = 283
	gapLength = 295

	if configuration.variation == 'FTOff':
		gapLength = 92.5


	gapLengthm = gapLength + 1
	ztart = gapZpos


	# airpipes to account for change in volume size from target to "root" within a magnetic field
	#
	#
	z_plane_airpipe  =  [   0, 2*gapLength ]
	zradius_airpipe  =  [   0,           0 ]
	oradius_airpipe  =  [  20,          55 ]

	gvolume = GVolume('airPipe')
	gvolume.description = 'airgap between target and shield to limit e- steps'
	gvolume.makeG4Polycone('0', '360', z_plane_airpipe, zradius_airpipe, oradius_airpipe)
	gvolume.setPosition(0, 0, ztart)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	innerAirpipeDimension = gapLength - 0.2;
	gvolume = GVolume('airPipe2')
	gvolume.mother      = 'airPipe'
	gvolume.description = 'airgap2 between target and shield to limit e- steps'
	gvolume.makeG4Tubs(0, 10, innerAirpipeDimension, 0, 360)
	gvolume.material    = 'G4_AIR'
	gvolume.setPosition(0, 0, innerAirpipeDimension)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)
