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
import inspect
import math
import random
from subprocess import *
from optparse import OptionParser
from collections import Counter
from collections import defaultdict

##
# local personal libraries

from Utils import *

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="d",help="Subdirectory where results will be saved",default=None)
    parser.add_option("-c", "--community", dest="c",help="Input community cluster file for the graph factoring")
    parser.add_option("-f", "--community-fasta", dest="f",help="Input community cluster file in FASTA format for the graph factoring")
    parser.add_option("-C", "--community-ID", dest="C", action="store_true",help="Keep the identifiers from the community file -- requires -c option, otherwise silently ignored",default=False)
    parser.add_option("-a", "--attribute-file", dest="a", help="Give attribute FILE")
    parser.add_option("-A", "--output-attribute-File", dest="A",help="Give FILE name to new attributeFile")
    parser.add_option("-k", "--keep", dest="k", help="Keep the original_id as a newAttribute with name NAME")
    parser.add_option("-t", "--trailing", dest="t",help="Input trailing file : Original_nodeName -> current_nodeName")
    parser.add_option("-n", "--inNodeType", dest="n",help="Input node type file : Original_nodeName -> type of node (in k-partite)")
    parser.add_option("-N", "--outNodeType", dest="N",help="Output node type file : New_nodeName -> type of node (in k-partite)")
    parser.add_option("-w", "--weight", dest="w", action="store_true",help="Use weights (BOOLEAN) -- modifies the output edgeFile as node1  node2  mean_weight   std_weight",default=False)
    parser.add_option("-s", "--separator", dest="s",help="Field separator",default="\t")
    parser.add_option("-l", "--log", dest="l", help="Specify log file",default=None)
    return parser

def Main(args,options,header=None):
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
    ### Argument processing =========================================
    edgeFile = args[0] # a filename with the list of edges
    outEdgeFile = args[1]   # the name for the new list of edges
    outTrailFile = args[2]  # the name for the trailing file
    ### Option processing ===========================================
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    if options.d:                                   # Out_directory processing
        directory = os.path.join(os.getcwd(),options.d)
        if not os.path.exists(directory):
            os.makedirs(directory)
    else:
        directory = os.getcwd()
    if options.c:                                   # clustering option
        communityFile = options.c                   # a filename with the attribution of community for each node
    if options.a:                                   # annotation options
        annotFile = options.a                       # the annotation file for the old nodeNames
        if options.A:                               # the annotation file for the new nodeNames  --> if options.c, we must decide on a way to attribute the new annotation (consensus, majority rule, list?...)
            newAnnotFile = os.path.join(directory,options.A)          
        else:
            newAnnotFile = os.path.join(directory,os.path.basename(options.a)+".new")
    ## Filename definitions ========================================
    i0 = time.clock()
    inext = i0
    outFile = os.path.join(directory,outEdgeFile)
    outDict = os.path.join(directory,outTrailFile)
    ## File reading options ======================================== 
    # Read the clustering file
    if options.c:                                   # this part tackles the case of the explicitly redefined nodes -- there may be some missing nodes that will be treated later
        newNodes,community_size = node2community(communityFile,sep=options.s,ID=options.C)
        inext = myTimer(inext,"Community reading",handle=logHandle)
    elif options.f:
        newNodes,community_size = node2communityFasta(options.f,sep=options.s)
    else:                                           # otherwise, all nodes are missing nodes, and appear in the completion process below
        newNodes = None
    ## Body ======================================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file
    if options.w:
        newDictionary,edges_dict,edges_std = network2communityNetwork_Weights(edgeFile,dictionary=newNodes,output_filename=outFile,sep=options.s)
        inext = myTimer(inext,"Community construction",handle=logHandle)
        outputEdgesDict_Weights(edges_dict,edges_std=edges_std,output_filename=outFile,sep=options.s)
    else:
        newDictionary,edges_dict = network2communityNetwork_NoWeights(edgeFile,dictionary=newNodes,output_filename=outFile,sep=options.s)
        inext = myTimer(inext,"Community construction",handle=logHandle)
        outputEdgesDict_NoWeights(edges_dict,output_filename=outFile,sep=options.s)
    inext = myTimer(inext,"New graph writing",handle=logHandle)
    ## Output options ======================================================
    if options.t:
        outputTrailFile(newDictionary,options.t,outfile=outDict,sep=options.s,header=header)
    else:
        outputFile(newDictionary,outfile=outDict,sep=options.s,header=header)
    inext = myTimer(inext,"TrailFile writing",handle=logHandle)
    if options.n:
        if options.N:
            outType = os.path.join(directory,options.N)
        else:
            outType = os.path.join(directory,output_network+".type")
        outputTypeFile(newDictionary,options.n,outfile=outType,sep=options.s)
        inext = myTimer(inext,"TypeFile writing",handle=logHandle)
    if options.a:
        transferAnnotations(annotFile,newAnnotFile,newDictionary,keep=options.k)
    ## Ending ==============================================================
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
    usage = "\nUsage: %s [options] inNetworkFile outNetworkFile outTrailingFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 3:
        parser.error(usage)
    option_dict = vars(options)
    header = printCmd(prog,args,option_dict)
    Main(args,options,header=header)	

