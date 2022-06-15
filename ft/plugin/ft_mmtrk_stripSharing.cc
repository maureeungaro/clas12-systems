#include "ft_mmtrk.h"

// clhep
using namespace CLHEP;

// c++
using namespace std;

// Routines to share energy between strips:
// A single g4 step can generate multiple hits

// return strip number based on coordinate
int FT_MMTRK_Plugin::get_strip_ID(double x, double y) {

	double r = sqrt(x*x + y*y);

	if( r < rmax && r > rmin && fabs(y) < pitch*nstrips*2/6 ) {

		int strip = (int) floor( y / pitch) + 1 + nstrips*2/6;

		if( strip > nstrips*3/6) { // strip in the top sector
			strip += nstrips*2/6;
		}
		else if( strip > nstrips/6 && x>0 ) {
			strip += nstrips*2/6;
		}
		return strip;
	}

	return -1;
}




// Create a GTouchableModifiers object with additional strips and their assigned energy
GTouchableModifiers FT_MMTRK_Plugin::StripAndEnergyPairs( int layer, double x, double y, double z, double Edep, vector<double> dimensions) {

	// the variable being modified is the strip (component)
	GTouchableModifiers stripAndEnergyPairs({"component"});

	// number of electrons (Nt)
	int Nel = (int) (1e6*Edep/w_i);
	double r = sqrt(x*x+y*y);

	// get layer position and drift distance from the detector dimensions
	double z0           = -dimensions[2];
	double hdrift       =  dimensions[2]*2;

	if ( fabs(z-z0) > (hdrift+0.2) ) {
		gDLogMessage("FT-MMTRK: Warning! z position of the FTM hit is not in the sensitive volume:  z-z0 = " + to_string(z-z0) );
	}
	if( r < dimensions[0] || r > dimensions[1]) {
		gDLogMessage("FT-MMTRK: Warning! r position of the FTM hit is not in the sensitive volume: r = " + to_string(r) );
	}

	double sigma_td_max = sigma_0*sqrt(hdrift/cm);
	double sigma_td     = sigma_td_max* sqrt(fabs(z-z0)/hdrift); // expression without Lorentz angle

	// check if hit radius is within active area
	if( r < rmax && r > rmin) {

		double x_real = 0;
		double y_real = 0;

		if ( layer%2 == 0 )      { // y_real is the coordinate given by the detector; strips are along x_real
			x_real = y;
			y_real = x;
		}
		else if ( layer%2 == 1 ) { // y_real is the coordinate given by the detector; strips are along x_real
			x_real = x;
			y_real = y;
		}

		// calculate the y coordinate of closest strip (N.B. y_strip may exceed the actual strip range
		// because the active area is a bit larger than the one instrumented with strips)
		double y_strip = pitch*( floor(y_real/pitch)) + pitch/2;

		// calculates y coordinates of strips that may be involved in the cluster
		double weight_tot = 0;
		bool noStripsIdentified = true;
		for(int i=-nb_sigma; i <= nb_sigma; i++ ) {

			// calculate strip coordinate
			double iy = y_strip + i*pitch;

			// determine the strip number
			int istrip = get_strip_ID(x_real , iy);

			// check if strip number is well defined (i.e. now really inside the active volume)
			if( istrip > 0 ) {

				// calculate weight
				double weight = exp(-(iy-y_real)*(iy-y_real)/2/sigma_td/sigma_td);
				int weight_n = round(weight*Nel*10);   // round weight to closer integer to get rid of very low energy hits
				if ( weight_n > 0 || i ==0 ) {         // save strips with non zero weight or at least the central one
					stripAndEnergyPairs.insertIdAndWeight("component", istrip, weight);

					weight_tot += weight;
					noStripsIdentified = false;
				}
			}

		}

		if( noStripsIdentified ) {    // if not strips have been identified, set at least 1, strip number -1 with all the energy in it
			stripAndEnergyPairs.insertIdAndWeight("component", -1, 1);
		}

		stripAndEnergyPairs.assignOverallWeight("component", weight_tot);


	} else {
		// outside acceptance, return strip -1 with all the energy in it
		stripAndEnergyPairs.insertIdAndWeight("component", -1, 1);
	}

	return stripAndEnergyPairs;
}

// get layer based on touchable
int FT_MMTRK_Plugin::getLayer(GTouchable *gTouchID) {

	// FTM gidentity:
	// superlayer, type, segment, strip
	vector<GIdentifier> ftmGID = gTouchID->getIdentity();
	return ftmGID[0].getValue() + ftmGID[1].getValue() - 2 ;
}

// access to GetTouchableHandle()->GetHistory()
#include "G4TouchableHistory.hh"

//// change the GTouchable in sensitiveDetector::ProcessHit
//// by default the touchable is not changed
//// this function is loaded by plugin methods
//// notice that this returns a vector of touchables, one g4step can produce multiple hits
//vector<GTouchable*> FT_MMTRK_Plugin::processTouchable(GTouchable *gTouchID, G4Step* thisStep) {
//
//	// Local Coordinates of interaction, from global
//	G4ThreeVector globalxyz = thisStep->GetPostStepPoint()->GetPosition();
//	G4ThreeVector localXYZ  = thisStep->GetPreStepPoint()->GetTouchableHandle()->GetHistory()->GetTopTransform().TransformPoint(globalxyz);
//
//	double xlocal          = localXYZ.x();
//	double ylocal          = localXYZ.y();
//	double zlocal          = localXYZ.z();
//	double depe            = thisStep->GetTotalEnergyDeposit();
//	vector<double> detDims = gTouchID->getDetectorDimensions();
//
//	GTouchableModifiers stripAndEnergyPairs = StripAndEnergyPairs(getLayer(gTouchID), xlocal, ylocal, zlocal, depe, detDims);
//
//	return processGTouchableModifiers(gTouchID, stripAndEnergyPairs);
//
//}
