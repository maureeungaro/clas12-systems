from gemc_api_geometry import *
import math


# global vars

###########################################################################################
###########################################################################################
# Define the relevant parameters of FT Geometry
#
# the FT geometry will be defined starting from these parameters
# and the position on the torus inner ring
#
# all dimensions are in mm
#

degrad    = 57.27
torus_z   = 2663.# position of the front face of the Torus ring (set the limit in z)

###########################################################################################
# CALORIMETER
#
# Define the number, dimensions and position of the crystals
Nx = 22                         # Number of crystals in horizontal directions
Ny = 22                         # Number of crystals in horizontal directions
Cfront  =  1897.8               # Position of the front face of the crystals
Cwidth  =    15.0               # Crystal width in mm (side of the squared front face)
Clength =   200.0               # Crystal length in mm
VM2000  =   0.130               # Thickness of the VM2000 wrapping
AGap    =   0.170               # Air Gap between Crystals, total wodth of crystal including wrapping and air gap is 15.3 mm
Flength =     8.0               # Length of the crystal front support
Fwidth  = Cwidth                # Width of the crystal front support
Wwidth  = Cwidth+VM2000         # Width of the wrapping volume
Vwidth  = Cwidth+VM2000+AGap    # Width of the crystal mother volume, total width of crystal including wrapping and air gap is 15.3 mm
Vlength = Clength+Flength       # Length of the crystal mother volume
Vfront  = Cfront-Flength        # z position of the volume front face
Slength =     7.0               # Length of the sensor 'box'
Swidth  = Cwidth                # Width of the sensor 'box'
Sgap    =     1.0               # Gap for flux detector
Sfront  = Vfront+Vlength+Sgap   # z position of the sensor front face

# Define the copper thermal shield parameters
# back disk
Bdisk_TN = 4.                                          # half thickness of the copper back disk
Bdisk_IR = 55.                                         # inner radius of the copper back disk
Bdisk_OR = 178.5                                       # outer radius of the copper back disk
Bdisk_Z  = Sfront+Slength+Bdisk_TN+0.1                 # z position of the copper back disk
# front disk
Fdisk_TN = 1.                                          # half thickness of the copper front disk supporting the crystal assemblies
Fdisk_IR = Bdisk_IR                                    # inner radius of the copper front disk
Fdisk_OR = Bdisk_OR                                    # outer radius of the copper front disk
Fdisk_Z  = Vfront-Fdisk_TN-0.1                         # z position of the copper front disk
# space for preamps
BPlate_TN = 25.                                        # half thickness of the preamps volume
BPlate_IR = Bdisk_IR                                   # inner radius of the preamps volume
BPlate_OR = Bdisk_OR                                   # outer radius of the preamps volume
BPlate_Z  = Bdisk_Z+Bdisk_TN+BPlate_TN+0.1             # z position of the preamps volume
# inner copper tube
Idisk_LT = (BPlate_Z+BPlate_TN-Fdisk_Z+Fdisk_TN)/2.    # length of the inner copper tube
Idisk_TN = 4                                           # thickness of the inner copper tube
Idisk_OR = Fdisk_IR                                    # outer radius of the inner copper tube matches inner radius of front and back disks
Idisk_IR = Fdisk_IR-Idisk_TN                           # inner radius of the inner copper tube
Idisk_Z  = (BPlate_Z+BPlate_TN+Fdisk_Z-Fdisk_TN)/2.    # z position of inner copper tube
# outer copper tube
Odisk_LT = (BPlate_Z+BPlate_TN-Fdisk_Z+Fdisk_TN)/2.    # length of the outer copper tube
Odisk_TN = 2                                           # thickness of the outer copper tube
Odisk_IR = Fdisk_OR                                    # inner radius of the outer copper tube matches outer radius of front and back disks
Odisk_OR = Fdisk_OR+Odisk_TN                           # outer radius of the outer copper tube
Odisk_Z  = Idisk_Z                                     # z position of the outer copper tube

# Define the motherboard parameters
Bmtb_TN = 1.                                           # half thickness of the motherboard
Bmtb_IR = Idisk_IR                                     # inner radius of the motherboard
Bmtb_OR = Odisk_OR                                     # outer radius of the motherboard
Bmtb_Z  = BPlate_Z + BPlate_TN + Bmtb_TN + 0.1         # z position of the motherboard
Bmtb_hear_WD = 80./2.                                  # half width of the motherboard extensions
Bmtb_hear_LN = 225./2                                  # half length of the motherboard extensions
Bmtb_hear_D0 = 0.                                      # displacement of the motherboard extensions
Bmtb_angle = [ 30., 150., 210., 330.]                  # angles of the motherboard extensions

# Define LED plate geometry parameters
LED_TN =   6.1                                        # half thickness of the pcb and pastic plate hosting the LEDs
LED_IR = Fdisk_IR                                     # inner radius of the pcb and pastic plate hosting the LEDs
LED_OR = Fdisk_OR                                     # outer radius of the pcb and pastic plate hosting the LEDs
LED_Z  = Fdisk_Z - Fdisk_TN - LED_TN - 0.1            # z position of the pcb and pastic plate hosting the LEDs

# bline: tungsten pipe inside the ft_cal
BLine_IR = 30.                                         # pipe inner radius
BLine_SR = 33.5                                        # pipe inner radius in steel case
BLine_DR = 25.1                                        # shield inner radius in steel case
BLine_TN = 10.                                         # pipe thickness
BLine_FR = BLine_IR + BLine_TN                         # radius in the front part, connecting to moller shield
BLine_OR = 100.                                        # radius of the back flange
BLine_BG = 1644.7                                      # z location of the beginning of the beamline (to be matched to moller shield)
BLine_ML = 1760.0                                      # z location of the end of the Moller shield


# back tungsten cup
BCup_tang = 0.0962                                     # tangent of 5.5 degrees
BCup_TN = 5.                                           # thickness of the flat part of the cup
BCup_ZM = Bmtb_Z+Bmtb_TN+0.1+43.4                      # z of the downstream face of the cup
BCup_Z1 = Bmtb_Z+Bmtb_TN+0.1+1                         # z of the side close to the motherboard (downstream)
BCup_Z2 = Bmtb_Z-Bmtb_TN-0.1-1                         # z of the side close to the motherboard (upstream)
BCup_ZE = BCup_ZM+BCup_TN                              # z of the downstream face of the cup
BCup_ZB = BCup_ZM-120.                                 # z beginning of the conical part
BCup_IRM = 190.                                        # inner radius at the beginning of the cone
BCup_ORB = BCup_ZB*BCup_tang                           # outer radius at the beginning of the cone
BCup_OR1 = BCup_Z1*BCup_tang                           # outer radius close to the MTB
BCup_OR2 = BCup_Z2*BCup_tang                           # outer radius close to the MTB
BCup_ORM = BCup_ZM*BCup_tang                           # outer radius at the front face of the plate
BCup_ORE = BCup_ZE*BCup_tang                           # outer radius at the back face of the plate
BCup_angle = int(math.atan(Bmtb_hear_WD/Bmtb_OR)*degrad*10)/10+0.5
BCup_iangle = [30.+BCup_angle, 150.+BCup_angle, 210.+BCup_angle, 330.+BCup_angle]
BCup_dangle = [(90.-BCup_iangle[0])*2., (180.-BCup_iangle[1])*2., (90.-BCup_iangle[0])*2.,(180.-BCup_iangle[1])*2.]

TPlate_TN= 20. # thickness of the tungsten plate on the back of the FT-Cal



###########################################################################################
# OUTER INSULATION
O_Ins_TN  = 15.-0.01
O_Ins_Z1  = Fdisk_Z - Fdisk_TN - LED_TN*2 - 10.8 - O_Ins_TN #1849.6
O_Ins_Z2  = O_Ins_Z1 + O_Ins_TN
O_Ins_Z3  = BCup_ZB
O_Ins_Z4  = BCup_Z2
O_Ins_Z5  = BCup_Z1
O_Ins_Z6  = BCup_ZM
O_Ins_Z7  = BCup_ZE
O_Ins_Z8  = BCup_ZE + 0.01
O_Ins_Z9  = O_Ins_Z8 + O_Ins_TN
O_Ins_Z10 = O_Ins_Z9
O_Ins_Z11 = O_Ins_Z10 + TPlate_TN

O_Ins_I1  = BLine_IR + BLine_TN + 0.01
O_Ins_I2  = O_Ins_Z2*BCup_tang +0.01
O_Ins_I3  = O_Ins_Z3*BCup_tang +0.01
O_Ins_I4  = O_Ins_Z4*BCup_tang +0.01
O_Ins_I5  = O_Ins_Z5*BCup_tang +0.01
O_Ins_I6  = O_Ins_Z6*BCup_tang +0.01
O_Ins_I7  = O_Ins_Z7*BCup_tang +0.01
O_Ins_I8  = O_Ins_Z8*BCup_tang +0.01
O_Ins_I9  = O_Ins_I1
O_Ins_I10 = O_Ins_Z10*BCup_tang +0.01
O_Ins_I11 = O_Ins_I10

O_Ins_O1  = O_Ins_Z1*BCup_tang +0.01 + O_Ins_TN
O_Ins_O2  = O_Ins_I2 + O_Ins_TN
O_Ins_O3  = O_Ins_I3 + O_Ins_TN
O_Ins_O4  = O_Ins_I4 + O_Ins_TN
O_Ins_O5  = O_Ins_I5 + O_Ins_TN
O_Ins_O6  = O_Ins_I6 + O_Ins_TN
O_Ins_O7  = O_Ins_I7 + O_Ins_TN
O_Ins_O8  = O_Ins_I8 + O_Ins_TN
O_Ins_O9  = O_Ins_Z9*BCup_tang +0.01 + O_Ins_TN
O_Ins_O10 = O_Ins_I10 + O_Ins_TN
O_Ins_O11 = O_Ins_I11 + O_Ins_TN

O_Ins_I4 = O_Ins_Z4*BCup_tang +0.5
O_Ins_I5 = O_Ins_Z5*BCup_tang +0.5

###########################################################################################
# INNER INSULATION
I_Ins_LT = (BCup_ZE - O_Ins_Z2 -0.1)/2.
I_Ins_OR =  Idisk_IR - 0.1
I_Ins_IR =  O_Ins_I1
I_Ins_Z  = (BCup_ZE + O_Ins_Z2)/2.

###########################################################################################
# OUTER SHELL
O_Shell_TN = 2.-0.01
O_Shell_Z1 = O_Ins_Z1-O_Shell_TN-0.01
O_Shell_Z2 = O_Shell_Z1+O_Shell_TN
O_Shell_Z3 = O_Ins_Z3
O_Shell_Z4 = BCup_Z2
O_Shell_Z5 = BCup_Z1
O_Shell_Z6 = O_Ins_Z6
O_Shell_Z7 = O_Ins_Z7
O_Shell_Z8 = O_Ins_Z8
O_Shell_Z9 = O_Ins_Z9
O_Shell_Z10 = O_Ins_Z10
O_Shell_Z11 = O_Ins_Z11 + 0.01
O_Shell_Z12 = O_Shell_Z11
O_Shell_Z13 = O_Shell_Z12 + O_Shell_TN

O_Shell_I1 = O_Ins_I1
O_Shell_I2 = O_Shell_Z2*BCup_tang + O_Ins_TN + 0.01
O_Shell_I3 = O_Shell_Z3*BCup_tang + O_Ins_TN + 0.01
O_Shell_I4 = O_Shell_Z4*BCup_tang + O_Ins_TN + 0.01
O_Shell_I5 = O_Shell_Z5*BCup_tang + O_Ins_TN + 0.01
O_Shell_I6 = O_Shell_Z6*BCup_tang + O_Ins_TN + 0.01
O_Shell_I7 = O_Shell_Z7*BCup_tang + O_Ins_TN + 0.01
O_Shell_I8 = O_Shell_Z8*BCup_tang + O_Ins_TN + 0.01
O_Shell_I9 = O_Shell_Z9*BCup_tang + O_Ins_TN + 0.01
O_Shell_I10 = O_Shell_Z10*BCup_tang + O_Ins_TN + 0.01
O_Shell_I11 = O_Shell_Z11*BCup_tang + O_Ins_TN + 0.01
O_Shell_I12 = O_Shell_I11 - O_Ins_TN -5.
O_Shell_I13 = O_Shell_I12

O_Shell_O1 = O_Shell_Z1*BCup_tang + O_Ins_TN + 0.01 + O_Shell_TN
O_Shell_O2 = O_Shell_I2 + O_Shell_TN
O_Shell_O3 = O_Shell_I3 + O_Shell_TN
O_Shell_O4 = O_Shell_I4 + O_Shell_TN
O_Shell_O5 = O_Shell_I5 + O_Shell_TN
O_Shell_O6 = O_Shell_I6 + O_Shell_TN
O_Shell_O7 = O_Shell_I7 + O_Shell_TN
O_Shell_O8 = O_Shell_I8 + O_Shell_TN
O_Shell_O9 = O_Shell_I9 + O_Shell_TN
O_Shell_O10 = O_Shell_I10 + O_Shell_TN
O_Shell_O11 = O_Shell_I11 + O_Shell_TN
O_Shell_O12 = O_Shell_O11
O_Shell_O13 = O_Shell_O12

O_Shell_I4 = O_Shell_Z4*BCup_tang + O_Ins_TN + 0.7
O_Shell_I5 = O_Shell_Z5*BCup_tang + O_Ins_TN + 0.7

###########################################################################################
# FT BEAMLINE COMPONENTS

# ft to torus pipe
Tube_OR         =  75.0
back_flange_OR  = 126.0
front_flange_OR = 148.0
flange_TN       =  15.0


TPlate_RR  = TPlate_TN * 0.6
TPlate_Z1  = O_Ins_Z9 + 0.01
TPlate_Z2  = TPlate_Z1 + TPlate_TN-0.01
TPlate_ZM  = TPlate_Z2 - TPlate_RR
TPlate_MR  = BLine_IR  + BLine_TN + TPlate_RR

BLine_MR  = BLine_IR + BLine_TN   # outer radius in the calorimeter section
BLine_Z1  = BLine_BG
BLine_Z2  = BLine_ML   + 0.2
BLine_Z3  = O_Shell_Z1 - 0.01
BLine_Z4  = TPlate_Z2  + 0.01
BLine_Z5  = BLine_Z4   - 0.01 + 20



###########################################################################################
# Hodoscope Dimension and Parameters
VETO_TN = 38./2. # thickness of the hodoscope volume
VETO_OR = 178.5  # outer radius
VETO_IR = 40.    # inner radius
VETO_Z  = O_Shell_Z1 - VETO_TN - 0.1 # position along z

VETO_RING_TN = 37./2. # thickness of the hodoscope volume
VETO_RING_IR = VETO_IR
VETO_RING_OR = 105/2.
VETO_RING_Z  = O_Shell_Z1 - VETO_RING_TN - 0.1 # position along z

VETO_SKIN_TN = 0.5
PAINT_TN     = 0.1
TILE_WW      = 15.0

VETO_iradius = [VETO_RING_OR,     VETO_RING_OR, VETO_IR, VETO_IR]
VETO_oradius = [VETO_OR,          VETO_OR,      VETO_OR, VETO_OR]
VETO_zpos    = [VETO_Z - VETO_TN, 1810.6,       1810.6,  VETO_Z + VETO_TN]

q_X = [1., -1., -1.,  1.]
q_Y = [1.,  1., -1., -1.]


n_L = 2
tn_L = [ 7.0, 15.0 ]
n_S1 = 9
px_S1 = [ 3.25, 2.5, 4.25, 3.5, 2.5, 4.5, 3.5, 2.5, 1.75 ]
py_S1 = [ 4.25, 4.5, 3.25, 3.5, 3.5, 2.5, 2.5, 2.5, 1.75 ]
ww_S1 = [ 1.00, 2.0, 1.00, 2.0, 2.0, 2.0, 2.0, 2.0, 1.00 ]

n_S2 = 20
px_S2 = [  1.5,  0.5, -0.5, -1.5,  1.5,  0.5, -0.5, -1.5,  1.5,  0.5, -0.5, -1.5,  1.75,  1.25,  0.75,  0.25, -0.25, -0.75, -1.25, -1.75 ]
py_S2 = [  5.0,  5.0,  5.0,  5.0,  4.0,  4.0,  4.0,  4.0,  3.0,  3.0 , 3.0,  3.0,  2.25,  2.25,  2.25,  2.25,  2.25,  2.25,  2.25,  2.25 ]
ww_S2 = [  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00,  1.00 ]


###########################################################################################
# Tracker Dimension and Parameters
# Gabriel Charles - 2014
# Michel Garçon - Jan. 2017
# Ported to python by Mauri - June 2022


# Mother volume dimensions
MVftt_ir   = 40
MVftt_mr   = 59.75
MVftt_er   = 50.
MVftt_or   = 170.0
MVftt_z1   = 1760.0 # includes support ring
MVftt_zmin = 1770.0 # should be <= 1774
MVftt_zmax = 1809.0 # should be >= 1806 and <= 1809.6
MVftt_z4   = 1810.6 # includes support ring
MVftt_zctr = (MVftt_zmax + MVftt_zmin)/2.0
MVftt_dz   = (MVftt_zmax - MVftt_zmin)/2.0

nlayer = 2

# Detector inner and outer radii
InnerRadius = 60.0
OuterRadius = 170.0

# Half-thicknesses:
Epoxy_Dz 		= 0.5*0.1
# 0.1 is half the 200 microns thickness (1/2 is attributed to each disk
# some detectors may have 500 microns glue instead of 200 check !
PCB_Dz 		      = 0.5*0.2
Strips_Dz 		   = 0.5*0.012
Kapton_Dz         = 0.5*0.075
ResistStrips_Dz   = 0.5*0.020
Gas1_Dz 		      = 0.5*0.128
Mesh_Dz 		      = 0.5*0.018
Photoresist_Dz    = 0.5*0.064
AluRings_Dz       = 0.5*5.0
DriftElectrode_Dz = 0.5*0.012
# Gas2_Dz 		= Photoresist_Dz + AluRings_Dz - DriftElectrode_Dz
# above is the real thickness, but leads to overlaps -> neglect 64 microns of gas (replaced de facto by air since the positioning does not change)
Gas2_Dz 		   = AluRings_Dz - DriftElectrode_Dz
DriftPCB_Dz		= 0.5*0.2
DriftGround_Dz = 0.5*0.005
Protection_Dz  = 0.5*0.05

AssemblyRing1_Dz   = 0.5*7.8
AssemblyRing2_Dz   = 0.5*7.8
AssemblyRing3_Dz   = 0.5*9.0

#zoffset            = 0.    # may be adjusted
CenteringSupportRing_zmin = (MVftt_z1, 1774.,  1805.2,    MVftt_zmin)
CenteringSupportRing_zmax = (1774.,     1805.2, MVftt_z4, 1774.)
CenteringSupportRing_Rmin = (MVftt_ir, MVftt_ir, MVftt_ir, MVftt_mr)
CenteringSupportRing_Rmax = (MVftt_mr, 50.,       MVftt_er, 67.)

MVftt_nplanes = 6
MVftt_iradius = (MVftt_ir, MVftt_ir,   MVftt_ir,   MVftt_ir,   MVftt_ir,   MVftt_ir)
MVftt_oradius = (MVftt_mr, MVftt_mr,   MVftt_or,   MVftt_or,   MVftt_er,   MVftt_er )
MVftt_zpos    = (MVftt_z1, MVftt_zmin, MVftt_zmin, MVftt_zmax, MVftt_zmax, MVftt_z4)


zrel = [0.0] * 13    # zrel[i] = zmax(i) of Table 1 of MG report, i= 1,12.
zrel[0] =  0.
zrel[1] =  zrel[0]  + 2.*Epoxy_Dz
zrel[2] =  zrel[1]  + 2.*PCB_Dz
zrel[3] =  zrel[2]  + 2.*Strips_Dz
zrel[4] =  zrel[3]  + 2.*Kapton_Dz
zrel[5] =  zrel[4]  + 2.*ResistStrips_Dz
zrel[6] =  zrel[5]  + 2.*Gas1_Dz
zrel[7] =  zrel[6]  + 2.*Mesh_Dz
zrel[8] =  zrel[7]  + 2.*(Photoresist_Dz+Gas2_Dz)
zrel[9] =  zrel[8]  + 2.*DriftElectrode_Dz
zrel[10] = zrel[9]  + 2.*DriftPCB_Dz
zrel[11] = zrel[10] + 2.*DriftGround_Dz
zrel[12] = zrel[11] + 2.*Protection_Dz

z_abs  = CenteringSupportRing_zmax[3] # entrance of detector1/disk1 = end of SupportRing4 = 1774.
# starting absolute z-coordinate for each disk
z0 = [0.0] * 2
z0[0]     = z_abs + zrel[12]
z0[1]     = z0[0] + 2.*zrel[9] + 2.*AssemblyRing3_Dz


# G4 materials
epoxy_material       = 'epoxy'
pcboard_material     = 'myFR4'
strips_material      = 'mmstrips'
kapton_material      = 'myKapton'
resistive_material   = 'ResistPaste'
gas_material         = 'mmgas'
mesh_material        = 'mmmesh'
photoresist_material = 'myPhRes'
drift_material       = 'mmmylar'


# G4 colors
epoxy_color      = 'e200e1'
pcboard_color    = '0000ff'
strips_color     = '353540'
gas_color        = 'e10000'
mesh_color       = '252020'
photoresist_color= 'd200d1'
drift_color      = 'fff600'
alu_color        = 'aaaaff'


#  FTM FEE Boxes
FEE_Disk_OR = 200.
FEE_Disk_LN = 2.
FEE_ARM_LN  = 530./2.-80
FEE_ARM_WD  = 90./2.

# size of crate
FEE_WD = 91./2.
FEE_HT = 265.5/2.
FEE_LN = 242./2.
FEE_TN = 1.5

FEE_PVT_TN=10.

FEE_PVT_WD = FEE_WD+FEE_PVT_TN
FEE_PVT_HT = FEE_HT+FEE_PVT_TN
FEE_PVT_LN = FEE_LN+FEE_PVT_TN

FEE_A_WD = FEE_WD-FEE_TN
FEE_A_HT = FEE_HT-FEE_TN
FEE_A_LN = FEE_LN-FEE_TN
FEE_azimuthal_angle = (210., 270., 330.)
FEE_polar_angle = -22.


# define crystals mother volume
nplanes_FT_CRY = 2
z_plane_FT_CRY = [  Idisk_Z-Idisk_LT,   Idisk_Z+Idisk_LT ]
iradius_FT_CRY = [          Idisk_IR,          Idisk_IR  ]
oradius_FT_CRY = [          Odisk_OR,          Odisk_OR  ]


