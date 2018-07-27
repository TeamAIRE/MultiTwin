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

##
# Local and personal libraries
#

import utils as ut
from utils import myModule,myTimer,printLog
import xmlform
import ds_launcher

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Outputs description files based on an annotation file for a trail history hierarchy of graphs.')
    parser.add_argument("-i","--input_edge_file", dest="i", help="Final edge file of graph",type=str)
    parser.add_argument("-a-","--annotation_file", dest="a",help="Annotation file (relative to ROOT graph)")
    parser.add_argument("-k", "--keyList", dest="k", help="Optional keyList",default=None)
    parser.add_argument("-x", "--configuration_file_use", dest="x",help="Specify XML configuration file and run")
    parser.add_argument("-K", "--update_xml_config", dest="K",action="store_true",help="Launch graphic interface with specified XML configure file (as indicated by -x option) -- boolean")
    parser.add_argument("-X", "--configuration_file_generate", dest="X",help="Generate template XML configuration file")
    parser.add_argument("-t", "--use_trail_file_unique_level", dest="t", help="Specify trail file")
    parser.add_argument("-H", "--use_trail_file_follow_history", dest="H",help="Use trailFile FILE history to generate XML file")
    parser.add_argument("-c", "--component_file", dest="c", help="Specify component file")
    parser.add_argument("-N", "--partiteness", dest="N", help="Optional nodeType file (value:1 if unipartite, nothing means bipartite, FILE with types in any other case)")
    parser.add_argument("-o", "--output_plain_file", dest="o", help="Give name to outfile (default edgeFile.desc)")
    parser.add_argument("-O", "--output_xml_file", dest="O",help="Generate XML parsable output description file (no default value)")
    parser.add_argument("-I", "--unique_node_identifier", dest="I", help="Key identifier (default 'UniqID')",default="UniqID")
    parser.add_argument("-T", "--track", dest="T", help="Track empty annotations: STRING will be written as annotation for every entry in graph whose annotation is missing (default 'No Annotation')",default="No Annotation")
    parser.add_argument("-E", "--empty", dest="E", action="store_true", help="If activated, does not include missing annotations -- boolean")
    parser.add_argument("-A", "--restrict_annotation", dest="A", action="store_true",help="Restrict annotation file (speedup expected) -- boolean")
    parser.add_argument("-G", "--graphical", dest="G", action="store_true", help="Launch graphical interface")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    parser.add_argument("-s", "--separator", dest="s", help="Field separator (default '\\t')",default="\t")
    parser.add_argument("-n", "--nodeList", dest="n", help="Optional nodeList")
    parser.add_argument("-u", "--unilateral", dest="u" ,help="Node types (1/2...)")
    parser.add_argument("-D", "--display-all", dest="D", action="store_true",help="Display all annotations by default in config file -- boolean")
    return(parser)

def Main(edgeFile=None,annotFile=None,sep=None,outFile=None,Xout=None,restrAnnot=None,nodeList=None,NodeType=None,nodeID=None,unilat=None,track=None,empty=None,\
         x=None,X=None,K=None,hist=None,display=None,trail=None,comp=None,keyList=None,log=None):
    """ Main program """
    ### Argument/options listing
    startWD = os.getcwd()
    if log != sys.stderr:
        try:
            log = os.path.join(startWD,log)
        except TypeError:
            log = sys.stderr
    ### Argument processing ========================================
    ## Filename definitions ======================================
    i0 = time.clock()
    inext = i0
    if not outFile:
        inRad = edgeFile.split(".")[0]
        outFile = inRad+".desc"
    if empty:
        track = None
    ## File reading options ========================================
    # Step 1) Store the node type (top(1)/bottom(2) in the bipartite graph), adapted for the k-partite case
    if not os.stat(edgeFile).st_size:
        if myModule() == "__main__.py":
            sys.exit("Error: Empty file %s" % edgeFile)
        else:
            raise IOError("Empty file %s" % edgeFile)
    nodeType = ut.readNodeType(edgeFile,Type=NodeType)                   # this step is not REALLY necessary, in the sense that only the values of the nodeType file are used here
    try:
        nodeTypes = list(set(nodeType.values()))                       # likely an overkill, but does not seem to be time-consuming
    except AttributeError:                                             # this is for the unipartite case (or is it?)
        nodeTypes = [1]
    inext = myTimer(inext,"Reading nodeType",handle=log)
    ## Step 2) Read XML configuration file or generate and exit. ++++++++++++++++++++++++++++++++++++++++++++++++++
    # a) set variables.
    if keyList:
        keyDict = ut.processOptions(keyList,nodeTypes)
    else:
        selectedKeys = list(ut.getHeader(annotFile).keys())
        selectedKeys.remove(nodeID)
        keyDict = dict()
        for n in nodeTypes:
            keyDict[n] = selectedKeys
    trailObjects = []
    compObject = None
    root = os.getcwd()
    if comp:
        compObject = ut.myMod(fileName=comp,attDict={0:"Module"})
    if hist:                                                  # added option to generate complete trailHistory in the XML file : options.H is the main trailFile (from rootDir to cwDir)
        history = ut.trailTrack(hist)
        root = ut.trailHist(hist)['root']
        k = 1
        for trailName in history:
            trailKeyDict = dict([(i,"NodeType"+str(i)) for i in nodeTypes])
            Trail = ut.myTrail(fileName=trailName,rank=k,attDict=trailKeyDict)
            trailObjects.append(Trail)
            k += 1
    if x:                                                      # this option gives the name of the config file, and proceeds with the description procedure
        configFile = x
        if X:                                                  # options.X is the name of the configurationFile that will be generated (default = "config.xml")
            if x == X:
                configFile = ut.generateXML(nodeTypes,trailObjects=trailObjects,compObject=compObject,attDict=keyDict,outFile=X,display=display,root=root)
            else:
                sys.exit("Conflicting fields -x and -X. Check and run again.")
        if K:
            ret = xmlform.main(xmlFile=configFile)
            if ret == "Cancel":
                sys.exit(0)
        trailObjects,compObject,keyDict,selectedKeys,XML = ut.readConfigFile(configFile)       
        ut.printDescription(trailObjects,compObject,keyDict,selectedKeys,handle=sys.stderr)
    else:                                                              # this block will generate the config file and stop: we start with this part.
        if X:                                                  # options.X is the name of the configurationFile that will be generated (default = "config.xml")
            outConf = X
        else:                           
            outConf = "config.xml"
        ## selectedKeys are obtained as header of the annotFile
        configFile = ut.generateXML(nodeTypes,trailObjects=trailObjects,compObject=compObject,attDict=keyDict,outFile=outConf,display=display,root=root)
        #configFile = generateXML(nodeTypes,trailObjects=trailObjects,compObject=compObject,attDict=keyDict,outFile=X,display=display)
        if myModule() == "__main__.py":
            printLog("Configured file %s: please check options, and pass it with -x option" % outConf,log)
        return()
    ## Step 3) Define nodeLists of currentID and UniqID. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if NodeType == '2':
        nodes = nodeType.keys()
    elif NodeType == '1':
        nodes = ut.readNodes(edgeFile,sep=sep)
        nodeType = ut.initDict(nodes,value=1)
    else:
        nodes = ut.readNodes(edgeFile,sep=sep)
    if nodeList:                                                      # if we explicitly give a file with the currentID to restrict to.
        nodeFile = options.n
        nodes = ut.file2set(nodeFile)                                     # nodes is actually a list (but without repetitions)!
        inext = myTimer(inext,"Reading nodeFile",handle=log)
    if unilat:
        nTypes = set(unilat.strip().split(","))
        nodes = (node for node in nodes if nodeType[node] in nTypes)
    printLog("""Loaded %d nodes""" % len(nodes),log)
    # Selected UniqIDs: ========
    if trailObjects:
        trailObjects[-1].getDict()                                     # here the dictionaries of the main trail file are loaded.
        current2UniqID = trailObjects[-1].dict_inv
        myEntries = ut.unList(map(lambda x:current2UniqID[x],nodes))
    else:
        myEntries = nodes
        current2UniqID = None
    printLog("""Found %d entries""" % len(myEntries),log)
    inext = myTimer(inext,"Reading allEntries",handle=log)
    # Annotation file processing: ==========
    if restrAnnot:
        annotationDict,fields = ut.restrictAnnot(annotFile,mainKey=str(nodeID),valueKeyList=selectedKeys)
    else:
        annotationDict,fields = ut.myLoadAnnotations(annotFile,mainKey=str(nodeID),valueKeyList=selectedKeys,counter=0)
    inext = myTimer(inext,"Reading annotations",handle=log)
    ## Step 4) Construct the actual description. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    OutFile = Xout
    ut.xmlDescription(annot=annotationDict,nodeDict=current2UniqID,entries=myEntries,compObject=compObject,trails=trailObjects,nodeType=nodeType,keyDict=keyDict,xmlOutFile=OutFile,outFile=outFile,track=track,X=XML,handle=log)
    if Xout:
        printLog("XML output written to %s" % OutFile,log)
    else:
        printLog("Description written to %s" % outFile,log)
    ## Output and exit ======================================================
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
    CMD = " ".join(sys.argv)
    printLog(CMD,args.l,mode="w")
    print(vars(args))
    if not args.G:
        Main(edgeFile=args.i,annotFile=args.a,sep=args.s,outFile=args.o,Xout=args.O,restrAnnot=args.A,nodeList=args.n,NodeType=args.N,\
             nodeID=args.I,unilat=args.u,track=args.T,empty=args.E,x=args.x,X=args.X,K=args.K,hist=args.H,display=args.D,trail=args.t,comp=args.c,keyList=args.k,log=args.l)
    else:
        ds_launcher.main(prog,args)


