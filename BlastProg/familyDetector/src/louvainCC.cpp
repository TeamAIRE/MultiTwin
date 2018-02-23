/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#include "functions.h"
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
#include <iomanip>

using namespace std;

// Composites Families detection algo

unsigned int louvainCC( vector<unsigned long long int>& nodes, map<unsigned long long int, unsigned long long int>& realName, map<unsigned long long int, geneInfo>& genes, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, unsigned short int minCov, unsigned short int mutual, unsigned long long int nCCdfs, ofstream& outputCCinfo, ofstream& outputCCnodes, ofstream& outputCCedges, map<unsigned long long int, unsigned long long int>& nodesCCID)
{
	// Map to check if a node was visted or not
	map<unsigned long long int, bool> isVisited;
	// Fill up isVisted and initialize nodes status
	vector<unsigned long long int>::iterator it;
	for( it = nodes.begin(); it != nodes.end(); it++)
	{
		isVisited[*it] = false;
	}
	// Number of connected components
	unsigned long long int nCC;
	if(nCCdfs != 0)
	{
		nCC = nCCdfs-1;
	}
	else
	{
		nCC = nCCdfs;
	}
        // Compute connected components
	for( it = nodes.begin(); it != nodes.end(); it++)
	{
		// Check if node has been visited, if true go to next one
		if(isVisited[*it] == true ) continue;
		// cc family number
		nCC++;
		// output nodes
		outputCCnodes << ">F" << nCC << endl;
		// outptu edges
		outputCCedges << ">F" << nCC << endl;
		// Temporary list containing nodes belonging to CC
		set<unsigned long long int> tmpNodes;
		set<unsigned long long int>::iterator val;
		// edges
		unsigned long long int NbEdges = 0;
		// nodes
		unsigned long long int NbNodes = 0;
		// Insert CC starting node
		tmpNodes.insert(*it);
		// starting node louvain id
		unsigned long long int louvainID = nodesCCID[*it];
		// Get CC until tmpNodes is not empty
		while(!tmpNodes.empty())
		{
			// Get node
			val = tmpNodes.begin();
			unsigned long long int node = *val;
			// Delete node from tmpNodes
			tmpNodes.erase(val);
			// If not visited check node
			if( isVisited[node] == false )
			{
				// Change node status to visited
				isVisited[node] = true;
				NbNodes++;
				//cout << "LOUVAIN " << node << " " << nCC << endl;
				outputCCnodes << node << endl;
				// Current node's neighnors
				vector<unsigned long long int > currentNodeNeighbors = genes[node].getNeighbors();
				while(!currentNodeNeighbors.empty())
				{
					// Get neighbor
					unsigned long long int neighbor = currentNodeNeighbors.back();
					currentNodeNeighbors.pop_back();
					// Check neighbor's status
					if(FoundIn(neighbor,nodes) and checkCoverage(node, neighbor, minCov, genes, edges, mutual))
					{
						if( nodesCCID[neighbor] == louvainID and isVisited[neighbor] == false )
						{
							// Add neighbor to tmpNodes
							tmpNodes.insert(neighbor);
							// edges
							NbEdges++;
							outputCCedges << node << "\t" << neighbor << endl;
						}
					}
				}
			}
		}
		float connectivity = (2.0*(float)NbEdges)/((float)NbNodes*((float)NbNodes-1.0));
		outputCCinfo << nCC << "\t" << NbNodes << "\t" << NbEdges << "\t" << setprecision (2) << fixed << connectivity << endl;
		//cout << "louvain " << nCC << endl;
	}
	// Clea	r isVisted map container
	isVisited.clear();
	nodesCCID.clear();
	realName.clear();
	nodes.clear();
	return nCC;
}
//end
