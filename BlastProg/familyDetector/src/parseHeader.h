/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/
#ifndef PARSEHEADER_H_INCLUDED
#define PARSEHEADER_H_INCLUDED

#include <string>
#include <map>

std::map<std::string, unsigned short int> getPositions(std::string header);

#endif // PARSEHEADER_H_INCLUDED
