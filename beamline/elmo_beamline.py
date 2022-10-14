from gemc_api_geometry import *
import math

def build_elmo_beamline(configuration):

	shieldStart      = 787.41  # start of vacuum pipe is 1mm downstream of target vac extension
	pipeFirstStep    = 2413
	torusStart       = 2754.17
	mediumPipeEnd    = 5016    # added by hand by shooting geantino vertically to locate the point
	bigPipeBegins    = 5064    # added by hand by shooting geantino vertically to locate the point
	pipeEnds         = 5732
	alcovePipeStarts = 5741
	alcovePipeEnds   = 9400
	mediumStarts  = pipeFirstStep + 76.5 # added by hand by shooting geantino vertically to locate the point


	# in "root" the first part of the pipe is straight
	# 1.651mm thick
	pipeLength = ( pipeFirstStep - shieldStart) / 2.0 - 0.1
	zpos = shieldStart + pipeLength
	firstVacuumIR = 33.275
	firstVacuumOR = 34.925

	gvolume = GVolume('vacuumPipe1')
	gvolume.description = 'first straightVacuumPipe steel'
	gvolume.make_tube(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
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
	gvolume.setPosition(0, 0, zpos)
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
	connectingIR = firstVacuumIR + 0.1

	gvolume = GVolume('vacuumPipe3')
	gvolume.description = 'third straightVacuumPipe steel'
	gvolume.make_tube(firstVacuumIR, firstVacuumOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)

	# vacuum inside,  this is inside ROOT
	gvolume = GVolume('vacuumInPipe3')
	gvolume.description = 'third straightVacuumPipe vacuum inside'
	gvolume.make_tube(0, firstVacuumIR, pipeLength, 0, 360)
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
	pipeLength  = 1829.4
	zpos        = 7570.4
	thirdPipeIR = 64
	thirdPipeOR = 68

	gvolume = GVolume('vacuumPipeToAlcove')
	gvolume.mother      = 'fc'
	gvolume.description = 'vacuumPipeToAlcove steel'
	gvolume.make_tube(0, thirdPipeOR, pipeLength, 0, 360)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.setPosition(0, 0, zpos)
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
	gvolume.setPosition(0, 0, zpos)
	gvolume.color       = '4499ff'
	gvolume.publish(configuration)


	# shield is a tapered pipe (G4 polycone)
	zplane_tcone  = [ 716.42, 1249.40,  1249.40, 1351.00 ]
	iradius_tcone = [  38.10,    38.10,   47.62,   47.62 ]
	or1_tcone = 53.28
	or2_tcone = 105.78
	orm_tcone = or1_tcone + ( or2_tcone - or1_tcone ) * ( zplane_tcone[1] - zplane_tcone[0] ) / (zplane_tcone[3] - zplane_tcone[0])
	oradius_tcone  = ( or1_tcone, orm_tcone, orm_tcone, or2_tcone )
	gvolume = GVolume('ElmoTungstenCone')
	gvolume.description = 'Tungsten moller shield - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_tcone, iradius_tcone, oradius_tcone)
	gvolume.material    = 'beamline_W'
	gvolume.color       = 'dd8648'
	gvolume.publish(configuration)

	# tip
	zplane_ttip  = [ 570.0, zplane_tcone[0] ]
	iradius_ttip = [ 39.0, iradius_tcone[0] ]
	oradius_ttip = [ 41.2, oradius_tcone[0] ]
	gvolume = GVolume('ElmoTungstenTip')
	gvolume.description = 'Tungsten tip - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_ttip, iradius_ttip, oradius_ttip)
	gvolume.material    = 'beamline_W'
	gvolume.color       = 'dd8648'
	gvolume.publish(configuration)

	# Lead Cylinder 1
	iradius_lc1 = [     47.62,     47.62 ]
	oradius_lc1 = [ or2_tcone, or2_tcone ]
	zplane_pb1 = [ 1357.35, 1802.71 ]
	gvolume = GVolume('ElmoPbCylinder1')
	gvolume.description = 'Lead Cylinder 1 - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_pb1, iradius_lc1, oradius_lc1)
	gvolume.material    = 'G4_Pb'
	gvolume.color       = '999966'
	gvolume.publish(configuration)

	# Lead Cylinder 2
	zplane_pb2 = [ 1809.06, 2240.86 ]
	gvolume = GVolume('ElmoPbCylinder2')
	gvolume.description = 'Lead Cylinder 2 - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_pb2, iradius_lc1, oradius_lc1)
	gvolume.material    = 'G4_Pb'
	gvolume.color       = '999966'
	gvolume.publish(configuration)

	# steel case
	zplane_steel  = [ zplane_pb1[0]-5, zplane_pb2[1]+15  ]
	iradius_steel = [ oradius_tcone[3], oradius_tcone[3] ]
	oradius_steel = [           109.54,           109.54 ]
	gvolume = GVolume('ElmoSteelCase')
	gvolume.description = 'Steel Case - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_steel, iradius_steel, oradius_steel)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.color       = '666666'
	gvolume.publish(configuration)

	# support pipe
	zm_stube = zplane_pb2[1]
	zf_stube = zm_stube + 27.5
	zplane_stube  = [  zplane_tcone[2],         zm_stube,         zm_stube,         zf_stube ]
	iradius_stube = [ iradius_tcone[0], iradius_tcone[0], iradius_tcone[0], iradius_tcone[0] ]
	oradius_stube = [ iradius_tcone[2], iradius_tcone[2], oradius_tcone[3], oradius_tcone[3] ]
	gvolume = GVolume('ElmoSupportPipe')
	gvolume.description = 'Support pipe - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_stube, iradius_stube, oradius_stube)
	gvolume.material    = 'G4_STAINLESS-STEEL'
	gvolume.color       = '669966'
	gvolume.publish(configuration)


	# air pipe
	zplane_apipe  = [ 54, 385,   385,  zplane_ttip[0] ]
	iradius_apipe = [  0,   0,     0,               0 ]
	oradius_apipe = [ 30,  30, 25.46, oradius_ttip[0] ]
	gvolume = GVolume('ElmoAirPipe')
	gvolume.description = 'Air pipe - ELMO configuration'
	gvolume.makeG4Polycone('0', '360', zplane_apipe, iradius_apipe, oradius_apipe)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = 'aaffff'
	gvolume.publish(configuration)



