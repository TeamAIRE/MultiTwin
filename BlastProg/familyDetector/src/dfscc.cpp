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
#include <set>
#include <stdlib.h>
#include <sstream>
#include <algorithm>
#include <fstream>
#include <vector>
#include <iomanip>

using namespace std;

// Composites Families detection algo

void dfsCC( map<unsigned long long int, geneInfo>& genes, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, map<unsigned long long int, bool>& isVisited, unsigned short int minCov, unsigned short int mutual, string outputDir, unsigned short int verbose, unsigned short int pidentOut)
{
	// Number of connected components
	unsigned long long int nCC = 0;
	// cc info file
	string fileOutCCinfo = outputDir + "/CC.info";
	ofstream outputCCinfo(fileOutCCinfo.c_str());
	outputCCinfo << "#CCid\tnodes\tedges" << endl;
	// nodes file
	string fileOutCCnodes = outputDir + "/CC.nodes";
	ofstream outputCCnodes(fileOutCCnodes.c_str());
	// edges file
	string fileOutCCedges = outputDir + "/CC.edges";
	ofstream outputCCedges(fileOutCCedges.c_str());
        // Compute connected components
	map<unsigned long long int, geneInfo>::iterator it;
	for( it = genes.begin(); it != genes.end(); it++)
	{
		// Check if node has been visited, if true go to next one
		if(isVisited[it->first] == true ) continue;
		// Start
		// cc family number
		nCC++;
		outputCCnodes << ">CC" << nCC << endl;
		outputCCedges << ">CC" << nCC << endl;
		// count cc edges
		unsigned long long int NbEdges = 0;
		// count cc nodes
		unsigned long long int NbNodes = 0;
		// Temporary list containing nodes belonging to CC
		set<unsigned long long int> tmpNodes;
		set<unsigned long long int>::iterator val;
		// Insert CC starting node
		tmpNodes.insert(it->first);
		// Get CC until tmpNodes is not empty
		while(!tmpNodes.empty())
		{
			// Get node
			val = tmpNodes.begin();
			unsigned long long int node = *val;
			// Delete node from tmpNodes
			tmpNodes.erase(val);
			// If not visited check node
			unsigned long long int i;
			if( isVisited[node] == false )
			{
				// Change node status to visited
				isVisited[node] = true;
				NbNodes++;
				outputCCnodes << node << endl;
				// Current node's neighnors
				vector<unsigned long long int> currentNodeNeighbors = genes[node].getNeighbors();
				while(!currentNodeNeighbors.empty())
				{
					// Get neighbor
					unsigned long long int neighbor = currentNodeNeighbors.back();
					currentNodeNeighbors.pop_back();
					// Check neighbor's status
					if(isVisited[neighbor] == false)
					{
						if(checkCoverage(node, neighbor, minCov, genes, edges, mutual))
						{
							// Add neighbor to tmpNodes
							tmpNodes.insert(neighbor);
							// count edge
							NbEdges++;
							if(pidentOut == 1)
							{
								float pident = getEdgeValues(edges,node,neighbor).getPident();
								outputCCedges << node << "\t" << neighbor << "\t" << pident << endl;
							}
							else
							{
								outputCCedges << node << "\t" << neighbor << endl;
							}
						}
					}
				}
			}
		}
		// output info
		outputCCinfo << nCC << "\t" << NbNodes << "\t" << NbEdges << endl;
	}
	// Clear isVisted map container
	isVisited.clear();
	if(verbose == 1)
	{
		cout << "Nb of CC : " << nCC << endl;
	}
}
//end
