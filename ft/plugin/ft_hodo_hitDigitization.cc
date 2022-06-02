#include "ft_hodo.h"

// G4 headers
#include "G4Poisson.hh"
#include "Randomize.hh"

GDigitizedData* FT_HODO_Plugin::digitizeHit(GHit *ghit, size_t hitn)
{

	GDigitizedData* gdata = new GDigitizedData(ghit);


	return gdata;
}
