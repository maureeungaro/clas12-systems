#include "ft_cal.h"

// G4 headers
#include "G4Poisson.hh"
#include "Randomize.hh"

GDigitizedData* FT_CAL_Plugin::digitizeHit(GHit *ghit, int hitn)
{
	vector<GIdentifier> identity = ghit->getGID();
	int IDX = identity[0].getValue();
	int IDY = identity[1].getValue();
	int iCrystal = (IDY-1)*22 + IDX-1;

	GDigitizedData* gdata = new GDigitizedData(ghit);

	float eTot = ghit->getTotalEnergyDeposited();
	float time = ghit->getAverageTime();
	vector<double> dimensions = ghit->getDetectorDimensions();
	float lz = ghit->getAvgLocalPosition().getX();

	double length = 2 * dimensions[2];

	// initialize ADC and TDC
	int ADC = 0;
	int TDC = 8191;
	float timeR = 0;

	if(eTot>0) {
		double dRight = length/2 - lz;       // distance along z between the hit position and the end of the crystal
		timeR  = time + dRight/light_speed;  // arrival time of the signal at the end of the crystal (speed of light in the crystal=15 cm/ns)

		// adding shift and spread on time
		timeR = timeR + time_offset[iCrystal] + G4RandGauss::shoot(0., time_rms[iCrystal]);

		TDC=int(timeR*time_to_tdc);
		if(TDC>tdc_max) TDC=(int)tdc_max;

		// calculate number of photoelectrons detected by the APD considering the light yield, the q.e., and the size of the sensor
		double charge   = eTot*mips_charge[iCrystal]/mips_energy[iCrystal];

		// add spread due to photoelectron statistics
		double npe_mean = charge/1.6E-7/preamp_gain[iCrystal]/apd_gain[iCrystal];
		double npe      = G4Poisson(npe_mean);

		// calculating APD output charge (in number of electrons) and adding noise
		double nel=npe*apd_gain[iCrystal];
		nel=nel*G4RandGauss::shoot(1.,apd_noise);
		if(nel<0) nel=0;
		// adding preamplifier input noise
		nel=nel+preamp_input_noise*G4RandGauss::shoot(0.,1.);
		if(nel<0) nel=0;

		// converting to charge (in picoCoulomb)
		ADC = (int) (charge/fadc_to_charge[iCrystal]);
	}

	gdata->includeVariable("sector",    1);
	gdata->includeVariable("layer",     1);
	gdata->includeVariable("component", iCrystal);
	gdata->includeVariable("order",     0);
	gdata->includeVariable("adc",       ADC);
	gdata->includeVariable("time",      timeR); // time in ns
	gdata->includeVariable("ped",       0);

	gdata->includeVariable("hitn",      hitn);

	// mandatory for streaming
	// first argument: gemc hit
	// second argument: time at electronics. Used to assign the payload to the frame buffer to stream
	// notice time is an int (assumed unit: ns)
	// third argument: charge at electronic: payload for this hit
	chargeAndTimeAtHardware((int) timeR, ADC, ghit, gdata);

	return gdata;
}
