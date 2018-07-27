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
import argparse

##
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Removes degree one nodes from graph')
    parser.add_argument("inEdgeFile", help="Input graph edge file",type=str)
    parser.add_argument("outEdgeFile", help="Output graph edge file",type=str)
    parser.add_argument("-d", "--degree", dest="d",help="Ceiling value for degree", default=1)
    parser.add_argument("-u", "--type", dest="u",help="Type of node if bipartite",type=int)
    parser.add_argument("-s", "--separator", dest="s",help="Field separator",default="\t")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    return(parser)

def Main(edgeFile=None,outEdgeFile=None,degree=None,nodeType=None,sep=None,log=None):
    """ Main program """
    ### Argument/options listing
    d = int(degree)
    i0 = time.clock()
    inext = i0
    ## Lecture des fichiers ========================================
    h2t,t2h = ut.adjacencyList(edgeFile)
    if nodeType == 1:  
        adj = h2t
    elif nodeType == 2:
        adj = t2h
    else:
        adj = h2t
        adj.update(t2h)
    subnodes = [i for (i,v) in iter(adj.items()) if len(v)<=d]
    nodeType = -1
    ## Corps du programme =========================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file
    ut.inducedSubgraph(edgeFile,subnodes,nodeType=nodeType,outFile=outEdgeFile,sep=sep)
    ## Sortie ======================================================
    inext = myTimer(inext,"Removed %s nodes" % len(subnodes),handle=log)
    ## Ending ==============================================================
    prog = myModule()
    if prog == "__main__.py":
        prog = sys.argv[0].split("/")[-1]
    inext = myTimer(i0,"Total computing time for %s" % prog,handle=log)
    return

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    args = parser.parse_args()
    header = " ".join(sys.argv)
    printLog(header,args.l,mode="w")
    print(vars(args))
    Main(edgeFile=args.inEdgeFile,outEdgeFile=args.outEdgeFile,degree=args.d,nodeType=args.u,sep=args.s,log=args.l)

