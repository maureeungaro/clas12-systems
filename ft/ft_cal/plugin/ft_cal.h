#ifndef FT_CAL_Plugin_HEADERS
#define FT_CAL_Plugin_HEADERS 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class FT_CAL_Plugin : public GDynamicDigitization {

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

	// noise
	float pedestal[484];
	float pedestal_rms[484];
	float noise[484];
	float noise_rms[484];
	float threshold[484];

	// energy
	float mips_charge[484];
	float mips_energy[484];
	float fadc_to_charge[484];
	float preamp_gain[484];
	float apd_gain[484];

	// time
	float time_offset[484];
	float time_rms[484];

	// fadc parameters
	float ns_per_sample;
	float fadc_input_impedence;
	float time_to_tdc;
	float tdc_max;

	// preamp parameter
	float preamp_input_noise;
	float apd_noise ;

	// crystal paramters
	float light_speed;

	//	voltage signal parameters, using float gaussian + delay (function DGauss, need documentation for it)
	float vpar[4];

};

#endif

