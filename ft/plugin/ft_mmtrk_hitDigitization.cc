#include "ft_mmtrk.h"


GDigitizedData* FT_MMTRK_Plugin::digitizeHit(GHit *ghit, size_t hitn)
{

	GDigitizedData* gdata = new GDigitizedData(ghit);


	return gdata;
}
