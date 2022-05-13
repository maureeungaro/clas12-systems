#include "ftof.h"

bool FTOF_Plugin::defineReadoutSpecs()
{
	float     timeWindow = 10;                  // electronic readout time-window of the detector
	float     gridStartTime = 0;                // defines the windows grid
	HitBitSet hitBitSet = HitBitSet("000000");  // defines what information to be stored in the hit
	bool      verbosity = true;

	readoutSpecs = new GReadoutSpecs(timeWindow, gridStartTime, hitBitSet, verbosity);

	return true;
}


// DO NOT EDIT BELOW THIS LINE: defines how to create the <FTOF_Plugin>
extern "C" GDynamicDigitization* GDynamicFactory(void) {
	return static_cast<GDynamicDigitization*>(new FTOF_Plugin);
}

