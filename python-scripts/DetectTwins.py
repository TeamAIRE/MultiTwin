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

from igraph import *

##
# Personal libraries 
#

from Utils import *

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-s", "--separator", dest="s",help="Field separator",default="\t")
    parser.add_option("-o", "--outfile", dest="o",help="Give name to outfile")
    parser.add_option("-u", "--unilateral", dest="u" ,help="Only detect twins from one side (1/2/3..) depending on the typeFile supplied (comma-separated)")
    parser.add_option("-t", "--twin-support",dest="t" ,help="Output twinSupport file (format: ID nbTwinNodes nbSupportNodes SupportNodesIDs (tab-separated)")
    parser.add_option("-T", "--Twin-Support",dest="T" ,help="Output twinSupport file (another format: ID TwinNodesIDs (comma-separated) SupportNodesIDs (comma-separated)")
    parser.add_option("-m", "--minimal-support",dest="thr" ,help="Minimal threshold for the size of the twin support", default=1)
    parser.add_option("-M", "--minimal-size",dest="M" ,help="Minimal threshold for the size of the twin", default=1)
    parser.add_option("-n", "--inNodeType", dest="n",help="Input node type file : Original_nodeName -> type of node (in k-partite) -- Syntax : 1/2 or nodeTypeFile",default=2)
    parser.add_option("-c", "--comp",dest="c" ,help="Output comp file for twin and support (ie both twin nodes and nodes in support receive the same component ID)")
    parser.add_option("-d", "--debug",dest="d", action="store_true",help="Debug")
    parser.add_option("-l", "--log", dest="l", help="Specify log file",default=None)
    return parser

def Main(args,options):
    """ Main program """
    ### Argument/options listing
    if options.l:
        try:
            logHandle = open(options.l,"w")
        except TypeError:
            logHandle = options.l
    else:
        logHandle = sys.stderr
    if myModule() == "__main__.py":
        print>> logHandle, "Argument List:",args
        print>> logHandle, "Option Dictionary:",options
    ### Argument processing ========================================
    edgeFile = args[0]
    ## Filename definitions ======================================
    i0 = time.clock()
    inext = i0
    if options.o:
        dictFile = options.o
    else:
        dictFile = edgeFile+".twins"
    sep = options.s
    thr = int(options.thr)
    try:
        k_part = int(options.n)
    except ValueError:
        k_part = options.n
    ## File reading ========================================
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    g = myReadGraph(edgeFile)
    print g.summary()
    id2name = {}
    name2id = {}
    for n in g.vs():
        name = n['name']
        ind = n.index
        id2name[ind] = name
        name2id[name] = ind
    inext = myTimer(i0,"Loading graph",handle=logHandle)
    ## Program body ===========================================
    # Adjacency list computation ------------------------------
    getName = lambda x:id2name[x]
    nodes = None
    if options.u:
        typeSet = set(map(lambda x:int(x),options.u.strip().split(",")))
        typeDict = defaultdict(int)
        if k_part == 2:
            typeDict.update(rawNodeType(edgeFile))
        elif k_part != 1:
            typeDict.update(loadNodeType(k_part))
        nodes = (n.index for n in g.vs() if typeDict[n['name']] in typeSet)
    ADJ = getAdjlist(g,nodes=nodes)
    inext = myTimer(inext,"Computation of adjacency list",handle=logHandle)
    # Twin computation ----------------------------------------
    support,twins = detectRepeated(ADJ,k_init=0,debug=options.d)   # support: groupID -> common_list_of_neighbours; twins: node -> groupID_of_its_twin_class
    inext = myTimer(inext,"Computation of twins",handle=logHandle)
    new_support = dict([(gid,tuple(map(getName,support[gid]))) for gid in support])
    new_twins = dict([(id2name[node],twins[node]) for node in twins])
    support = new_support
    twins = new_twins
    inext = myTimer(inext,"Renumbering of twins",handle=logHandle)
    sniwt = InvertMap(twins)   # groupID -> list_of_twin_nodes
    inext = myTimer(inext,"Computation of twin support",handle=logHandle)
    # Computation of components (twins + support)
    if options.c:
        h = open(options.c,"w")
        for key,val in twins.iteritems():
            outString = str(key)+sep+str(val)
            print>>h, outString
        inext = myTimer(inext,"Writing twins file",handle=logHandle)
        for val,nodes in support.iteritems():
            for node in nodes:
                outString = str(node)+sep+str(val)
                print>>h, outString
        h.close()
        inext = myTimer(inext,"Writing twins component file",handle=logHandle)
    # Computation of twinSupport (twinID twinNb twinSupport)
    if options.t:
        g = open(options.t,"w")
        for i,nodeList in sniwt.iteritems():
            supp = support[i]
            if len(supp) >= thr and len(nodeList) >= int(options.M):   # Threshold for trivial twins (new option 15/12/15)
                vals = [str(i),str(len(nodeList)),str(len(supp))]
                vals.extend(list(map(lambda x:str(x),supp)))
                print>>g,"\t".join(vals)
        g.close()
        inext = myTimer(inext,"Writing twins support file",handle=logHandle)
    # Computation of TwinSupport (twinID twinNodes twinSupport)
    if options.T:
        g = open(options.T,"w")
        for i,nodeList in sniwt.iteritems():
            supp = support[i]
            if len(supp) >= thr and len(nodeList) >= int(options.M):   # Threshold for trivial twins (new option 15/12/15)
                myTwins = ",".join(map(lambda x:str(x),nodeList))
                mySupport = ",".join(map(lambda x:str(x),supp))
                vals = [str(i)]
                vals.extend([myTwins,mySupport])
                print>>g,"\t".join(vals)
        g.close()
        inext = myTimer(inext,"Writing Twins Support file",handle=logHandle)
    outputDict(twins,dictFile,sep=options.s)
    allTwins = len(sniwt.keys())
    t = len([i for (i,v) in sniwt.iteritems() if len(v) == 1])
    try:
        tp = 100*float(t)/float(allTwins)
    except:
        tp = 0
    nt = allTwins - t
    try:
        ntp = 100*float(nt)/float(allTwins)
    except:
        ntp = 0
    print>> logHandle, """Found %s twins, %s trivial twins (%.2f%%) and %s non-trivial twins (%.2f%%)""" % (allTwins,t,tp,nt,ntp)
    ## Ending ======================================================
    prog = myModule()
    if prog == "__main__.py":
        prog = sys.argv[0].split("/")[-1]
    inext = myTimer(inext,prog,handle=logHandle)
    return

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    options, args = parser.parse_args()
    usage = "\nUsage: %s [options] edgeFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 1:
        parser.error(usage)
    Main(args,options)	
