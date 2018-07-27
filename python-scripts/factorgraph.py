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

import re
import sys
import time
import os
import itertools
import math
import argparse
from collections import Counter, defaultdict

##
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog
import fg_launcher

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Factors a graph as communities')
    parser.add_argument("-i", "--input_edge_file", help="Input graph edge file",type=str)
    parser.add_argument("-o", "--output_edge_file", help="Output graph edge file",type=str)
    parser.add_argument("-T", "--output_trail_file", help="Output trailing file",type=str)
    parser.add_argument("-d", "--output_directory", dest="d",help="Subdirectory where results will be saved",default=None)
    parser.add_argument("-c", "--community_file", dest="c",help="Input community cluster file for the graph factoring")
    parser.add_argument("-f", "--community_file-fasta", dest="f",help="Input community cluster file in FASTA format for the graph factoring")
    parser.add_argument("-C", "--keep_community_IDs", dest="C", action="store_true",help="Keep the identifiers from the community file -- requires -c option, otherwise silently ignored",default=False)
    parser.add_argument("-t", "--input_trail_file", dest="t",help="Input trailing file : Original_nodeName -> current_nodeName")
    parser.add_argument("-n", "--input_node_type_file", dest="n",help="Input node type file : Original_nodeName -> type of node (in k-partite)")
    parser.add_argument("-N", "--output_node_type_file", dest="N",help="Output node type file : New_nodeName -> type of node (in k-partite)")
    parser.add_argument("-w", "--use_weights", dest="w", action="store_true",help="Use weights (BOOLEAN) -- modifies the output edgeFile as node1  node2  mean_weight   std_weight",default=False)
    parser.add_argument("-l", "--log_file", dest="l", help="Specify log file",default=sys.stderr)
    parser.add_argument("-G", "--graphical", dest="G", action="store_true", help="Launch graphical interface")
    parser.add_argument("-s", "--separator", dest="s",help="Field separator",default="\t")
    return(parser)

def Main(edgeFile=None,outEdgeFile=None,outTrailFile=None,direct=None,community=None,comm_fasta=None,comm_id=None,in_trail=None,inType=None,outType=None,sep=None,weight=None,log=None,header=None):
    """ Main program """
    ### Argument/options listing
    if not outEdgeFile:
        outEdgeFile = edgeFile+".out"
    if not outTrailFile:
        outTrailFile = edgeFile+".trail"
    ### Option processing ===========================================
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    if direct:                                   # Out_directory processing
        directory = os.path.join(os.getcwd(),direct)
        if not os.path.exists(directory):
            os.makedirs(directory)
    else:
        directory = os.getcwd()
    if community:                                   # clustering option
        communityFile = community                   # a filename with the attribution of community for each node
    ## Filename definitions ======================================== 
    i0 = time.clock()
    inext = i0
    outFile = os.path.join(directory,outEdgeFile)
    outDict = os.path.join(directory,outTrailFile)
    ## File reading options ======================================== 
    # Read the clustering file and attribute a community identifier to nodes
    if community:                                   # this part tackles the case of the explicitly redefined nodes -- there may be some missing nodes that will be treated later
        newNodes = ut.node2community(communityFile,sep=sep,ID=comm_id)
        inext = myTimer(inext,"Community reading",handle=log)
    elif comm_fasta:
        newNodes = ut.node2communityFasta(comm_fasta,sep=sep)
    else:                                           # otherwise, all nodes are missing nodes, and appear in the completion process below
        newNodes = None
    ## Body ======================================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file.
    newDictionary,edges_dict,edges_std = ut.network2communityNetwork(edgeFile,dictionary=newNodes,sep=sep,useWeights=True)
    inext = myTimer(inext,"Community construction",handle=log)
    if weight:
        ut.outputEdgesDict_Weights(edges_dict,edges_std=edges_std,outFile=outFile,sep=sep)
    else:
        ut.outputEdgesDict_NoWeights(edges_dict,outFile=outFile,sep=sep)
    inext = myTimer(inext,"New graph writing",handle=log)
    ## Output options ======================================================
    if in_trail:
        ut.outputTrailFile(newDictionary,in_trail,outfile=outDict,sep=sep,header=header)
    else:
        ut.outputFile(newDictionary,outfile=outDict,sep=sep,header=header)
    inext = myTimer(inext,"TrailFile writing",handle=log)
    if inType:
        if outType:
            outType = os.path.join(directory,outType)
        else:
            outType = os.path.join(directory,output_network+".type")
        ut.outputTypeFile(newDictionary,inType,outfile=outType,sep=sep)
        inext = myTimer(inext,"TypeFile writing",handle=log)
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
    args.header = header
    print(vars(args))
    if not args.G:
        Main(edgeFile=args.input_edge_file,outEdgeFile=args.output_edge_file,outTrailFile=args.output_trail_file,direct=args.d,community=args.c,\
         comm_fasta=args.f,comm_id=args.C,in_trail=args.t,inType=args.n,outType=args.N,sep=args.s,weight=args.w,log=args.l,header=header)
    else:
        fg_launcher.main(prog,args)
