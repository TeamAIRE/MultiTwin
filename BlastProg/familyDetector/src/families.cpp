/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "functions.h"
#include "louvainCC.h"
#include <igraph.h>
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

void computeFamilies( map<unsigned long long int, geneInfo>& genes, map<pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, map<unsigned long long int, bool>& isVisited, unsigned short int minCov, unsigned short int mutual, string outputDir, unsigned short int verbose)
{
	// Louvain
	map<unsigned long long int, bool> inLouvain;
	// Number of connected components
	unsigned long long int nCC = 0;
	// family info file
	string fileOutCCinfo = outputDir + "/family.info";
	ofstream outputCCinfo(fileOutCCinfo.c_str());
	outputCCinfo << "#familyID\tnodes\tedges\tconnectivity" << endl;
	// nodes file
	string fileOutCCnodes = outputDir + "/family.nodes";
	ofstream outputCCnodes(fileOutCCnodes.c_str());
	// edges file
	string fileOutCCedges = outputDir + "/family.edges";
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
		// CC nodes list
		vector<unsigned long long int> ccNodes;
		// CC edges
		vector<pair<unsigned long long int,unsigned long long int>> ccEdges;
		// Nb edges for connectivity
		unsigned long long int NbEdges = 0;
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
			inLouvain[node] = false;
			// Delete node from tmpNodes
			tmpNodes.erase(val);
			// If not visited check node
			if( isVisited[node] == false )
			{
				// Change node status to visited
				isVisited[node] = true;
				// Add node to the current CC
				ccNodes.push_back(node);
				NbNodes++;
				// Current node's neighnors
				vector<unsigned long long int > currentNodeNeighbors = genes[node].getNeighbors();
				//for(i = 0; i < currentNodeNeighbors.size(); i++ )
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
							// Count edges
							NbEdges++;
							ccEdges.push_back(make_pair(node,neighbor));
						}
					}
				}
			}
		}
		// Check CC integrity
		if( ccNodes.size() < 3 )
		{
			//info
			outputCCinfo << nCC << "\t" << NbNodes << "\t" << NbEdges << "\t1.00" << endl;
			outputCCnodes << ">F" << nCC << endl;
			while(!ccNodes.empty())
			{
				outputCCnodes << ccNodes.back() << endl;
				ccNodes.pop_back();
			}
			ccNodes.clear();
			//
			outputCCedges << ">F" << nCC << endl;
			while(!ccEdges.empty())
			{
				pair<unsigned long long int, unsigned long long int > e = ccEdges.back();
				outputCCedges << e.first << "\t" << e.second << endl;
				ccEdges.pop_back();
			}
			ccEdges.clear();
		}
		else
		{
			vector<unsigned long long int> nodes;
			vector<unsigned long long int>& refN = nodes;
			unsigned long long int realEdges = 0;
			unsigned long long int goodEdges = 0;
			long long int newName = -1;
			map<unsigned long long int, unsigned long long int> realName;
			map<unsigned long long int, unsigned long long int>& refRN = realName;
			map<unsigned long long int, unsigned long long int> renamedAs;
			// igraph
			igraph_t g;
			igraph_vector_t modularity, membership, tmpEdges;
			igraph_matrix_t memberships;
			igraph_vector_init(&modularity,0);
			igraph_vector_init(&membership,0);
			igraph_matrix_init(&memberships,0,0);
			igraph_vector_init(&tmpEdges,0);
			while( ccNodes.size() > 1 )
			{
				// Get node
				unsigned long long int node = ccNodes.back();
				nodes.push_back(node);
				// Get the list of all neighbors of node
				vector<unsigned long long int> all_node_neighbors = genes[node].getNeighbors();
				vector<unsigned long long int>& refAnn = all_node_neighbors;
				ccNodes.pop_back();
				// Check if node's cc neighbors and mean cov
				vector<unsigned long long int>::iterator i;
				for( i = ccNodes.begin(); i != ccNodes.end(); ++i)
				{
					unsigned long long int neighbor = *i;
					if(FoundIn(neighbor, refAnn))
					{
						realEdges++;
						if( checkCoverage(node, neighbor, minCov, genes, edges, mutual) )
						{
							unsigned long long int n1;
							unsigned long long int n2;
							if(inLouvain[node] == false)
							{
								newName++;
								n1 = newName;
								realName[newName]=node;
								renamedAs[node]=newName;
								inLouvain[node]=true;
							}
							else
							{
								n1 = renamedAs[node];
							}
							if(inLouvain[neighbor] == false)
							{
								newName++;
								n2 = newName;
								realName[newName]=neighbor;
								renamedAs[neighbor]=newName;
								inLouvain[neighbor]=true;
							}
							else
							{
								n2 = renamedAs[neighbor];
							}
							//outputTmpEdges << n1 << "\t" << n2 << endl;
							igraph_vector_push_back(&tmpEdges,n1);
							igraph_vector_push_back(&tmpEdges,n2);
							goodEdges++;
						}
					}
				}
			}
			nodes.push_back(ccNodes.back());
			ccNodes.clear();
			sort(nodes.begin(),nodes.end());
			unsigned short int goodCovPercent = ceil(((float)goodEdges/(float)realEdges)*100.0);
			if( goodCovPercent < 100 )
			{
				ccEdges.clear();
				map<unsigned long long int, unsigned long long int> nodesCCID;
				map<unsigned long long int, unsigned long long int>& refNCCID = nodesCCID;
				// Louvain
				igraph_create(&g, &tmpEdges, nodes.size(), 0);
				igraph_community_multilevel(&g, 0, &membership, &memberships, &modularity);
				long long int i, j, no_of_nodes = igraph_vcount(&g);
				unsigned int level = igraph_matrix_nrow(&memberships) - 1;
				for(j=0; j < no_of_nodes; j++)
				{
					unsigned long long int goodName = realName[j];
					nodesCCID[goodName]=(long long int)MATRIX(*&memberships, level, j);
				}
				igraph_destroy(&g);
				igraph_vector_destroy(&modularity);
				igraph_vector_destroy(&membership);
				igraph_vector_destroy(&tmpEdges);
				igraph_matrix_destroy(&memberships);
				nCC=louvainCC(refN, refRN, genes, edges, minCov, mutual, nCC, outputCCinfo, outputCCnodes, outputCCedges, refNCCID);
			}
			else
			{
				float connectivity = (2.0*(float)NbEdges)/((float)nodes.size()*((float)nodes.size()-1.0));
				outputCCinfo << nCC << "\t" << NbNodes << "\t" << NbEdges << "\t" << setprecision (2) << fixed << connectivity << endl;
				//
				outputCCnodes << ">F" << nCC << endl;
				while(!nodes.empty())
				{
					outputCCnodes << nodes.back() << endl;
					nodes.pop_back();
				}
				nodes.clear();
				outputCCedges << ">F" << nCC << endl;
				while(!ccEdges.empty())
				{
					pair<unsigned long long int, unsigned long long int> e = ccEdges.back();
					outputCCedges << e.first << "\t" << e.second << endl;
					ccEdges.pop_back();
				}
				ccEdges.clear();
			}
		}
	}
	// Clear isVisted map container
	isVisited.clear();
	if(verbose == 1)
	{
		cout << "Nb Families : " << nCC << endl;
	}
}

//end
