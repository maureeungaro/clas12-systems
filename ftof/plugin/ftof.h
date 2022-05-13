#ifndef FTOF_Plugin_HEADERS
#define FTOF_Plugin_HEADERS 1

// glibrary
#include "gdynamicdigitization.h"
#include "gutsConventions.h"

class FTOF_Plugin : public GDynamicDigitization {

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

	// For paddle dependent constants read from CCDB
	// Array [6][3][2] -> sector,panel,LR

	// status:
	//	0 - fully functioning
	//	1 - noADC
	//	2 - noTDC
	//	3 - noADC, noTDC (PMT is dead)
	// 5 - any other reconstruction problem
	vector<int> status[6][3][2];


	vector<double> tdcconv[6][3][2];      // tdc_conc: tdc conversion factors
	vector<double> veff[6][3][2];         // veff: effective velocity
	vector<double> attlen[6][3][2];       // attlen: attenuation length
	vector<double> countsForMIP[6][3][2]; // countsForMIP: Desired ADC channel for MIP peak calibration
	vector<double> twlk[6][3][6];         // twlk: Time walk correction, 3 constants each for L and R

	// toff_LR and tof_P2P: time offsets for Left-Right and Paddle-to-Paddle
	vector<double> toff_LR[6][3];
	vector<double> toff_RFpad[6][3];
	vector<double> toff_P2P[6][3];

	// ======== FADC Pedestals and sigmas ===========
	double pedestal[6][3][62][2] = {};
	double pedestal_sigm[6][3][62][2] = {};

	// tres: Gaussian sigma for smearing time resolution
	// indexes are sector/layer/paddle
	vector<double> tres[6][3];

	int    npaddles[3];  // Number of paddles for Panel 1A, 1B and 2.
	int    thick[3];     // Thickness of paddles (cm) for Panel 1A, 1B and 2.
	double dEdxMIP;      // Nominal MIP specific energy loss (MeV/gm/cm2)
	double dEMIP[3];     // Nominal MIP energy loss (MeV) for Panel 1A, 1B and 2.

	double pmtPEYld;      // Photoelectron yield (p.e./MeV)


};

#endif

