from gemc_api_geometry import *
import math


from parameters import *


def buildHodoscope(configuration):
	gvolume = GVolume('ft_hodo')
	gvolume.mother      = 'root'
	gvolume.description = 'ft scintillation hodoscope'
	gvolume.makeG4Polycone('0', '360', VETO_zpos, VETO_iradius, VETO_oradius)
	gvolume.material    = 'G4_AIR'
	gvolume.color       = '3399FF'
	gvolume.style       = 0
	gvolume.visible     = 0
	gvolume.publish(configuration)

	gvolume = GVolume('ft_hodo_innervol')
	gvolume.mother      = 'ft_hodo'
	gvolume.description = 'ft scintillation hodoscope inner volume'
	gvolume.make_tube(VETO_RING_OR, VETO_OR, VETO_TN, 0.0, 360.0)
	gvolume.material    = 'G4_AIR'
	gvolume.setPosition(0, 0, VETO_Z)
	gvolume.color       = '3399FF'
	gvolume.style       = 0
	gvolume.visible     = 0
	gvolume.publish(configuration)

	gvolume = GVolume('ft_hodo_ring')
	gvolume.mother      = 'ft_hodo'
	gvolume.description = 'ft hodoscope support ring'
	gvolume.make_tube(VETO_RING_IR, VETO_RING_OR, VETO_RING_TN, 0.0, 360.0)
	gvolume.material    = 'ft_peek'
	gvolume.setPosition(0, 0, VETO_RING_Z)
	gvolume.color       = 'cccccc'
	gvolume.publish(configuration)

	LS_Z = -VETO_TN

	# loop over layers
	for l in range(n_L):
		L = l + 1
		LS_TN = VETO_SKIN_TN/2.0
		LS_Z  = LS_Z + LS_TN

		gvolume = GVolume(f'ft_hodo_L{L}')
		gvolume.mother      = 'ft_hodo_innervol'
		gvolume.description = f'ft_hodo layer {L} support'
		gvolume.make_tube(VETO_RING_OR, VETO_OR, LS_TN, 0.0, 360.0)
		gvolume.material    = 'carbonFiber'
		gvolume.setPosition(0, 0, LS_Z)
		gvolume.color       = 'EFEFFB'
		gvolume.publish(configuration)


		LS_Z = LS_Z + LS_TN
		LS_TN = tn_L[l]/2. + PAINT_TN
		TILE_TN = tn_L[l]/2
		LS_Z = LS_Z + LS_TN
		p_X=0.0
		p_Y=0.0
		p_Z=LS_Z
	
		for q in range(4):

			S = 1 + 2*q
			for i in range(n_S1):
				I = i+1
				sp_X = px_S1[i]*2 * (TILE_WW + 2*PAINT_TN)
				sp_Y = py_S1[i]*2 * (TILE_WW + 2*PAINT_TN)
				
				if   q == 0 :
					p_X = sp_X
					p_Y = sp_Y
				elif q == 1 :
					p_X = -sp_Y
					p_Y =  sp_X
				elif q == 2 :
					p_X = -sp_X
					p_Y = -sp_Y
				elif q == 3 :
					p_X =  sp_Y
					p_Y = -sp_X
				
				WW_TILE  = ww_S1[i]*TILE_WW/2.0
				WW_PAINT = ww_S1[i]*(TILE_WW + 2*PAINT_TN)/2.0
				TNAME  = 'ft_hodo_p30_'
				TTNAME = 'ft_hodo_p30_tile_'
				TCOLOR = '0431B4'
				
				if ww_S1[i] == 1 :
					TNAME  = 'ft_hodo_p15_'
					TTNAME = 'ft_hodo_p15_tile_'
					TCOLOR = '3399FF'
				
				gvolume = GVolume(f'{TNAME}{S}{L}{I}')
				gvolume.mother      = 'ft_hodo_innervol'
				gvolume.description = f'{TNAME} {S} {L} {I}'
				gvolume.setPosition(p_X, p_Y, p_Z)
				gvolume.make_box(WW_PAINT, WW_PAINT, LS_TN)
				gvolume.material    = 'G4_MYLAR'
				gvolume.color       = TCOLOR
				gvolume.publish(configuration)

				gvolume = GVolume(f'{TTNAME}{S}{L}{I}')
				gvolume.mother       = f'{TNAME}{S}{L}{I}'
				gvolume.description  = f'{TTNAME} {S} {L} {I}'
				gvolume.make_box(WW_TILE, WW_TILE, TILE_TN)
				gvolume.material     = 'scintillator'
				gvolume.color        = 'BCA9F5'
				gvolume.digitization = 'ft_hodo'
				gvolume.setIdentifier('sector', S, 'layer', L, 'component', I)
				gvolume.publish(configuration)


			S = 2 + 2*q
			for i in range(n_S2):

				I = i+1
				sp_X = px_S2[i]*2.0*(TILE_WW + 2*PAINT_TN)
				sp_Y = py_S2[i]*2.0*(TILE_WW + 2*PAINT_TN)
				if   q == 0 :
					p_X = sp_X
					p_Y = sp_Y
				elif q == 1 :
					p_X = -sp_Y
					p_Y =  sp_X
				elif q == 2 :
					p_X = -sp_X
					p_Y = -sp_Y
				elif q == 3 :
					p_X =  sp_Y
					p_Y = -sp_X

				WW_TILE  = ww_S2[i]*TILE_WW/2.0
				WW_PAINT = ww_S2[i]*(TILE_WW + 2*PAINT_TN)/2.0
				TNAME  = 'ft_hodo_p30_'
				TTNAME = 'ft_hodo_p30_tile_'
				TCOLOR = '0431B4'
				if ww_S2[i] == 1 :
					TNAME  = "ft_hodo_p15_"
					TTNAME = "ft_hodo_p15_tile_"
					TCOLOR = "3399FF"

				gvolume = GVolume(f'{TNAME}{S}{L}{I}')
				gvolume.mother      = 'ft_hodo_innervol'
				gvolume.description = f'{TNAME} {S} {L} {I}'
				gvolume.setPosition(p_X, p_Y, p_Z)
				gvolume.make_box(WW_PAINT, WW_PAINT, LS_TN)
				gvolume.material    = 'G4_MYLAR'
				gvolume.color       = TCOLOR
				gvolume.publish(configuration)

				gvolume = GVolume(f'{TTNAME}{S}{L}{I}')
				gvolume.mother       = f'{TNAME}{S}{L}{I}'
				gvolume.description  = f'{TTNAME} {S} {L} {I}'
				gvolume.make_box(WW_TILE, WW_TILE, TILE_TN)
				gvolume.material     = 'scintillator'
				gvolume.color        = 'BCA9F5'
				gvolume.digitization = 'ft_hodo'
				gvolume.setIdentifier('sector', S, 'layer', L, 'component', I)
				gvolume.publish(configuration)


		LS_Z = LS_Z + LS_TN


