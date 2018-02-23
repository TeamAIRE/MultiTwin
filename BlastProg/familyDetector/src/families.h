/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#ifndef FAMILIES_H_INCLUDED
#define FAMILIES_H_INCLUDED

#include "functions.h"
#include <map>
#include <string>
#include <list>
#include <set>
#include <vector>
#include <iostream>

// used for Composites' Families algo
void computeFamilies( std::map<unsigned long long int, geneInfo>& genes, std::map<std::pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, std::map<unsigned long long int, bool>& isVisited, unsigned short int minCov, unsigned short int mutual, std::string outputDir, unsigned short int verbose);
#endif // FAMILIES_H_INCLUDED
