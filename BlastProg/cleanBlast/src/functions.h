/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of CleanBlast.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#ifndef FUNCTIONS_H_INCLUDED
#define FUNCTIONS_H_INCLUDED

#include <map>
#include <string>
#include <list>
#include <set>
#include <vector>
#include <iostream>

// EDGES	

class edgeValues
{
	public:
		edgeValues();
		edgeValues(unsigned short int qstart, unsigned short int qend, unsigned short int sstart, unsigned short int send, float pident, long double evalue);
		// Set values for the edge
		void setQstart(unsigned short int);
		void setQend(unsigned short int);
		void setSstart(unsigned short int);
		void setSend(unsigned short int);
		void setPident(float);
		void setEvalue(long double);
		// Get values 
		unsigned short int getQstart();
		unsigned short int getQend();
		unsigned short int getSstart();
		unsigned short int getSend();
		float getPident();
		long double getEvalue();
	private:
		// Query
		unsigned short int m_qstart;
		unsigned short int m_qend;
		// Subject
		unsigned short int m_sstart;
		unsigned short int m_send;
		// Hits values
		float m_pident;
		long double m_evalue;
};

bool checkCoverage(unsigned int qstart, unsigned int qend, unsigned int qlen, unsigned int sstart,unsigned int send,unsigned int slen, unsigned short int minCov, unsigned short int mutual);
#endif // FUNCTIONS_H_INCLUDED
