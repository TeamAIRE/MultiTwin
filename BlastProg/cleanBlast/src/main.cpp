/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of CleanBlast.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "parseHeader.h"
#include "functions.h"
#include "createNetwork.h"
#include "getTime.h"
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <list>
#include <iterator>
#include <unistd.h>
#include <stdlib.h>
#include <sstream>
#include <algorithm>
#include <fstream>
#include <map>
#include <thread>
#include <cmath>
#include <ctime>
#include <set>
#include <vector>

using namespace std;

int main(int argc, char * argv[])
{
	// ALL TIME (start)
	time_t Astart = time(NULL);
	// *************** Default Values ***************
	// Blastp file header
	string header = "qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen";
	// Verbose mode
	unsigned short int verbose = 1;
	// Percentage of identity threshold
	float pidentLimit = 30;
	// hit min coverage
	unsigned short int minCov = 0;
	// Mutual coverage
	unsigned short int mutualCov = 0;
	// numbering
	unsigned short int numbering = 0;
	// Check cmd line 
	if( argc == 1 || argc < 3 || argc > 18 )
	{
		cout << endl;
		cout << "Usage : " << argv[0] << " -i blastp.out [optional -h header -p pident -c hit_cov -m mutual_cov -n numbering -d output_dir -v verbose]" << endl << endl;
		cout << "-- Default values --" << endl << endl;
		cout << "header       : " << header << endl;
		cout << "pident_limit : " << pidentLimit << endl;
		cout << "hit_cov      : " << minCov << endl;
		cout << "mutual_cov   : " << mutualCov << endl;
		cout << "numbering    : " << numbering << endl;
		cout << "verbose      : " << verbose << endl;
		exit(1);
	}
	// Time
	time_t start, end;
	int c;
	// Blastp.out file
	string fileIn;
	// FusedTriplets output file
	string fileOut;
	// output dir
	string outDir;
	// Get arguments
	while( (c = getopt (argc, argv, "i:h:p:c:m:n:d:v:")) != -1)
	{
		switch(c)
		{
			case 'i':
				fileIn = optarg;
				break;
			case 'h':
				header = optarg;
				break;
			case 'p':
				pidentLimit = atof(optarg);
				break;
			case 'n':
				numbering = atoi(optarg);
				break;
			case 'c':
				minCov = atoi(optarg);
				break;
			case 'm':
				mutualCov = atoi(optarg);
				break;
			case 'd':
				outDir = optarg;
				break;
			case 'v':
				verbose = atoi(optarg);
				break;
			default:
				cout << endl;
				cout << "Usage : " << argv[0] << " -i blastp.out [optional -p pident -c hit_cov -m mutual_cov -n numbering -v verbose]" << endl << endl;
				cout << "-- Default values --" << endl << endl;
				cout << "header       : " << header << endl;
				cout << "pident_limit : " << pidentLimit << endl;
				cout << "hit_cov      : " << minCov << endl;
		                cout << "mutual_cov   : " << mutualCov << endl;
				cout << "numbering    : " << numbering << endl;
				cout << "verbose      : " << verbose << endl;
				exit(1);
				break;
		}
	}
	// input file basename
	string basename = fileIn.substr(fileIn.find_last_of("\\/")+1);
	// Output file
	if(outDir != "")
	{
		fileOut = outDir + "/" + basename + ".cleanNetwork";
	}
	else
	{
		fileOut = basename + ".cleanNetwork";
	}
	// Print running command line
	if( verbose == 1 )
	{
		cout << "---------- PARAMETERS ----------" << endl << endl;
		cout << "Input   : " << basename << endl << endl;
		cout << "Ouput   : " << fileOut << endl << endl;
		cout << "--------------------------------" << endl << endl;
	}
	// Create all maps and their reference
	// edges[query,subject]:qstart, qend, sstart, send, evalue and pident
	map<pair<unsigned long long int, unsigned long long int>, edgeValues> edges;
	map<pair<unsigned long long int, unsigned long long int>, edgeValues>& refEdges = edges;
	// genes seq length info
	map<unsigned long long int, unsigned int> genes;
	map<unsigned long long int, unsigned int>& refGenes = genes;
	// Check header
	map<string, unsigned short int> positionsList;
	map<string, unsigned short int>& refPositionsList = positionsList;
	// get header position
	positionsList = getPositions(header);
	// Create network
	start = time(NULL);
	if( verbose == 1 )
	{
		cout << "----- NETWORK CREATION -----" << endl << endl;
		cout << "START - " << asctime(localtime(&start)) << endl;
		cout << endl;
	}
	createNetwork(fileIn, fileOut, pidentLimit, refPositionsList, refEdges, refGenes, minCov, mutualCov, numbering, verbose);
	end = time(NULL);
	if( verbose == 1 )
	{
		cout << "END   - " << asctime(localtime(&end)) << endl;
	}
	// Get time
	duration( start, end, verbose );
	cout << endl;
}
//END
