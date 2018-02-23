#! /usr/bin/python

# -*- coding: utf-8 -*-

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of MultiTwin.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

##
# standard libraries -- with Python v2.4 or higher
#

import re
import sys
import os
import itertools
import time
from optparse import OptionParser
import inspect
import math
import random
from subprocess import *
from collections import defaultdict
from collections import Counter

##
# python-igraph library import 
#

import igraph

##
# Personal import
#

from Utils import myTimer

##
# Functions
#

def Clustering(g,method=None):
    if method == "fg":
        c = g.community_fastgreedy(weights=None)
        clustering = c.as_clustering(n=c.optimal_count)
    elif method == "im":
        clustering = g.community_infomap(edge_weights=None, vertex_weights=None, trials=10)
    elif method == "le":
        clustering = g.community_leading_eigenvector(clusters=None, weights=None, arpack_options=None)
    elif method == "lp":
        clustering = g.community_label_propagation(weights=None, initial=None, fixed=None)
    elif method == "ml":
        clustering = g.community_multilevel(weights=None, return_levels=False)
    elif method == "om":
        clustering = g.community_optimal_modularity()
    elif method == "eb":
        c = g.community_edge_betweenness(clusters=None, directed=True, weights=None)
        clustering = c.as_clustering(n=c.optimal_count)
    elif method == "sg":
        clustering = g.community_spinglass(weights=None, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule="config", gamma=1, implementation="orig", lambda_=1)
    elif method == "wt":
        c = g.community_walktrap( weights=None, steps=4)
        clustering = c.as_clustering(n=c.optimal_count)
    else:
        sys.exit("Wrong option: see -h option")
    return clustering

##
# Main procedure ====================================================
#

MethodString = """Clustering method:
'fg': community_fastgreedy(self, weights=None)
Community structure based on the greedy optimization of modularity.
\n  	
'im': community_infomap(self, edge_weights=None, vertex_weights=None, trials=10)
Finds the community structure of the network according to the Infomap method of Martin Rosvall and Carl T.
\n	
'le': community_leading_eigenvector(clusters=None, weights=None, arpack_options=None)
Newman's leading eigenvector method for detecting community structure.
\n	
'lp': community_label_propagation(weights=None, initial=None, fixed=None)
Finds the community structure of the graph according to the label propagation method of Raghavan et al.
\n	
'ml': community_multilevel(self, weights=None, return_levels=False)
Community structure based on the multilevel algorithm of Blondel et al.
\n	
'om': community_optimal_modularity(self, *args, **kwds)
Calculates the optimal modularity score of the graph and the corresponding community structure.
\n	
'eb': community_edge_betweenness(self, clusters=None, directed=True, weights=None)
Community structure based on the betweenness of the edges in the network.
\n	
'sg': community_spinglass(weights=None, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule='config', gamma=1, implementation='orig', lambda_=1)
Finds the community structure of the graph according to the spinglass community detection method of Reichardt & Bornholdt.
\n	
'wt': community_walktrap(self, weights=None, steps=4)
Community detection algorithm of Latapy & Pons, based on random walks.
"""

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-o", "--outfile", dest="o",help="Give name to outfile")
    parser.add_option("-m", "--method", dest="m",help=MethodString)
    return parser

def Main(args,options):
    """ Main program """
    print args,options
    ### Argument processing ========================================
    edgeFile = args[0]
    ## Filename definitions ======================================
    i0 = time.clock()
    if options.o:
        outFile = options.o
    else:
        outFile = edgeFile+"_"+options.m+".comp"
    ## File reading ========================================
    g = igraph.read(edgeFile, format="ncol", directed=False, names=True)
    names = g.vs["name"]
    clustering = Clustering(g,method=options.m)
    f = open(outFile,'w')
    for node in g.vs:
        print>>f, """%s\t%s""" % (names[node.index],clustering.membership[node.index])
    f.close()
    ## Ending ======================================================
    myTimer(i0)
    return

#========= Main program

if __name__ == '__main__':
    MethodString = """Clustering method (-m METHOD):
'fg': community_fastgreedy(self, weights=None)
\tCommunity structure based on the greedy optimization of modularity.
'im': community_infomap(self, edge_weights=None, vertex_weights=None, trials=10)F
\tFinds the community structure of the network according to the Infomap method of Martin Rosvall and Carl T.
'le': community_leading_eigenvector(clusters=None, weights=None, arpack_options=None)
\tNewman's leading eigenvector method for detecting community structure.
'lp': community_label_propagation(weights=None, initial=None, fixed=None)
\tFinds the community structure of the graph according to the label propagation method of Raghavan et al.
'ml': community_multilevel(self, weights=None, return_levels=False)
\tCommunity structure based on the multilevel algorithm of Blondel et al.
'om': community_optimal_modularity(self, *args, **kwds)
\tCalculates the optimal modularity score of the graph and the corresponding community structure.
'eb': community_edge_betweenness(self, clusters=None, directed=True, weights=None)
\tCommunity structure based on the betweenness of the edges in the network.
'sg': community_spinglass(weights=None, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule='config', gamma=1, implementation='orig', lambda_=1)
\tFinds the community structure of the graph according to the spinglass community detection method of Reichardt & Bornholdt.
'wt': community_walktrap(self, weights=None, steps=4)
\tCommunity detection algorithm of Latapy & Pons, based on random walks.
"""
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    options, args = parser.parse_args()
    usage = "\nUsage: %s [options] edgeFile; \nTry %s -h for details\n%s" % (prog,prog,MethodString)
    if len(args) < 1:
        parser.error(usage)
    Main(args,options)	
