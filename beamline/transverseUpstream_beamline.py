from gemc_api_geometry import *
import math

def build_transverseUpstream_beamline(configuration):

	pipeLength    = 500
	zpos          = -858
	firstVacuumOR = 35

	gvolume = GVolume('upstreamTransverseMagnetVacuumPipe1')
	gvolume.description = 'upstreamTransverseMagnetVacuumPipe1 volume upstream of the target'
	gvolume.make_tube(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.setPosition(0, 0, zpos)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '334488'
	gvolume.publish(configuration)



	pipeLength    = 148
	zpos          = -204
	firstVacuumOR = 35

	gvolume = GVolume('upstreamTransverseMagnetVacuumPipe2')
	gvolume.description = 'upstreamTransverseMagnetVacuumPipe2 volume upstream of the target'
	gvolume.make_tube(0, firstVacuumOR, pipeLength, 0, 360)
	gvolume.setPosition(0, 0, zpos)
	gvolume.material    = 'G4_Galactic'
	gvolume.color       = '334488'
	gvolume.publish(configuration)

