#! /usr/bin/python

# -*-coding: utf-8 -*-

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
import  time
from optparse import OptionParser
import inspect
import math
import random
from subprocess import *
from collections import Counter
from collections import defaultdict

##
# Local and personal libraries
#
from Utils import *

##
# Argument parsing -- from OptionParser module
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-s", "--separator", dest="s", help="Field separator (default '\\t')",default="\t")
    parser.add_option("-o", "--outfile", dest="o", help="Give name to outfile (default edgeFile.out)")
    parser.add_option("-O", "--xml-Output", dest="O",help="Generate XML parsable output description file (no default value)")
    parser.add_option("-a", "--annotation", dest="a", action="store_true",help="Restrict annotation file (speedup expected) -- boolean")
    parser.add_option("-n", "--nodeList", dest="n", help="Optional nodeList")
    parser.add_option("-N", "--nodeType", dest="N", help="Optional nodeType file (value:1 if unipartite, nothing means bipartite, FILE with types in any other case)")
    parser.add_option("-i", "--id", dest="i", help="Key identifier (default 'UniqID')",default="UniqID")
    parser.add_option("-u", "--unilateral", dest="u" ,help="Node types (1/2...)")
    parser.add_option("-T", "--track", dest="T", help="Track empty annotations: STRING will be written as annotation for every entry in graph whose annotation is missing (default 'No Annotation')",default="No Annotation")
    parser.add_option("-E", "--empty", dest="E", action="store_true", help="If activated, does not include missing annotations -- boolean")
    parser.add_option("-x", "--xml-config", dest="x",help="Specify XML configuration file")
    parser.add_option("-X", "--generate-xml-config", dest="X",help="Generate template XML configuration file")
    parser.add_option("-H", "--history", dest="H",help="Use trailFile FILE history to generate XML file")
    parser.add_option("-D", "--display-all", dest="D", action="store_true",help="Display all annotations by default in config file -- boolean")
    # Deprecated options (but still useful to generate the XML config file)
    parser.add_option("-t", "--trail-old", dest="t", help="Optional comma-separated embedded old trail files to include a previous clustering. Syntax: keyForType1:keyForType2:...=TrailFile1,... \nIf omitted, keyForType2 will not be included in the description, as in keyForType1::=trail1, means tripartite but only nodes of type1 considered at this level")
    parser.add_option("-c", "--component", dest="c", help="Optional comma-separated embedded component files. Syntax: keyForType1:keyForType2=compFile")
    parser.add_option("-k", "--keyList", dest="k", help="Optional keyList. Syntax: key1-type1:type2,key2. This means that key1 has a relevance both for type 1 and type2, and key2 for all; default None means no keys asked.",default=None)
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
    edgeFile = args[0]                                                 # the graph : current_ID1   current_ID2
    annotFile = args[1]                                                # the node annotations : nodeID    list_of_attributes. NB: nodeID should be currentID if no trailFile is specified !!!
    ## Filename definitions ======================================
    i0 = time.clock()
    inext = i0
    if options.o:
        outFile = options.o
    else:
        outFile = edgeFile+".out"
    sep = options.s
    if options.E:
        options.T = None
    ## File reading options ========================================
    # Step 1) Store the node type (top(1)/bottom(2) in the bipartite graph), adapted for the k-partite case
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    nodeType = readNodeType(edgeFile,Type=options.N)                   # this step is not REALLY necessary, in the sense that only the values of the nodeType file are used here
    try:
        nodeTypes = list(set(nodeType.values()))                       # likely an overkill, but does not seem to be time-consuming
    except AttributeError:                                             # this is for the unipartite case (or is it?)
        nodeTypes = [1]
    inext = myTimer(inext,"nodeType",handle=logHandle)
    ## Step 2) Read XML configuration file or generate and exit. ++++++++++++++++++++++++++++++++++++++++++++++++++
    if options.x:                                                      # this option gives the name of the config file, and proceeds with the description procedure : to adapt when second block is written.
        configFile = options.x
        trailObjects,compObject,keyDict,selectedKeys,XML = readConfigFile(configFile)       
        printDescription(trailObjects,compObject,keyDict,selectedKeys,handle=sys.stderr)
    else:                                                              # this block will generate the config file and stop: we start with this part.
        if options.X:                                                  # options.X is the name of the configurationFile that will be generated (default = "config.xml")
            outConf = options.X
        else:                           
            outConf = "config.xml"
        ## selectedKeys are obtained as header of the annotFile
        if options.k:
            keyDict = processOptions(options.k,nodeTypes)
        else:
            selectedKeys = getHeader(annotFile).keys()
            selectedKeys.remove(options.i)
            keyDict = dict()
            for n in nodeTypes:
                keyDict[n] = selectedKeys
        trailObjects = []
        compObject = None
        if options.c:
            compObject = myMod(fileName=options.c,attDict={0:"Module"})
        if options.H:                                                  # added option to generate complete trailHistory in the XML file : options.H is the main trailFile (from rootDir to cwDir)
            history = trailTrack(options.H)
            k = 1
            for trailName in history:
                trailKeyDict = dict([(i,"NodeType"+str(i)) for i in nodeTypes])
                Trail = myTrail(fileName=trailName,rank=k,attDict=trailKeyDict)
                trailObjects.append(Trail)
                k += 1
        configFile = generateXML(nodeTypes,trailObjects=trailObjects,compObject=compObject,attDict=keyDict,outFile=options.X,display=options.D)
        if myModule() == "__main__.py":
            print>> logHandle, "Configured file %s: please check options, and pass it with -x option" % outConf
        return
    ## Step 3) Define nodeLists of currentID and UniqID. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if options.N == '2':
        nodes = nodeType.keys()
    elif options.N == '1':
        nodes = readNodes(edgeFile,sep=sep)
        nodeType = initDict(nodes,value=1)
    else:
        nodes = readNodes(edgeFile,sep=sep)
    if options.n:                                                      # if we explicitly give a file with the currentID to restrict to.
        nodeFile = options.n
        nodes = file2set(nodeFile)                                     # nodes is actually a list (but without repetitions)!
        inext = myTimer(inext,"nodeFile",handle=logHandle)
    if options.u:
        nTypes = set(options.u.strip().split(","))
        nodes = (node for node in nodes if nodeType[node] in nTypes)
    print >> logHandle, """Loaded %d nodes""" % len(nodes)
    # Selected UniqIDs: ========
    if trailObjects:
        trailObjects[-1].getDict()                                     # here the dictionaries of the main trail file are loaded.
        current2UniqID = trailObjects[-1].dict_inv
        myEntries = unList(map(lambda x:current2UniqID[x],nodes))
    else:
        myEntries = nodes
        current2UniqID = None
    print >> logHandle, """Found %d entries""" % len(myEntries)
    inext = myTimer(inext,"allEntries",handle=logHandle)
    # Annotation file processing: ==========
    if options.a:
        annotationDict,fields = restrictAnnot(annotFile,mainKey=str(options.i),valueKeyList=selectedKeys)
    else:
        annotationDict,fields = myLoadAnnotations(annotFile,mainKey=str(options.i),valueKeyList=selectedKeys,counter=0)
    inext = myTimer(inext,"Annotations",handle=logHandle)
    ## Step 4) Construct the actual description. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OutFile = options.O
    xmlDescription(annot=annotationDict,nodeDict=current2UniqID,entries=myEntries,compObject=compObject,trails=trailObjects,nodeType=nodeType,keyDict=keyDict,xmlOutFile=OutFile,outFile=outFile,track=options.T,X=XML,handle=logHandle)
    if options.O:
        print >> logHandle, "XML output written to %s" % OutFile
    else:
        print >> logHandle, "Description written to %s" % outFile
    inext = myTimer(inext,"Description",handle=logHandle)
    ## Output and exit ======================================================
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
    usage = "\nUsage: %s [options] edgeFile annotFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 2:
        parser.error(usage)
    Main(args,options)	
