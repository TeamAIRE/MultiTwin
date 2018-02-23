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

import re, sys, os, itertools, time
from optparse import OptionParser
import inspect, math, random
from subprocess import *
from Utils import *
from collections import Counter

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    #parser.add_option("-a", "--anchor-input", dest="anc",help="Optional alternative fragment input file -- in Dialign anchor format")
    parser.add_option("-n", "--nodes", dest="n",help="Give file containing subnodes")
    parser.add_option("-N", "--Nodes", dest="N",help="Give list of comma-separated subnodes")
    parser.add_option("-c", "--component", dest="c",help="Outputs subgraph corresponding to component COMP in compFile FILE (given as a pair FILE,COMP)")
    parser.add_option("-t", "--type", dest="t",help="specify type of subgraph on nodes (0:incident,1:induced,-1:remove)",default=1)
    parser.add_option("-s", "--separator", dest="s",help="Field separator",default="\t")
    return parser

def Main(args,options):
    """ Main program """
    print args,options
    ### Argument processing ========================================
    network_filename = args[0] # a filename with the list of edges
    output_network = args[1]   # the name for the new list of edges
    #output_nodeDict = args[2]  # the name for the trailing file
    ### Option processing
    ## Filename definitions ======================================
    i0 = time.clock()
    ## Lecture des fichiers ========================================  
    if options.n:
        subnodes = file2list(options.n)
    elif options.N:
        subnodes = options.N.strip().split(",")
    elif options.c:
        compFile,compID = options.c.strip().split(",")
        subnodes = getNodes(compFile,compID)
    ## Corps du programme =========================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file
    inducedSubgraph(network_filename,subnodes,options,output_filename=output_network,sep=options.s)
    ## Sortie ======================================================
    ## Fin ==============
    i1 = time.clock()
    t1 = i1-i0
    print "Computation completed in %f seconds" % t1
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
