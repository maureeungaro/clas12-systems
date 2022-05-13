#include "ftof.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

// clhep
using namespace CLHEP;

bool FTOF_Plugin::loadConstants(int runno, string variation)
{
	npaddles[0] = 23;
	npaddles[1] = 62;
	npaddles[2] = 5;

	thick[0] = 5.0;
	thick[1] = 6.0;
	thick[2] = 5.0;

	dEdxMIP = 1.956; // muons in polyvinyltoluene
	pmtPEYld = 500;

	return true;
}
