#include "ft_hodo.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

bool FT_HODO_Plugin::loadTT(int runno, string variation)
{
	string connection = getenv ("CCDB_CONNECTION") == nullptr ? "mysql://clas12reader@clasdb.jlab.org/clas12" :  (string) getenv("CCDB_CONNECTION");
	unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));
	vector<vector<double> > data;

	translationTable = new GTranslationTable();

	string database   = "/daq/tt/fthodo:1";
	gDLogMessage("FT-HODO: Loading Translation Table " + database);
	data.clear(); calib->GetCalib(data, database);

	// filling translation table
	for(unsigned row = 0; row < data.size(); row++) {
		int crate   = data[row][0];
		int slot    = data[row][1];
		int channel = data[row][2];
		
		int sector  = data[row][3];
		int layer   = data[row][4];
		int component = data[row][5];
		int order   = data[row][6];

		// mode 0: "crate" is the frame source
		// mode 1: "crate/slot" is the frame source
		// mode 2: "crate/slot/channel" is the frame source
		int mode = 0;

		translationTable->addGElectronicWithIdentity({sector, layer, component, order}, GElectronic(crate, slot, channel, mode));
	}

	return true;
}
