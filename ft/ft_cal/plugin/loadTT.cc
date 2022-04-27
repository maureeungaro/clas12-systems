#include "ft_cal.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

string connection = "mysql://clas12reader@clasdb.jlab.org/clas12";
unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));

int icomponent;
vector<vector<double> > data;

bool FT_CAL_Plugin::loadTT(int runno, string variation)
{
	translationTable = new GTranslationTable();

	vector<vector<double> > data;

	string database   = "/daq/tt/ftcal:1";
	gLogMessage("FT-CAL: Loading Translation Table " + database);
	data.clear(); calib->GetCalib(data, database);

	// filling translation table
	for(unsigned row = 0; row < data.size(); row++) {
		int crate   = data[row][0];
		int slot    = data[row][1];
		int channel = data[row][2];

		int crystal = data[row][5];

		// mode 0: "crate" is the frame source
		// mode 1: "crate/slot" is the frame source
		// mode 2: "crate/slot/channel" is the frame source
		int mode = 0;

		int iX = crystal%22 + 1;
		int iY = crystal/22 + 1;

		translationTable->addGElectronicWithIdentity({iX, iY}, GElectronic(crate, slot, channel, mode));
	}

	// translationTable->print();

	return true;
}
