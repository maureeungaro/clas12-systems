#ifndef FT_HODO_Plugin_HEADERS
#define FT_HODO_Plugin_HEADERS 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class FT_HODO_Plugin : public GDynamicDigitization {

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
	// status:
	//	0 - fully functioning
	//	1 - noisy channel
	//	3 - dead channel
	//  5 - any other issue
	vector<int> status[8][2];
	
	// noise
	vector<double>  pedestal[8][2];
	vector<double>  pedestal_rms[8][2];
	vector<double>  gain_pc[8][2];
	vector<double>  gain_mv[8][2];
	vector<double>  npe_threshold[8][2];
	
	// energy
	vector<double>  mips_charge[8][2];
	vector<double>  mips_energy[8][2];
	vector<double>  preamp_gain[8][2];
	
	// time
	vector<double>  time_offset[8][2];
	vector<double>  time_rms[8][2];
	
	// fadc parameters
	double  ns_per_sample;
	double  fadc_input_impedence;
	double  fadc_LSB;
	double  time_to_tdc;
	double  tdc_max;


};

#endif

