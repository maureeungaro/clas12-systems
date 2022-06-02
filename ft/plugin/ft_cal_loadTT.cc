#include "ft_cal.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;


bool FT_CAL_Plugin::loadTT(int runno, string variation)
{
	string connection = getenv ("CCDB_CONNECTION") == nullptr ? "mysql://clas12reader@clasdb.jlab.org/clas12" :  (string) getenv("CCDB_CONNECTION");
	unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));
	vector<vector<double> > data;

	translationTable = new GTranslationTable();

	string database   = "/daq/tt/ftcal:1";
	gDLogMessage("FT-CAL: Loading Translation Table " + database);
	data.clear(); calib->GetCalib(data, database);

	// filling translation table
	for(unsigned row = 0; row < data.size(); row++) {
		int crate   = data[row][0];
		int slot    = data[row][1];
		int channel = data[row][2];

		int crystal = data[row][5];
		int iX = crystal%22 + 1;
		int iY = crystal/22 + 1;

		// mode 0: "crate" is the frame source
		// mode 1: "crate/slot" is the frame source
		// mode 2: "crate/slot/channel" is the frame source
		int mode = 0;
		
		translationTable->addGElectronicWithIdentity({iX, iY}, GElectronic(crate, slot, channel, mode));
	}

	return true;
}
