/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of FamilyDetector.
        
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

// Genes
class geneInfo
{
	public:
		geneInfo();
		geneInfo(unsigned int length);
		// Set or insert values
		void setLength(unsigned int);
		void insertNeighbor(unsigned long long int);
		// Get values
		unsigned int getLength();
		std::vector<unsigned long long int> getNeighbors();
	private:
		unsigned int m_length;
		std::vector<unsigned long long int> m_neighbors;
};

// EDGES	

class edgeValues
{
	public:
		edgeValues();
		edgeValues(unsigned short int qstart, unsigned short int qend, unsigned short int sstart, unsigned short int send, float pident, double evalue);
		// Set values for the edge
		void setQstart(unsigned short int);
		void setQend(unsigned short int);
		void setSstart(unsigned short int);
		void setSend(unsigned short int);
		void setPident(float);
		void setEvalue(double);
		// Get values 
		unsigned short int getQstart();
		unsigned short int getQend();
		unsigned short int getSstart();
		unsigned short int getSend();
		float getPident();
		double getEvalue();
	private:
		// Query
		unsigned short int m_qstart;
		unsigned short int m_qend;
		// Subject
		unsigned short int m_sstart;
		unsigned short int m_send;
		// Hits values
		float m_pident;
		double m_evalue;
};

edgeValues getEdgeValues(std::map<std::pair<unsigned long long int,unsigned long long int>, edgeValues> &edges, unsigned long long int a, unsigned long long int b);

edgeValues reverseEdgeValues(edgeValues edge);

bool FoundIn(unsigned long long int value, std::vector<unsigned long long int>& List);

bool checkCoverage(unsigned long long int node1, unsigned long long int node2, unsigned short int minCov, std::map<unsigned long long int, geneInfo>& genes, std::map<std::pair<unsigned long long int, unsigned long long int>, edgeValues>& edges, unsigned short int mutual);

#endif // FUNCTIONS_H_INCLUDED
