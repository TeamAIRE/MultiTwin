#! /usr/bin/python3

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of multitwin.
        
        multitwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

##
# standard libraries -- with Python >= 3.5
#

import sys
import time
import random
from subprocess import Popen
import argparse

##
# python-igraph library import 
#

import igraph

##
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog

##
# Functions
#

def Clustering(g,method=None,weight=None):
    if method == "fg":
        c = g.community_fastgreedy(weights=weight)
        clustering = c.as_clustering(n=c.optimal_count)
    elif method == "im":
        clustering = g.community_infomap(edge_weights=weight, vertex_weights=None, trials=10)
    elif method == "le":
        clustering = g.community_leading_eigenvector(clusters=None, weights=weight, arpack_options=None)
    elif method == "lp":
        clustering = g.community_label_propagation(weights=weight, initial=None, fixed=None)
    elif method == "ml":
        clustering = g.community_multilevel(weights=weight, return_levels=False)
    elif method == "om":
        clustering = g.community_optimal_modularity()
    elif method == "eb":
        c = g.community_edge_betweenness(clusters=None, directed=True, weights=weight)
        clustering = c.as_clustering(n=c.optimal_count)
    elif method == "sg":
        clustering = g.community_spinglass(weights=weight, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule="config", gamma=1, implementation="orig", lambda_=1)
    elif method == "wt":
        c = g.community_walktrap(weights=weight, steps=4)
        clustering = c.as_clustering(n=c.optimal_count)
    else:
        sys.exit("Wrong option: see -h option")
    return clustering

##
# Main procedure ====================================================
#

MethodString = r"""Clustering method:\n
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
    parser = argparse.ArgumentParser(description='Cluster algorithm wrapper. Outputs a community file.',formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("edgeFile", help="Input graph edge file",type=str)
    parser.add_argument("-o", "--outfile", dest="o",help="Give name to outfile")
    parser.add_argument("-m", "--method", dest="m",help=MethodString,required=True)
    parser.add_argument("-w", "--weight", dest="w", action="store_true",help="Use weights - boolean.")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    return(parser)

##
# Main procedure ====================================================
#


def Main(edgeFile=None,outFile=None,method=None,log=None):
    """ Main program """
    ### Argument/options listing
    i0 = time.clock()
    inext = i0
    ## Lecture des fichiers ========================================
    if not outFile:
        outFile = edgeFile+"_"+method+".comp"
    ## File reading ========================================
    try:
        g = igraph.read(edgeFile, format="ncol", directed=False, names=True)
    except SystemError:
        tag = random.randint(100000,1000000)
        tempFile = edgeFile+"_"+str(tag)+".edges"
        tempCmd = """cut -f1,2,9 %s > %s""" %  (edgeFile,tempFile)
        proc1 = Popen(args=[tempCmd],shell=True,executable = "/bin/bash")
        proc1.communicate()
        g = igraph.read(tempFile, format="ncol", directed=False, names=True)
        rmCmd = """rm %s""" %  tempFile
        proc2 = Popen(args=[rmCmd],shell=True,executable = "/bin/bash")
        proc2.communicate()
    names = g.vs["name"]
    try:
        clustering = Clustering(g,method=method)
    except igraph._igraph.InternalError as e:
        sys.exit(e)
    f = open(outFile,'w')
    for node in g.vs:
        f.write("""%s\t%s\n""" % (names[node.index],clustering.membership[node.index]))
    f.close()
    ## Sortie ======================================================
    inext = myTimer(inext,handle=log)
    ## Ending ==============================================================
    prog = myModule()
    if prog == "__main__.py":
        prog = sys.argv[0].split("/")[-1]
    inext = myTimer(i0,"Total computing time for %s" % prog,handle=log)
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
    args = parser.parse_args()
    header = " ".join(sys.argv)
    printLog(header,args.l,mode="w")
    print(vars(args))
    Main(edgeFile=args.edgeFile,outFile=args.o,method=args.m,log=args.l)

