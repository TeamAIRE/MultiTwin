/*

        Written by Jananan PATHMANATHAN, 2014-2018
        
        This file is part of CleanBlast.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/

*/

#include "functions.h"
#include <iostream>
#include <map>
#include <list>
#include <vector>
#include <math.h>
#include <algorithm>
#include <cmath>

using namespace std;

// Class edgeValues
edgeValues::edgeValues() : m_qstart(0), m_qend(0), m_sstart(0), m_send(0), m_pident(0), m_evalue(0)
{

}

edgeValues::edgeValues(unsigned short int qstart, unsigned short int qend, unsigned short int sstart, unsigned short int send, float pident, long double evalue) : m_qstart(qstart), m_qend(qend), m_sstart(sstart), m_send(send), m_pident(pident), m_evalue(evalue)
{

}

void edgeValues::setQstart(unsigned short int qstart)
{
	m_qstart = qstart;
}

void edgeValues::setQend(unsigned short int qend)
{
	m_qend = qend;
}

void edgeValues::setSstart(unsigned short int sstart)
{
	m_sstart = sstart;
}

void edgeValues::setSend(unsigned short int send)
{
	m_send = send;
}

void edgeValues::setPident(float pident)
{
        m_pident = pident;
}

void edgeValues::setEvalue(long double evalue)
{
	m_evalue = evalue;
}

unsigned short int edgeValues::getQstart()
{
	return m_qstart;
}

unsigned short int edgeValues::getQend()
{
	return m_qend;
}

unsigned short int edgeValues::getSstart()
{
	return m_sstart;
}

unsigned short int edgeValues::getSend()
{
	return m_send;
}

float edgeValues::getPident()
{
        return m_pident;
}

long double edgeValues::getEvalue()
{
	return m_evalue;
}


bool checkCoverage(unsigned int qstart, unsigned int qend, unsigned int qlen, unsigned int sstart,unsigned int send,unsigned int slen, unsigned short int minCov, unsigned short int mutual)
{
        // Query coverage
        unsigned short int qcov = floor((((float)qend-(float)qstart+1.0)*100.0)/(float)qlen);
        // Subject coverage
        unsigned short int scov = floor((((float)send-(float)sstart+1.0)*100.0)/(float)slen);
        // Return true if both cov are higher or equal to the minimum coverage value 
        // fixed by the user or the default one (0%)
        if( (qcov >= minCov and scov >= minCov) and mutual == 1 )
        {
                return true;
        }
        else if( (qcov >= minCov or scov >= minCov) and mutual == 0 )
        {
                return true;
        }
        else
        {
                return false;
        }
}




//END
