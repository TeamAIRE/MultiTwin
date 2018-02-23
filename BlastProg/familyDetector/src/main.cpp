/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "parseHeader.h"
#include "functions.h"
#include "loadNetwork.h"
#include "dfscc.h"
#include "families.h"
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
	// Clean Blastp file header
	string header = "qseqid sseqid qstart qend qlen sstart send slen pident evalue";
	// Evalue threshold
	double evalueLimit = 10;
	// Percentage of identity threshold
	float pidentLimit = 30;
	// Minimum mutual coverage between two sequences
	unsigned short int minCov = 80;
	// mutual cov
	unsigned short int mutual = 1;
	// Number of CPU(s)
	unsigned int nCpu = 1;
	// Verbose mode
	unsigned short int verbose = 1;
	// Output pidentOut
	unsigned short int pidentOut = 0;
	// Check cmd line 
	if( argc == 1 || argc < 7 || argc > 21 )
	{
		cout << endl;
		cout << "Usage : " << argv[0] << " -i blastp.out.cleanNetwork -n blastp.out.cleanNetwork.genes -m [cc or families] " << endl << endl;
		cout << "-- optional -- " << endl << endl;
		cout << "-e evalue_limit " << endl;
		cout << "-d outDir " << endl;
		cout << "-p pident_limit " << endl;
		cout << "-o pidentOut " << endl;
		cout << "-c min_cov " << endl;
		cout << "-r mutual_cov " << endl;
		cout << "-t n_cpu " << endl;
		cout << "-g specific_gene_list " << endl;
		cout << "-v verbose " << endl;
		cout << "-help" << endl << endl;
		cout << "-- Default values --" << endl << endl;
		cout << "evalue_limit : " << evalueLimit << endl;
		cout << "pident_limit : " << pidentLimit << endl;
		cout << "min_cov      : " << minCov << endl;
		cout << "mutual_cov   : " << mutual << endl;
		cout << "n_cpu        : " << nCpu << endl;
		cout << "pidentOut    : " << pidentOut << endl;
		cout << "verbose      : " << verbose << endl << endl;
		exit(1);
	}
	// Time
	time_t start, end;
	int c;
	// Blastp.out file
	string fileIn;
	// Blastp genes list
	string blastpGenesFile;
	// FusedTriplets output file
	string fileOut;
	// output dir
	string outputDir;
	// File containing specific genes to analyse
	string geneList;
	// triplets, fusedtriplets or fusedgenes
	string found;
	// select algorithm
	unsigned short int methodSelected = 0;
	// blastp genes list given
	unsigned short int blastpGenes = 0;
	// Get arguments
	while( (c = getopt (argc, argv, "i:n:m:d:r:e:p:o:c:t:g:v:")) != -1)
	{
		switch(c)
		{
			case 'i':
				fileIn = optarg;
				break;
			case 'n':
				blastpGenesFile = optarg;
				blastpGenes = 1;
				break;
			case 'm':
				found = optarg;
				methodSelected = 1;
				if( found != "cc" && found != "families" )
				{
					cout << "Method option [-m] " << found << " unknown." << endl;
					cout << "Please select one of those : cc or families." << endl;
					exit(1);
				}
				break;
			case 'd':
				outputDir = optarg;
				break;
			case 'e':
				evalueLimit = atof(optarg);
				break;
			case 'p':
				pidentLimit = atof(optarg);
				break;
			case 'o':
				pidentOut = atoi(optarg);
				break;
			case 'c':
				minCov = atoi(optarg);
				break;
			case 'r':
				mutual = atoi(optarg);
				break;
			case 't':
				nCpu = atoi(optarg);
				break;
			case 'g':
				geneList = optarg;
				break;
			case 'v':
				verbose = atoi(optarg);
				break;
			default:
				cout << endl;
				cout << "Usage : " << argv[0] << " -i blastp.out -m [cc or families] " << endl << endl;
				cout << "-- optional -- " << endl << endl;
				cout << "-e evalue_limit " << endl;
				cout << "-d output_dir " << endl;
				cout << "-p pident_limit " << endl;
				cout << "-o pidentOut " << endl;
				cout << "-c min_cov " << endl;
				cout << "-r mutual_cov" << endl;
				cout << "-t n_cpu " << endl;
				cout << "-g specific_gene_list " << endl;
				cout << "-v verbose " << endl;
				cout << "-help" << endl << endl;
				cout << "-- Default values --" << endl << endl;
				cout << "evalue_limit : " << evalueLimit << endl;
				cout << "pident_limit : " << pidentLimit << endl;
				cout << "min_cov      : " << minCov << endl;
				cout << "mutual_cov   : " << mutual << endl;
				cout << "n_cpu        : " << nCpu << endl;
				cout << "pidentOut    : " << pidentOut << endl;
				cout << "verbose      : " << verbose << endl << endl;
				exit(1);
				break;
		}
	}
	if( methodSelected == 0 && blastpGenes == 0 )
	{
		cout << "Please select one of those method : cc or families." << endl;
		cout << "The file containing the list of blastp genes is missing : -n blastp_genes.list" << endl;
		exit(1);
	}
	else if(methodSelected == 0 && blastpGenes == 1 )
	{
		cout << "Please select one of those method : cc or families." << endl;
		exit(1);
	}
	else if( methodSelected == 1 && blastpGenes == 0 )
	{
		cout << "The file containing the list of blastp genes is missing : -n blastp_genes.list" << endl;
		exit(1);
	}
	// input file basename
	string basename = fileIn.substr(fileIn.find_last_of("\\/")+1);
	replace(basename.begin(), basename.end(), '.', '_');
	string folder = basename + "_" + found;
	// Output directory
	string folderTime = asctime(localtime(&Astart));
	replace(folderTime.begin(), folderTime.end(), ' ', '_');
	replace(folderTime.begin(), folderTime.end(), ':', '_');
	folderTime.pop_back();
	if(outputDir == "")
	{
		string outputDir = folder + "_" + folderTime;
	}
	system(("mkdir -p " + outputDir).c_str());
        // Ouput file basename
        fileOut = outputDir + "/" + basename;
	// Print running command line
	if( verbose == 1 )
	{
		cout << "---------- PARAMETERS ----------" << endl;
		cout << "Input        : " << fileIn << endl;
		cout << "Output       : " << outputDir << endl;
		cout << "Compute      : " << found << endl;
		cout << "E-value      : " << evalueLimit << endl;
		cout << "pidentLimit  : " << pidentLimit << endl;
		cout << "pidentOut    : " << pidentOut << endl;
		cout << "MinCov       : " << minCov << endl;
		cout << "MutualCov    : " << mutual << endl;
		cout << "Nb CPUs      : " << nCpu << endl;
		cout << "Verbose      : " << verbose << endl;
		cout << "--------------------------------" << endl << endl;
		//cout << "COMPUTING\tSTART\tEND\tDURATION" << endl;
	}
	// Create all maps and their reference
	// edges[query,subject]:qstart, qenid, sstart, send, evalue and pident
	map<pair<unsigned long long int, unsigned long long int>, edgeValues> edges;
	map<pair<unsigned long long int, unsigned long long int>, edgeValues>& refEdges = edges;
	// all_neighbors[node]: list of all neighbors
	map<unsigned long long int, geneInfo > genes;
	map<unsigned long long int, geneInfo >& refGenes = genes;
	// Check header
	map<string, unsigned short int> positionsList;
	map<string, unsigned short int>& refPositionsList = positionsList;
	// family dectection isVisted
	map<unsigned long long int, bool> isVisited;
	map<unsigned long long int, bool>& refIV = isVisited;
	// for loading network
	map<unsigned long long int, bool> geneIsVisited;
	map<unsigned long long int, bool>& refGIV = geneIsVisited;
	
	// Step 1 : get header position
	positionsList = getPositions(header);
	
	//Step 2 : Initialize isVisited and geneIsVisited
	start = time(NULL);
	if( verbose == 1 )
	{
		cout << "----- GENE LIST INITIALIZATION -----" << endl << endl;
		cout << "START - " << asctime(localtime(&start)) << endl;
	}
	initializeGeneList(blastpGenesFile,refIV,refGIV);
	end = time(NULL);
	if( verbose == 1 )
	{
		cout << "END   - " << asctime(localtime(&end)) << endl;
	}
	
	// Step 3 : Load network
	start = time(NULL);
	if( verbose == 1 )
	{
		cout << "----- NETWORK LOADING -----" << endl << endl;
		cout << "START - " << asctime(localtime(&start)) << endl;
	}
	runLoadNetwork(fileIn, geneList, pidentLimit, evalueLimit, refPositionsList, refEdges, refGenes, refGIV, nCpu, folderTime);
	end = time(NULL);
	if( verbose == 1 )
	{
		cout << "END   - " << asctime(localtime(&end)) << endl;
	}
	duration( start, end, verbose );
	cout << endl;
	if( verbose == 1 )
	{
		cout << "---------- NETWORK INFO ----------" << endl << endl;
		cout << "Number of nodes :\t" << genes.size() << endl << endl;
		cout << "Number of edges :\t" << edges.size() << endl << endl;
		cout << "----------------------------------" << endl << endl;
	}
	// Step 2 : compute composites and compositesFamilies
	if( found == "cc" )
	{
		start = time(NULL);
		if( verbose == 1 )
		{
			cout << "----- COMPUTE CONNECTED COMPONENTS -----" << endl << endl;
			cout << "START - " << asctime(localtime(&start)) << endl;
		}
		dfsCC(refGenes, refEdges, refIV, minCov, mutual, outputDir, verbose, pidentOut);
		end = time(NULL);
		if( verbose == 1 )
		{
			cout << "END   - " << asctime(localtime(&end)) << endl;
		}
		duration( start, end, verbose );
		cout << endl;
	}
	else if ( found == "families" )
	{
		start = time(NULL);
		if( verbose == 1 )
		{
			cout << "----- COMPUTE FAMILIES -----" << endl << endl;
			cout << "START - " << asctime(localtime(&start));
		}
		// Run FusedGenes in MultiThread mode
		computeFamilies(refGenes, refEdges, refIV, minCov, mutual, outputDir, verbose);
		end = time(NULL);
		if( verbose == 1 )
		{
			cout << "END   - " << asctime(localtime(&end));
		}
		duration( start, end, verbose);
	}
	// ALL TIME (end)
	time_t Aend = time(NULL);
	// REAL TIME
	cout << "----- TOTAL COMPUTING TIME -----" << endl;;
	duration( Astart, Aend, verbose);
	cout << endl;
}
//END
