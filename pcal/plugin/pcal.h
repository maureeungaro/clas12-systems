#ifndef PCAL_Plugin_HEADERS
#define PCAL_Plugin_HEADERS 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class PCAL_Plugin : public GDynamicDigitization {

public:

	// mandatory readout specs definitions
	bool defineReadoutSpecs();

	// loads digitization constants
	bool loadConstants(int runno, string variation);

	// loads the translation table
	bool loadTT(int runno, string variation);

	// digitized the hit
	GDigitizedData* digitizeHit(GHit *ghit, size_t hitn);

private:

	// Calibration Constants
	// ---------------------



};

#endif

