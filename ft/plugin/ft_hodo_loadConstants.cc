#include "ft_hodo.h"

// ccdb
#include <CCDB/Calibration.h>
#include <CCDB/Model/Assignment.h>
#include <CCDB/CalibrationGenerator.h>
using namespace ccdb;

// clhep
using namespace CLHEP;

bool FT_HODO_Plugin::loadConstants(int runno, string variation)
{
	string connection = getenv ("CCDB_CONNECTION") == nullptr ? "mysql://clas12reader@clasdb.jlab.org/clas12" :  (string) getenv("CCDB_CONNECTION");
	unique_ptr<Calibration> calib(CalibrationGenerator::CreateCalibration(connection));
	vector<vector<double> > data;

	string database = "/calibration/ft/fthodo/noise:" + to_string(runno) + ":"  + variation;
	gDLogMessage("FT-HODO: Getting noise from " + database);
	data.clear(); calib->GetCalib(data, database);
	for(unsigned row = 0; row < data.size(); row++) {
		int isector    = data[row][0];
		int ilayer     = data[row][1];
		
		double pdstl = data[row][3];
		pdstl = 101.;                      // Remove when DB will be filled
		double pdstl_RMS = data[row][4];
		pdstl_RMS  =2.;                    // Remove when DB will be filled
		
		pedestal[isector-1][ilayer-1].push_back(pdstl);
		pedestal_rms[isector-1][ilayer-1].push_back(pdstl_RMS);
		gain_pc[isector-1][ilayer-1].push_back(data[row][5]);
		gain_mv[isector-1][ilayer-1].push_back(data[row][6]);
		npe_threshold[isector-1][ilayer-1].push_back(data[row][7]);
	}
	
	
	database = "/calibration/ft/fthodo/charge_to_energy:" + to_string(runno) + ":"  + variation;
	gDLogMessage("FT-HODO: Getting charge_to_energy from " + database);
	data.clear(); calib->GetCalib(data, database);
	for(unsigned row = 0; row < data.size(); row++) {
		int isector    = data[row][0];
		int ilayer     = data[row][1];
		mips_charge[isector-1][ilayer-1].push_back(data[row][3]);
		mips_energy[isector-1][ilayer-1].push_back(data[row][4]);
	}

	database = "/calibration/ft/fthodo/time_offsets:" + to_string(runno) + ":"  + variation;
	gDLogMessage("FT-HODO: Getting time_offsets from " + database);
	data.clear(); calib->GetCalib(data, database);
	for(unsigned row = 0; row < data.size(); row++) {
		int isector    = data[row][0];
		int ilayer     = data[row][1];
		time_offset[isector-1][ilayer-1].push_back(data[row][3]);
		time_rms[isector-1][ilayer-1].push_back(data[row][4]);
	}

	// fadc parameters
	ns_per_sample = 4*ns;
	time_to_tdc   = 100/ns_per_sample;// conversion factor from time(ns) to TDC channels)
	tdc_max       = 8191;               // TDC range
	fadc_input_impedence = 50;
	fadc_LSB      = 0.4884;


	return true;
}
