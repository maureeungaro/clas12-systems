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
	translationTable = new GTranslationTable();

	vector<vector<double> > data;

	string database   = "/daq/tt/ftof:1";
	gDLogMessage("FTOF: Loading Translation Table " + database);
	data.clear(); calib->GetCalib(data, database);

	// filling translation table
	for(unsigned row = 0; row < data.size(); row++) {
		int crate   = data[row][0];
		int slot    = data[row][1];
		int channel = data[row][2];

		int sector = data[row][3];
		int panel = data[row][4];
		int paddle = data[row][5];
		int pmt = data[row][6];

		// mode 0: "crate" is the frame source
		// mode 1: "crate/slot" is the frame source
		// mode 2: "crate/slot/channel" is the frame source
		int mode = 0;

		// order is important as we could have duplicate entries w/o it
		translationTable->addGElectronicWithIdentity({sector, panel, paddle, pmt}, GElectronic(crate, slot, channel, mode));
	}

	return true;
}
