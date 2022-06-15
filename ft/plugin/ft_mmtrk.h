#ifndef FT_MMTRK_Plugin_HEADERS
#define FT_MMTRK_Plugin_HEADERS 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class FT_MMTRK_Plugin : public GDynamicDigitization {

public:

	// mandatory readout specs definitions
	bool defineReadoutSpecs();

	// loads digitization constants
	bool loadConstants(int runno, string variation);

	// digitized the hit
	GDigitizedData* digitizeHit(GHit *ghit, size_t hitn);

private:

	// Calibration Constants
	// ---------------------
	double sigma_0      ;  // transverse diffusion
	double w_i          ;  // ionization energy

	double rmin ;          // inner radius of disks
	double rmax ;          // outer radius of disks
	double pitch;          // strip pitch
	int    nstrips;        // number of strips per layer
	int    nb_sigma;       // To define the number of strips to look at around the closest one


	// return strip number based on coordinate
	int get_strip_ID(double x, double y);

	// Create a GTouchableModifiers object with additional strips and their assigned energy
	GTouchableModifiers StripAndEnergyPairs( int layer, double x, double y, double z, double Edep, vector<double> dimensions);

	// change the GTouchable in sensitiveDetector::ProcessHit
	// by default the touchable is not changed
	// this function is loaded by plugin methods
	// notice that this returns a vector of touchables, one g4step can produce multiple hits
	//vector<GTouchable*> processTouchable(GTouchable *gTouchID, G4Step* thisStep);

	// get layer based on touchable
	int getLayer(GTouchable *gTouchID);
};

#endif

