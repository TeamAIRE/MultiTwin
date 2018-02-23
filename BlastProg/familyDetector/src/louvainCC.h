/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#ifndef LOUVAINCC_H_INCLUDED
#define LOUVAINCC_H_INCLUDED

#include "functions.h"
#include <map>
#include <string>
#include <list>
#include <set>
#include <vector>
#include <iostream>

// used for Composites' Families algo

unsigned int louvainCC( std::vector<unsigned long long int>& nodes, std::map<unsigned long long int, unsigned long long int>& realName, std::map<unsigned long long int, geneInfo>& genes, std::map<std::pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, unsigned short int minCov, unsigned short int mutual, unsigned long long int nCCdfs, std::ofstream& outputCCinfo, std::ofstream& outputCCnodes, std::ofstream& outputCCedges, std::map<unsigned long long int, unsigned long long int>& nodesCCID);
#endif // LOUVAINCC_H_INCLUDED
