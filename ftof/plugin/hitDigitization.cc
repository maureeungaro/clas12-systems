#include "ftof.h"

// G4 headers
#include "G4Poisson.hh"
#include "Randomize.hh"

GDigitizedData* FTOF_Plugin::digitizeHit(GHit *ghit, size_t hitn)
{
	GDigitizedData* gdata = new GDigitizedData(ghit);

	gdata->includeVariable("hitn",      (int) hitn);

	return gdata;
}
