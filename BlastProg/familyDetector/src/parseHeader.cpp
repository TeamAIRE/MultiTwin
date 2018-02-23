/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#include "parseHeader.h"
#include <iostream>
#include <string>
#include <map>
#include <iterator>
#include <algorithm>
#include <list>
#include <string>
#include <sstream> // istringstream
#include <cstring> // strcmp

using namespace std;

// getPositions is a function which takes a string containing 
// the blastp headers and returns a list of the following header
// positions:
//	- qseqid
//	- sseqid
//	- qstart
//	- qend
//	- qlen
//	- sstart
//	- send
//	- slen
//	- pident
//	- evalue

map<string,unsigned short int> getPositions(string header)
{
	//list<short int> headersPosition;
	map<string,unsigned short int> headersPosition;
	// Initialize headers status
	map<string,int> status;
	status["qseqid"] = 0;
	status["sseqid"] = 0;
	status["qstart"] = 0;
	status["qend"] = 0;
	status["qlen"] = 0;
	status["sstart"] = 0;
	status["send"] = 0;
	status["slen"] = 0;
	status["evalue"] = 0;
	status["pident"] = 0;
	//
	// Split 
	istringstream iss(header);
	list<string> headerList;
	copy(istream_iterator<string>(iss), istream_iterator<string>(), back_inserter<list<string> >(headerList));
	list<string>::iterator pos;
	short int i = 0;
	//short int found = 0;
	for ( pos = headerList.begin(); pos != headerList.end(); pos++)
	{
		//cout << *pos << endl;
		string a = *pos;
		if( !strcmp(a.c_str(),"qseqid") )
		{
			headersPosition["qseqid"] = i;
			status["qseqid"]++;
		}
		else if( !strcmp(a.c_str(),"sseqid") )
		{
			headersPosition["sseqid"] = i;
			status["sseqid"]++;
		}
		else if( !strcmp(a.c_str(),"pident") )
		{
			headersPosition["pident"] = i;
			status["pident"]++;
		}
		else if( !strcmp(a.c_str(),"evalue") )
		{
			headersPosition["evalue"] = i;
			status["evalue"]++;
		}
		else if( !strcmp(a.c_str(),"qstart") )
                {
			headersPosition["qstart"] = i;
			status["qstart"]++;
                }
		else if( !strcmp(a.c_str(),"qend") )
                {
			headersPosition["qend"] = i;
			status["qend"]++;
                }
		else if( !strcmp(a.c_str(),"qlen") )
		{
			headersPosition["qlen"] = i;
			status["qlen"]++;
		}
		else if( !strcmp(a.c_str(),"sstart") )
                {
			headersPosition["sstart"] = i;
			status["sstart"]++;
                }
		else if( !strcmp(a.c_str(),"send") )
                {
			headersPosition["send"] = i;
			status["send"]++;
                }
		else if( !strcmp(a.c_str(),"slen") )
		{
			headersPosition["slen"] = i;
			status["slen"]++;
		}
		// increment position
		i++;
	}
	// Check if all positions have been retrived !
	unsigned short int Exit = 0;
	map<string,int>::iterator p;
	for( p = status.begin(); p != status.end(); ++p )
	{
		if( p->second > 1 )
		{
			cout << p->first << " is duplicated !" << endl;
			Exit = 1;
		}
		else if( p->second == 0)
		{
			cout << p->first << " is missing !" << endl;
			Exit = 1;
		}
	}
	if( Exit == 1)
	{
		cout << "~~~~~ ERROR ! Please check your header ! ~~~~~" << endl;
		exit(1);
	}
	//return headerPositions list if everything is ok
	return headersPosition;
}
