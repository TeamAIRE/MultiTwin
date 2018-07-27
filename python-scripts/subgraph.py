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
    parser = argparse.ArgumentParser(description='Computes subgraph')
    parser.add_argument("inEdgeFile", help="Input graph edge file",type=str)
    parser.add_argument("outEdgeFile", help="Output graph edge file",type=str)
    parser.add_argument("-n", "--nodes", dest="n",help="Give file containing subnodes")
    parser.add_argument("-N", "--Nodes", dest="N",help="Give list of comma-separated subnodes")
    parser.add_argument("-c", "--component", dest="c",help="Outputs subgraph corresponding to component COMP in compFile FILE (given as a pair FILE,COMP)")
    parser.add_argument("-t", "--type", dest="t",help="specify type of subgraph on nodes (0:incident,1:induced,-1:remove)",default=1)
    parser.add_argument("-s", "--separator", dest="s",help="Field separator",default="\t")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    return(parser)

def Main(edgeFile=None,outEdgeFile=None,nodeFile=None,nodeList=None,comp=None,subType=None,sep=None,log=None):
    """ Main program """
    i0 = time.clock()
    inext = i0
    ### Argument processing ========================================
    ## Filename definitions ======================================
    i0 = time.clock()
    ## Lecture des fichiers ========================================  
    if nodeFile:
        subnodes = ut.file2list(nodeFile)
    elif nodeList:
        subnodes = nodeList.strip().split(",")
    elif comp:
        compFile,compID = comp.strip().split(",")
        subnodes = ut.getNodes(compFile,compID)
    else:
        subnodes = None
    ## Corps du programme =========================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file
    ut.inducedSubgraph(edgeFile,subnodes=subnodes,nodeType=subType,outFile=outEdgeFile,sep=sep)
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
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    args = parser.parse_args()
    header = " ".join(sys.argv)
    printLog(header,args.l,mode="w")
    print(vars(args))
    Main(edgeFile=args.inEdgeFile,outEdgeFile=args.outEdgeFile,nodeFile=args.n,nodeList=args.N,comp=args.c,subType=args.t,sep=args.s,log=args.l)
