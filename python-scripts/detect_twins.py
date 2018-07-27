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
import os
import time
import argparse
from collections import defaultdict

##
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog
import dt_launcher

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Computes twin classes of nodes in graph')
    parser.add_argument("-i", "--input_edge_file", help="Input graph edge file",type=str)
    parser.add_argument("-o", "--output_twin_file", dest="o",help="Give name to outfile",type=str)
    parser.add_argument("-c", "--twin_component_file",dest="c" ,help="Output comp file for twin and support (ie both twin nodes and nodes in support receive the same component ID)",type=str)
    parser.add_argument("-n", "--partiteness", dest="n",help="Input node type file : Original_nodeName -> type of node (in k-partite) -- Syntax : 1/2 or nodeTypeFile",default=2)
    parser.add_argument("-u", "--restrict_to_node_types", dest="u" ,help="Only detect twins from one side (1/2/3..) depending on the typeFile supplied (comma-separated)")
    parser.add_argument("-m", "--minimum_support",dest="thr" ,help="Minimal threshold for the size of the twin support", default=1,type=int)
    parser.add_argument("-M", "--minimum_twin_size",dest="M" ,help="Minimal threshold for the size of the twin", default=1,type=int)
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    parser.add_argument("-G", "--graphical", dest="G", action="store_true", help="Launch graphical interface")
    parser.add_argument("-s", "--separator", dest="s",help="Field separator",default="\t")
    parser.add_argument("-t", "--twin-support",dest="t" ,help="Output twinSupport file (format: ID nbTwinNodes nbSupportNodes SupportNodesIDs (tab-separated)",type=str)
    parser.add_argument("-T", "--Twin-Support",dest="T" ,help="Output twinSupport file (another format: ID TwinNodesIDs (comma-separated) SupportNodesIDs (comma-separated)",type=str)
    parser.add_argument("-d", "--debug",dest="d", action="store_true",help="Debug")
    return(parser)

def Main(edgeFile=None,outFile=None,sep=None,unilat=None,twin_supp=None,Twin_Supp=None,min_supp=None,min_size=None,nodeType=None,comp=None,debug=None,log=None):
    """ Main program """
    i0 = time.clock()
    inext = i0
    ## File reading options ========================================
    if not outFile:
        outFile = edgeFile+".twins"
    thr = min_supp
    try:
        k_part = int(nodeType)
    except (TypeError,ValueError):
        k_part = nodeType
    ## File reading ========================================
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    g = ut.myReadGraph(edgeFile)
    print(g.summary())
    id2name = {}
    name2id = {}
    for n in g.vs():
        name = n['name']
        ind = n.index
        id2name[ind] = name
        name2id[name] = ind
    inext = myTimer(i0,"Loading graph",handle=log)
    ## Program body ===========================================
    # Adjacency list computation ------------------------------
    getName = lambda x:id2name[x]
    nodes = None
    if unilat:
        typeSet = set(map(lambda x:int(x),unilat.strip().split(",")))
        typeDict = defaultdict(int)
        if k_part == 2 or not k_part:
            typeDict.update(ut.rawNodeType(edgeFile))
        elif k_part != 1:
            typeDict.update(ut.loadNodeType(k_part))
        nodes = (n.index for n in g.vs() if typeDict[n['name']] in typeSet)
    ADJ = ut.getAdjlist(g,nodes=nodes)
    inext = myTimer(inext,"Computation of adjacency list",handle=log)
    # Twin computation ----------------------------------------
    support,twins = ut.detectRepeated(ADJ,k_init=0,debug=debug)   # support: groupID -> common_list_of_neighbours; twins: node -> groupID_of_its_twin_class
    inext = myTimer(inext,"Computation of twins",handle=log)
    new_support = dict([(gid,tuple(map(getName,support[gid]))) for gid in support])
    new_twins = dict([(id2name[node],twins[node]) for node in twins])
    support = new_support
    twins = new_twins
    inext = myTimer(inext,"Renumbering of twins",handle=log)
    sniwt = ut.InvertMap(twins)   # groupID -> list_of_twin_nodes
    inext = myTimer(inext,"Computation of twin support",handle=log)
    # Computation of components (twins + support)
    if comp:
        with open(comp,'w') as h:
            for key,val in iter(twins.items()):
                outString = str(key)+sep+str(val)+"\n"
                h.write(outString)
            inext = myTimer(inext,"Writing twins file",handle=log)
            for val,nodes in iter(support.items()):
                for node in nodes:
                    outString = str(node)+sep+str(val)+"\n"
                    h.write(outString)
            inext = myTimer(inext,"Writing twins component file",handle=log)
    # Computation of twinSupport (twinID twinNb twinSupport)
    if twin_supp:
        with open(twin_supp,'w') as g:
            for i,nodeList in iter(sniwt.items()):
                supp = support[i]
                if len(supp) >= thr and len(nodeList) >= min_size:   # Threshold for trivial twins (new option 15/12/15)
                    vals = [str(i),str(len(nodeList)),str(len(supp))]
                    vals.extend(list(map(lambda x:str(x),supp)))
                    g.write("\t".join(vals)+"\n")
        inext = myTimer(inext,"Writing twins support file",handle=log)
    # Computation of TwinSupport (twinID twinNodes twinSupport)
    if Twin_Supp:
        with open(Twin_Supp,'w') as g:
            for i,nodeList in iter(sniwt.items()):
                supp = support[i]
                if len(supp) >= thr and len(nodeList) >= min_size:   # Threshold for trivial twins (new option 15/12/15)
                    myTwins = ",".join(map(lambda x:str(x),nodeList))
                    mySupport = ",".join(map(lambda x:str(x),supp))
                    vals = [str(i)]
                    vals.extend(list(map(lambda x:str(x),supp)))
                    g.write("\t".join(vals)+"\n")
        inext = myTimer(inext,"Writing Twins Support file",handle=log)
    ut.outputDict(twins,outFile,sep=sep)
    allTwins = len(sniwt.keys())
    t = len([i for (i,v) in iter(sniwt.items()) if len(v) == 1])
    try:
        tp = 100*float(t)/float(allTwins)
    except:
        tp = 0
    nt = allTwins - t
    try:
        ntp = 100*float(nt)/float(allTwins)
    except:
        ntp = 0
    printLog("""Found %s twins, %s trivial twins (%.2f%%) and %s non-trivial twins (%.2f%%)""" % (allTwins,t,tp,nt,ntp),log)
    ## Ending ======================================================
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
    if not args.G:
        Main(edgeFile=args.input_edge_file,outFile=args.o,sep=args.s,unilat=args.u,twin_supp=args.t,Twin_Supp=args.T,min_supp=args.thr,min_size=args.M,nodeType=args.n,comp=args.c,debug=args.d,log=args.l)
    else:
        dt_launcher.main(prog,args)
