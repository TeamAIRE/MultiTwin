/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#include <ctime>
#include <iostream>

using namespace std;

void duration(time_t start, time_t end, unsigned short int verbose)
{
	// Elapsed time in seconds
	int S = end - start;
	// Day, hour and min in seconds
	int day = 86400;
	int hour = 3600;
	int min = 60;
	//Days
	int D = S/day;
	S = S-(D*day);
	// Hours
	int H = S/hour;
	S = S-(H*hour);
	// Minutes
	int M = S/min;
	S = S-(M*min);
	// Print elapsed time, format --> DAY HOUR MIN SEC
	if( verbose == 1 )
	{
		cout << "TIME  - " << D << " d " << H << " h " << M << " m " << S << " s" << endl;
	}
}
