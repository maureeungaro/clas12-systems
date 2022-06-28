#include "pcal.h"

bool PCAL_Plugin::defineReadoutSpecs()
{
	float     timeWindow = 10;                  // electronic readout time-window of the detector
	float     gridStartTime = 0;                // defines the windows grid
	HitBitSet hitBitSet = HitBitSet("000000");  // defines what information to be stored in the hit
	bool      verbosity = true;

	readoutSpecs = new GReadoutSpecs(timeWindow, gridStartTime, hitBitSet, verbosity);

	return true;
}


// DO NOT EDIT BELOW THIS LINE: defines how to create the <PCAL_Plugin>
extern "C" GDynamicDigitization* GDynamicDigitizationFactory(void) {
	return static_cast<GDynamicDigitization*>(new PCAL_Plugin);
}

