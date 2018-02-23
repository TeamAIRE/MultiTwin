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
from collections import Counter
from Utils import *

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-d", "--degree", dest="d",help="Ceiling value for degree", default=1)
    parser.add_option("-u", "--type", dest="u",help="Type of node if bipartite")
    parser.add_option("-s", "--separator", dest="s",help="Field separator",default="\t")
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
    edgeFile = args[0] # a filename with the list of edges
    outFile = args[1]   # the name for the new list of edges
    ### Option processing
    d = int(options.d)
    ## Filename definitions ======================================
    i0 = time.clock()
    inext = i0
    ## Lecture des fichiers ========================================
    h2t,t2h = adjacencyList(edgeFile)
    if options.u == '1':  
        #print "Right side only"
        adj = h2t
    elif options.u == '2':
        #print "Left side only"
        adj = t2h
    else:
        #print "Both sides"
        adj = h2t
        adj.update(t2h)
    subnodes = [i for (i,v) in adj.iteritems() if len(v)<=d]
    options.t = -1
    ## Corps du programme =========================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file
    inducedSubgraph(edgeFile,subnodes,options,output_filename=outFile,sep=options.s)
    ## Sortie ======================================================
    print>> logHandle, "Removed %s nodes" % len(subnodes)
    ## Fin ==============    
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
    usage = "\nUsage: %s [options] in_networkFile out_subnetworkFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 2:
        parser.error(usage)
    Main(args,options)	
