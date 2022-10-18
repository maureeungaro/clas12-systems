from gemc_api_geometry import *
import math

def build_rgab_beamline(configuration):

	shieldStart      = 963     # start of vacuum pipe is 1mm downstream of target vac extension
	pipeFirstStep    = 2413
	torusStart       = 2754.17
	mediumPipeEnd    = 5016    # added by hand by shooting geantino vertically to locate the point
	bigPipeBegins    = 5064    # added by hand by shooting geantino vertically to locate the point
	pipeEnds         = 5732
	alcovePipeStarts = 5741
	alcovePipeEnds   = 9400
	mediumStarts  = pipeFirstStep + 76.5 # added by hand by shooting geantino vertically to locate the point

	if configuration.variation == 'FTOff':
		shieldStart = 503

	# in "root" the first part of the pipe is straight
	# 1.651mm thick
	pipeLength = ( pipeFirstStep - shieldStart) / 2.0 - 0.1
	zpos = shieldStart + pipeLength
	firstVacuumIR = 26.924
	firstVacuumOR = 28.52

	gvolume = GVolume('vacuumPipe1')
	gvolume.description = 'first straightVacuumPipe steel'
	gvolume.make_tube(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.set_position(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe1')
	gvolume.mother      = 'vacuumPipe1'
	gvolume.description = 'first straightVacuumPipe vacuum inside'
	gvolume.make_tube(0, firstVacuumIR, pipeLength, 0, 360)
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
	gvolume.make_tube(0, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.set_position(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipe2')
	gvolume.mother      = 'vacuumPipe2'
	gvolume.description = 'second straightVacuumPipe vacuum inside'
	gvolume.make_tube(0, secondVacuumIR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '000000'
	gvolume.publish(configuration)

	# added SST piece on top of Al junction
	pipeLength = ( mediumStarts - pipeFirstStep ) / 2.0 - 0.1
	zpos = pipeFirstStep + pipeLength
	connectingIR = secondVacuumIR + 0.1

	gvolume = GVolume('vacuumPipe3')
	gvolume.description = 'third straightVacuumPipe steel'
	gvolume.make_tube(connectingIR, secondVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.set_position(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside,  this is inside ROOT
	gvolume = GVolume('vacuumInPipe3')
	gvolume.description = 'third straightVacuumPipe vacuum inside'
	gvolume.make_tube(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_Galactic'
	gvolume.set_position(0, 0, zpos)
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
	gvolume.make_polycone('0', '360', z_plane_vbeam, vradius_vbeam, oradius_vbeam)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside
	gvolume = GVolume('vacuumInPipe')
	gvolume.mother      = 'vacuumPipe'
	gvolume.description = 'vacuumPipe vacuum'
	gvolume.make_polycone('0', '360', z_plane_vbeam, vradius_vbeam, iradius_vbeam)
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
	gvolume.make_tube(0, thirdPipeOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.set_position(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	gvolume = GVolume('vacuumInPipeToAlcove')
	gvolume.mother      = 'vacuumPipeToAlcove'
	gvolume.description = 'vacuumPipeToAlcove vacuum inside'
	gvolume.make_tube(0, thirdPipeIR, pipeLength, 0, 360)
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
	gvolume.make_tube(apexIR, apexOR, apexLength, 0, 360)
	gvolume.material    = 'G4_Pb'
	gvolume.set_position(0, 0, zpos)
	gvolume.color       = '4499ff'
	gvolume.publish(configuration)


	# airpipes to account for change in volume size from target to "root" within a magnetic field
	#
	#

	gapZpos = 283
	gapLength = 295

	if configuration.variation == 'FTOff':
		gapLength = 92.5

	gapLengthm = gapLength + 1
	ztart = gapZpos

	z_plane_airpipe  =  [   0, 2*gapLength ]
	zradius_airpipe  =  [   0,           0 ]
	oradius_airpipe  =  [  20,          55 ]

	gvolume = GVolume('airPipe')
	gvolume.description = 'airgap between target and shield to limit e- steps'
	gvolume.make_polycone('0', '360', z_plane_airpipe, zradius_airpipe, oradius_airpipe)
	gvolume.set_position(0, 0, ztart)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	innerAirpipeDimension = gapLength - 0.2;
	gvolume = GVolume('airPipe2')
	gvolume.mother      = 'airPipe'
	gvolume.description = 'airgap2 between target and shield to limit e- steps'
	gvolume.make_tube(0, 10, innerAirpipeDimension, 0, 360)
	gvolume.material    = 'G4_AIR'
	gvolume.set_position(0, 0, innerAirpipeDimension)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)
