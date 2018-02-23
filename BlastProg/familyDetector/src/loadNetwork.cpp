/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "functions.h"
#include <map>
#include <string>
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
#include <thread>
#include <mutex>

using namespace std;

std::mutex mtx;

void loadNetwork(string fileIn, string geneList, float pidentLimit, double evalueLimit, map<string, unsigned short int>& positionsList, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, map<unsigned long long int, geneInfo>& genes, map<unsigned long long int, bool>& geneIsVisited, unsigned int l)
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
	// Read input file
	ifstream blastp(fileIn.c_str());
	// Gene list to check
	vector<unsigned long long int> genesToCheck;
	vector<unsigned long long int>& refgenesToCheck = genesToCheck;
	// local edges
	map<pair<unsigned long long int, unsigned long long int>, edgeValues> localEdges;
	// local length
	map<unsigned long long int, geneInfo> localGenes;
	// Check file
	if(!blastp)
	{
		cout << "Can't open file " << fileIn << "cpu " << l << endl;
	}
	else
	{
		// Store into a vector the specific genes to check
		if( geneList != "" )
		{
			ifstream genes(geneList.c_str());
			string gene;
			while(getline(genes,gene))
			{
				genesToCheck.push_back(atoll(gene.c_str()));
			}
			sort(genesToCheck.begin(),genesToCheck.end());
		}
		// Read blastp out and create the network
		string hit;
		// Network's edge number
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
			double evalue;
			// flag keep (1) or not (0)
			unsigned short int keep = 1;
			// Get only the necessary values from the headers
			// Do not keep self hits and hits out of the pident thresholds
			if(atof(hitValues[pident_p].c_str()) < pidentLimit or atof(hitValues[evalue_p].c_str()) > evalueLimit)
			{
				keep = 0;
			}
			if(geneList != "")
			{
				// Check if qseqid and sseqid are in the specific genes list
				if(not FoundIn(atoll(hitValues[qseqid_p].c_str()), refgenesToCheck) or not FoundIn(atoll(hitValues[sseqid_p].c_str()), refgenesToCheck))
				{
					keep = 0;
				}
			}
			//cout << hit << endl;
			//cout << keep << endl;
			// keep hit
			if(keep == 1)
			{
				qseqid = atoll(hitValues[qseqid_p].c_str());
				sseqid = atoll(hitValues[sseqid_p].c_str());
				qstart = atoi(hitValues[qstart_p].c_str());
				qend = atoi(hitValues[qend_p].c_str());
				qlen = atoi(hitValues[qlen_p].c_str());
				sstart = atoi(hitValues[sstart_p].c_str());
				send = atoi(hitValues[send_p].c_str());
				slen = atoi(hitValues[slen_p].c_str());
				pident = atof(hitValues[pident_p].c_str());
				evalue = atof(hitValues[evalue_p].c_str());
				// Free hitValues memory
				hitValues.clear();
				// Add new edge
				localEdges[make_pair(qseqid,sseqid)] = edgeValues(qstart, qend, sstart, send, pident, evalue);
				localGenes[qseqid] = geneInfo(qlen);
				localGenes[sseqid] = geneInfo(slen);
			}
		}
	}
	mtx.lock();
	//cout << "Thread " << l << " --> lines: " << count << " edges: " << localEdges.size() << endl;
	//map<pair<unsigned int,unsigned int>, edgeValues>::iterator it = localEdges.begin();
	while(!localEdges.empty())
	{
		edges[localEdges.begin()->first] = localEdges.begin()->second;
		// node 1
		if(geneIsVisited[localEdges.begin()->first.first] == true)
		{
			genes[localEdges.begin()->first.first].insertNeighbor(localEdges.begin()->first.second);
		}
		else
		{
			genes[localEdges.begin()->first.first] = localGenes[localEdges.begin()->first.first];
			genes[localEdges.begin()->first.first].insertNeighbor(localEdges.begin()->first.second);
			geneIsVisited[localEdges.begin()->first.first]=true;
		}
		// node 2
		if(geneIsVisited[localEdges.begin()->first.second] == true)
		{
			genes[localEdges.begin()->first.second].insertNeighbor(localEdges.begin()->first.first);
		}
		else
		{
			genes[localEdges.begin()->first.second] = localGenes[localEdges.begin()->first.second];
			genes[localEdges.begin()->first.second].insertNeighbor(localEdges.begin()->first.first);
			geneIsVisited[localEdges.begin()->first.second]=true;
		}
		//it++;
		localEdges.erase(localEdges.begin());
	}
	localEdges.clear();
	localGenes.clear();
	//cout << "current Total edges: " << edges.size() << endl;
	//cout << "current Total nodes: " << all_neighbors.size() << endl;
	//cout << "Thread\t" << l << "\t[Done]" << endl;
	mtx.unlock();
}


// Load Network (MultiThread)

void runLoadNetwork( string fileIn, string geneList, float pidentLimit, double evalueLimit, map<string, unsigned short int>& positionsList, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, map<unsigned long long int, geneInfo >& genes, map<unsigned long long int, bool>& geneIsVisited, unsigned int nCpu, string timeInfo)
{
	// split network
	if( nCpu > 1 )
	{
		// Split file into N parts where N = nCpu
		string splitCmd = "split -d -n l/" + to_string(nCpu) + ' ' + fileIn;
		system((splitCmd).c_str());
		// Rename splited files
		string modNameCmd = "for i in $(ls x*); do N=$(($N+1)); mv $i $N.familyDetectorLoadNetwork_"+ timeInfo +"; done";
		system((modNameCmd).c_str());
	}
	else
	{
		// create link
		system(("ln -s " + fileIn + " 1.familyDetectorLoadNetwork_" + timeInfo ).c_str());
	}
	// Multithreading
	vector<thread> threads;
	for(unsigned int i = 1; i < nCpu+1; ++i)
	{
		string subNetwork = to_string(i) + ".familyDetectorLoadNetwork_" + timeInfo;
		threads.push_back(thread(loadNetwork, subNetwork, geneList, pidentLimit, evalueLimit, std::ref(positionsList), std::ref(edges), std::ref(genes), std::ref(geneIsVisited),i));
	}
	for(auto& thread : threads)
	{
		thread.join();
	}
	// Delete subnetworks
	system(("rm *.familyDetectorLoadNetwork_" + timeInfo).c_str());
}

// Initialize gene list
void initializeGeneList(string blastpGenesFile, map<unsigned long long int, bool>& isVisited, map<unsigned long long int, bool>& geneIsVisited)
{
	ifstream geneList(blastpGenesFile.c_str());
	if(!geneList)
	{
		cout << "Can't open file " << blastpGenesFile << endl;
	}
	else
	{
		string gene;
		while(getline(geneList,gene))
		{
			isVisited[atoll(gene.c_str())]=false;
			geneIsVisited[atoll(gene.c_str())]=false;
		}
	}
}
//end
