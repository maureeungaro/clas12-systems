#include "ft_mmtrk.h"


// clhep
using namespace CLHEP;

bool FT_MMTRK_Plugin::loadConstants(int runno, string variation)
{
	sigma_0  = 0.3*mm;      // very small transverse diffusion (temporary)
	w_i      = 25.0;        // ionization energy
	nb_sigma = 4;           // number of strips to be considered in the cluster definition

	rmin     =  70.43;      // inner radius of disks
	rmax     = 143.66;      // outer radius of disks
	pitch    =  0.560;      // pitch of the strips
	nstrips  = 768;         // Number of strips

	return true;
}
