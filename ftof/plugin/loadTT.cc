#include "ftof.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

string connection = "mysql://clas12reader@clasdb.jlab.org/clas12";
unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));

int icomponent;
vector<vector<double> > data;

bool FTOF_Plugin::loadTT(int runno, string variation)
{

	return true;
}
