/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of CleanBlast.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "functions.h"
#include <map>
#include <string>
#include <iomanip>
#include <iostream>
#include <cstring>
#include <list>
#include <stdlib.h>
#include <sstream>
#include <algorithm>
#include <fstream>
#include <cfloat>
#include <cstring>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sys/stat.h>
#include <sys/resource.h>
#include <math.h>
#include <set>
#include <vector>

using namespace std;

void createNetwork(string fileIn, string fileOut, float pidentLimit, map<string, unsigned short int>& positionsList, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, map<unsigned long long int, unsigned int>& genes, unsigned short int minCov, unsigned short int mutalCov, unsigned short int numbering, unsigned short int verbose)
{
	// Get headers position value
	// qseqid position
	unsigned short int qseqid_p = positionsList["qseqid"];
	// sseqid position
	unsigned short int sseqid_p = positionsList["sseqid"];
	// pident position
	unsigned short int pident_p = positionsList["pident"];
	// evalue position
	unsigned short int evalue_p = positionsList["evalue"];
	// qstart position
	unsigned short int qstart_p = positionsList["qstart"];
	// qend position
	unsigned short int qend_p = positionsList["qend"];
	// qlen position
	unsigned short int qlen_p = positionsList["qlen"];
	// sstart position
	unsigned short int sstart_p = positionsList["sstart"];
	// send position
	unsigned short int send_p = positionsList["send"];
	// slen position
	unsigned short int slen_p = positionsList["slen"];
	// numbering
	map<string,unsigned long long int> newName;
	unsigned long long int num = 0;
	// Read input file
	ifstream blastp(fileIn.c_str());
	// Check file
	if(!blastp)
	{
		cout << "Can't open file " << fileIn << endl;
	}
	else
	{
		// Read blastp out and create the network
		string hit;
		// Start reading blastp out
		while(getline(blastp,hit))
		{
			// Get hit line
			istringstream hitInfo(hit);
			// Split line and store values into hitValues vector
			vector<string> hitValues;
			copy(istream_iterator<string>(hitInfo),istream_iterator<string>(),back_inserter<vector<string> >(hitValues));
			// Values to keep
			unsigned long long int qseqid, sseqid;
			unsigned short int qstart, qend, qlen, sstart, send, slen;
			float pident;
			long double evalue;
			// Get only the necessary values from the headers
			// Do not keep self hits and hits out of the pident thresholds
			if(numbering != 0)
			{
				if(newName.find(hitValues[qseqid_p]) != newName.end())
				{
					qseqid=newName[hitValues[qseqid_p]];
				}
				else
				{
					num++;
					newName[hitValues[qseqid_p]]=num;
					qseqid=num;
				}
				if(newName.find(hitValues[sseqid_p]) != newName.end())
				{
					sseqid=newName[hitValues[sseqid_p]];
				}
				else
				{
					num++;
					newName[hitValues[sseqid_p]]=num;
					sseqid=num;
				}
			}
			else
			{
				qseqid=atoll(hitValues[qseqid_p].c_str());
				sseqid=atoll(hitValues[sseqid_p].c_str());
			}
			if(qseqid != sseqid and atof(hitValues[pident_p].c_str()) >= pidentLimit)
			{
				// format hits in order to have the smallest sequence id first
				if(qseqid < sseqid)
				{
					qstart = atoi(hitValues[qstart_p].c_str());
					qend = atoi(hitValues[qend_p].c_str());
					qlen = atoi(hitValues[qlen_p].c_str());
					sstart = atoi(hitValues[sstart_p].c_str());
					send = atoi(hitValues[send_p].c_str());
					slen = atoi(hitValues[slen_p].c_str());
					pident = atof(hitValues[pident_p].c_str());
					evalue = atof(hitValues[evalue_p].c_str());
				}
				else if(qseqid > sseqid)
				{
					unsigned long long int tmp = qseqid;
					qseqid = sseqid;
					sseqid = tmp;
                               		qstart = atoi(hitValues[sstart_p].c_str());
                                	qend = atoi(hitValues[send_p].c_str());
					qlen = atoi(hitValues[slen_p].c_str());
                                	sstart = atoi(hitValues[qstart_p].c_str());
                                	send = atoi(hitValues[qend_p].c_str());
					slen = atoi(hitValues[qlen_p].c_str());
                                	pident = atof(hitValues[pident_p].c_str());
                               		evalue = atof(hitValues[evalue_p].c_str());
				}
				//cout << evalue << endl;
				// Free hitValues memory
				hitValues.clear();
				// Check Cov
				unsigned short int hitCov = 0;
				if(checkCoverage(qstart,qend,qlen,sstart,send,slen,minCov,mutalCov))
				{
					hitCov = 1;
				}
				if( hitCov == 1 )
				{
					// Fill up edges map
					if( edges.find(make_pair(qseqid,sseqid)) != edges.end() )
					{
						// Get edge values for qseqid-sseqid hit
						edgeValues oldValues = edges[make_pair(qseqid,sseqid)];
						// Check if current e-value is better than old one.
						if( oldValues.getEvalue() > evalue )
						{
							// Update edgeValues for qseqid-sseqid hit [ keep best hit ]
							edges[make_pair(qseqid,sseqid)] = edgeValues(qstart, qend, sstart, send, pident, evalue);
						}
					}
					else
					{
						// Add new edge
						edges[make_pair(qseqid,sseqid)] = edgeValues(qstart, qend, sstart, send, pident, evalue);
						// qseqid
						genes[qseqid]=qlen;
						genes[sseqid]=slen;
					}
				}
			}
		}
		// OUTPUT EDGES
		ofstream output(fileOut.c_str());
		map<pair<unsigned long long int,unsigned long long int>, edgeValues>::iterator it;
		for(it=edges.begin(); it!=edges.end(); ++it)
		{
			edgeValues edgeInfo = it->second;
			unsigned long long int e1 = it->first.first;
			unsigned long long int e2 = it->first.second;
			//cout << edgeInfo.getEvalue() << endl;
			output << e1 << "\t" << e2 << "\t" << edgeInfo.getQstart() << "\t" << edgeInfo.getQend() << "\t" << genes[e1] <<"\t" << edgeInfo.getSstart() << "\t" << edgeInfo.getSend() << "\t" << genes[e2] << "\t" << setprecision (4) <<  edgeInfo.getPident() << "\t" << edgeInfo.getEvalue() << endl;
		}
		// OUTPUT NODES
		string genesFile = fileOut + ".genes";
		ofstream outputGenes(genesFile.c_str());
		map<unsigned long long int, unsigned int>::iterator g;
		for(g = genes.begin(); g != genes.end(); ++g)
		{
			outputGenes << g->first << endl;
		}
		if(numbering != 0)
		{
			string dicoFile = fileOut + ".dico";
			ofstream outputDico(dicoFile.c_str());
			map<string, unsigned long long int>::iterator n;
			for(n = newName.begin(); n != newName.end(); ++n)
			{
				outputDico << n->first << "\t" << n->second << endl;
			}
		}
		// Print Network information
		if( verbose == 1 )
		{
			cout << "---------- NETWORK INFO ----------" << endl << endl;
			cout << "Number of nodes        :\t" << genes.size() << endl << endl;
			cout << "Number of edges        :\t" << edges.size() << endl << endl;
			cout << "----------------------------------" << endl << endl;
		}
	}
}
//end
