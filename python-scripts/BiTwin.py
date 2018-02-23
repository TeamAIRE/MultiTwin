#! /usr/bin/python

# -*-coding:utf-8 -*-

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
from igraph import *
from optparse import OptionParser
import subprocess 
from collections import Counter
import multiprocessing 
import FactorGraph as FG
import ShaveGraph as SG
import DetectTwins as DT
import Description as D

##
# Local libraries
#

from Utils import *

##
# Local executable definitions
#

blastAll = "BlastAll.py"
cleanblast = "CleanBlast"
FactorGraph = "FactorGraph.py"
DetectTwins = "DetectTwins.py"
familydetector = "FamilyDetector"
shaveGraph = "ShaveGraph.py"
Description = "Description.py"
transferAnnotations = "TransferAnnotations.py"

##
# Function definitions
#

def runBlast(fastaFile,blastFile):
    i0 = time.clock()
    nbCPU = multiprocessing.cpu_count()
    n = nbCPU-2
    tag = random.randint(100000,1000000)
    dbFile = fastaFile+"_"+str(tag)+".db"
    dbCmd = """makeblastdb -in %s -input_type "fasta" -dbtype prot -out %s -hash_index""" %  (fastaFile,dbFile)
    proc1 = Popen(args=[dbCmd],shell=True,executable = "/bin/bash")
    proc1.communicate()
    blastCmd = """%s -i %s -out %s -db %s -th %d -evalue 1e-5""" % (blastAll,fastaFile,blastFile,dbFile,n)
    proc2 = Popen(args=[blastCmd],shell=True,executable = "/bin/bash")
    proc2.communicate()
    cleanCmd = """rm %s*""" % dbFile
    proc3 = Popen(args=[cleanCmd],shell=True,executable = "/bin/bash")
    proc3.communicate()
    myTimer(i0,"runBlast")

def runDiamond(fastaFile,blastFile):
    i0 = time.clock()
    tag = random.randint(100000,1000000)
    dbRad = fastaFile+"_"+str(tag)
    dbFile = dbRad+".dmnd"
    dbCmd = """diamond makedb --in %s -d %s""" %  (fastaFile,dbRad)
    proc1 = Popen(args=[dbCmd],shell=True,executable = "/bin/bash")
    proc1.communicate()
    diaCmd = """diamond blastp -d %s -q %s -o %s -f 6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen --more-sensitive""" % (dbRad,fastaFile,blastFile)
    proc2 = Popen(args=[diaCmd],shell=True,executable = "/bin/bash")
    proc2.communicate()
    cleanCmd = """rm %s*""" % dbFile
    proc3 = Popen(args=[cleanCmd],shell=True,executable = "/bin/bash")
    proc3.communicate()
    myTimer(i0,"runDiamond")

def runDescription(annotFile,radical=None,ID=None,handle=sys.stderr):
    if not ID:
        ID = "UniqID"
    descFile = radical+".desc"
    xmlFile = radical+".xml_desc"
    configFile = radical+".config"
    trailFile = radical+".trail"
    edgeFile = radical+".edges"
    compFile = radical+".twin_comp"
    cmd8 = """%s -i %s -o %s -X %s -a -D -c %s -H %s %s %s""" % (Description,ID,descFile,configFile,compFile,trailFile,edgeFile,annotFile)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Configuring %s" % cmd8
    args8 = (edgeFile,annotFile)
    parser8 = D.processArgs()
    options8 = parser8.get_default_values()
    options8.i,options8.o,options8.X,options8.a,options8.D,options8.c,options8.H = ID,descFile,configFile,True,True,compFile,trailFile
    options8.l = handle
    try:
        D.Main(args8,options8)
    except IOError as e:
        print>> handle, "Error in %s: %s\nExiting." % (cmd8,e)
        return
    parser8bis = D.processArgs()
    options8bis = parser8bis.get_default_values()
    options8bis.i,options8bis.o,options8bis.O,options8bis.x,options8bis.a,options8bis.H = ID,descFile,xmlFile,configFile,True,trailFile
    cmd8bis = """%s -i %s -o %s -O %s -x %s -a -H %s %s %s""" % (Description,ID,descFile,xmlFile,configFile,trailFile,edgeFile,annotFile)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd8bis
    options8bis.l = handle
    try:
        D.Main(args8,options8bis)
    except IOError as e:
        print>> handle, "Error in %s: %s\nExiting." % (cmd8bis,e)
        return

def getArticulationPoints(edgeFile):
    g = Graph.Read_Ncol(edgeFile,directed=False)
    bic,aps = g.biconnected_components(return_articulation_points=True)
    art = []
    for node in aps:
        art.append(g.vs[node]['name'])
    return art

def completeAnalysis(geneNetwork,genome2sequence,n,c,a=None,options=None,handle=sys.stderr):
    directory = "graphs"+str(n)
    try:
        os.mkdir(directory)
    except OSError:
        pass
    # Names and file definitions ==== To check
    clustType = options.C
    if clustType == 'cc':
        seqCompFile = "CC.nodes"                       # compFile for sequences
    elif clustType == 'families':
        seqCompFile = "family.nodes"                       # compFile for sequences
    else:
        sys.exit("Bad clustering type -- see -C option")
    seqCCFile = "seqFile.cc"                       # CCFile for sequences
    UniqID = str(options.i)
    edgeFile = "graph.edges"                       # edgeFile
    trailFile = "graph.trail"                      # trailFile
    #geneNetworkFiltered = "geneNetwork.blastp"     # trimmed blastp output
    geneNetworkDico = geneNetwork+".dico"
    geneNetworkGenes = geneNetwork+".genes"
    clustType = options.C
    ## ==============================
    # c) assemble sequence families by computing the connected components
    cmd2 = """%s -i %s -d %s -n %s -m %s -p %d""" % (familydetector,geneNetwork,directory,geneNetworkGenes,clustType,n)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd2
    proc2 = Popen(args=[cmd2],shell=True,stdout=PIPE,executable = "/bin/bash")
    out = proc2.communicate()[0]
    print>> handle, out
    #os.chdir(directory)
    mySeqCompFile = os.path.join(directory,seqCompFile)
    # renumber back families through geneNetworkDico
    dic1 = loadMapping(geneNetworkDico)
    dic2 = node2communityFasta(mySeqCompFile,sep=options.s)[0]
    compDict = composeDict(dic1,dic2)
    outputDict(compDict,mySeqCompFile,sep=options.s)
    ## B) from the sequence families to the bipartite graph
    # a) Cluster sequence families and quotient the graph
    args3 = (genome2sequence,edgeFile,trailFile)
    parser3 = FG.processArgs()
    options3 = parser3.get_default_values()
    options3.c,options3.k,options3.d,options3.l = mySeqCompFile,UniqID,directory,handle
    cmd3 = """%s -c %s -k %s -d %s %s %s %s""" % (FactorGraph,mySeqCompFile,UniqID,directory,genome2sequence,edgeFile,trailFile)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd3
    FG.Main(args3,options3)
    os.chdir(directory)
    print >> handle, "--------------------------------------------------"
    print>> handle, "cd %s" % directory
    rad = "graph0"
    # b) Remove the degree one nodes from the sequence side
    edges = rad+".edges"
    comp = rad+".comp"
    cc = rad+".cc"
    args4 = (edgeFile,edges)
    parser4 = SG.processArgs()
    options4 = parser4.get_default_values()
    options4.d,options4.u,options4.l = 1,2,handle
    cmd4 = """%s -d 1 -u 2 %s %s""" % (shaveGraph,edgeFile,edges)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd4
    SG.Main(args4,options4)
    # d) Compute twins and twin supports of the bipartite graph
    twins = rad+".twins"
    twinComp = rad+".twin_comp"
    cmd6 = """%s -o %s -u 2 -c %s %s """ % (DetectTwins,twins,twinComp,edges)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd6
    args6 = (edges,)
    parser6 = DT.processArgs()
    options6 = parser6.get_default_values()
    options6.o,options6.u,options6.c,options6.l = twins,str(2),twinComp,handle
    try:
        DT.Main(args6,options6)
    except IOError as e:
        print>> handle, "Error in %s: %s\nExiting." % (cmd6,e)
        return
    ## C) from the bipartite graph to the twins and articulation points
    # a) twin quotienting
    twinDir = "TwinQuotient"
    try:
        os.mkdir(twinDir)
    except OSError:
        pass
    rad = "graph1"
    newEdges = rad+".edges"
    newTrail = rad+".trail"
    cmd7 = """%s -c %s -k %s -d %s -t %s %s %s %s""" % (FactorGraph,twins,UniqID,twinDir,trailFile,edges,newEdges,newTrail)
    print >> handle, "--------------------------------------------------"
    print>> handle, "Running %s" % cmd7
    args7 = (edges,newEdges,newTrail)
    parser7 = FG.processArgs()
    options7 = parser7.get_default_values()
    options7.c,options7.k,options7.d,options7.t,options7.l = twins,UniqID,twinDir,trailFile,handle
    try:
        FG.Main(args7,options7)
    except IOError as e:
        print>> handle, "Error in %s: %s\nExiting." % (cmd7,e)
        return
    os.chdir(twinDir)
    print >> handle, "--------------------------------------------------"
    print>> handle, "cd %s" % twinDir
    # b) Renumbering and computing articulation points
    ART = getArticulationPoints(newEdges)
    artPoints = rad+".art"
    aP = open(artPoints,"w")
    print >> handle, "--------------------------------------------------"
    print>> handle, "Printing %d articulation points in %s" % (len(ART),artPoints)
    for node in ART:
        print>> aP,node
    aP.close()
    ## D) annotations and component analysis
    if a:
        edges = rad+".edges"
        twins = rad+".twins"
        twinComp = rad+".twin_comp"
        cmd9 = """%s -o %s -u 2 -c %s %s """ % (DetectTwins,twins,twinComp,edges)
        print >> handle, "--------------------------------------------------"
        print>> handle, "Running %s" % cmd9
        args9 = (edges,)
        parser9 = DT.processArgs()
        options9 = parser9.get_default_values()
        options9.o,options9.u,options9.c,options9.l = twins,str(2),twinComp,handle
        try:
            DT.Main(args9,options9)
        except IOError as e:
            print>> handle, "Error in %s: %s\nExiting." % (cmd9,e)
            return
        runDescription(a,radical=rad,ID=UniqID,handle=handle)
    return
  
##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-s", "--separator", dest="s", help="""Field separator (default "\\t")""",default="\t")
    parser.add_option("-n", "--thr", dest="n", help="Threshold(s) for sequence similarity (comma-separated)",default="30,40,50,60,70,80,90,95")
    parser.add_option("-c", "--cover", dest="c", help="Threshold for reciprocal sequence length cover",default=80)
    parser.add_option("-I", "--input-network", dest="I", help="Skips CleanBlast step with supplied networkFile FILE")
    parser.add_option("-f", "--fasta", dest="f", help="Fasta file -- if supplied, then the blast-all will be run first to generate the blastFile. Attention, the supplied blastFile NAME will be used for the output")
    parser.add_option("-A", "--aln", dest="A", help="Use ALN (b=BLAST/d=Diamond) sequence comparison program (only with -f option)",default="b")
    parser.add_option("-C", "--clustering", dest="C", help="Clustering type for family detection (cc or families)",default="cc")
    parser.add_option("-o", "--outfile", dest="o", help="Give NAME to outfile")
    parser.add_option("-a", "--annotation", dest="a", help="Annotation file, referenced by UniqID")
    parser.add_option("-i", "--id", dest="i", help="Key identifier (default: UniqID)",default="UniqID")
    parser.add_option("-k", "--keyList", dest="k", help="Optional list of keys in annotFile to consider (requires option -a -- default All)",default=None)
    parser.add_option("-l", "--log", dest="l", help="Specify log file",default=None)
    return parser

def Main(args,options):
    """ Main program """
    if options.l:
        logHandle = open(options.l,"w")
    else:
        logHandle = sys.stderr
    if myModule() == "__main__.py":
        print>> logHandle, "Argument List:",args
        print>> logHandle, "Option Dictionary:",options
    ###
    startWD = os.getcwd()
    ### Argument processing =============================================================================================================
    blastFile,genome2sequence = args
    if not options.n:
        sys.exit("Sequence identity threshold (option -n) required")
    else:
        ThresholdList = map(lambda x:int(x),options.n.strip().split(","))
    cover = float(options.c)
    if options.f:
        if options.A == "b":
            runBlast(options.f,blastFile)
        elif options.A == "d":
            runDiamond(options.f,blastFile)
        else:
            sys.exit("Wrong sequence comparison option -- use (b) for BLAST - (d) for DIAMOND")
    UniqID = options.i
    ## Filename definitions =============================================================================================================
    if options.I:
        geneNetwork = options.I
    else:
        geneNetwork = blastFile+".cleanNetwork"
    if options.a:
        annot = os.path.join(startWD,options.a)
    else:
        annot = None
    ## Corps du programme ===========================================
    inext = time.clock()
    rootDir = os.getcwd()
    ## A) from the blast output to the sequence families
    # a) filter self-hits and keep only best hit
    if not options.I:
        cmd1 = """%s -n 1 -i %s""" % (cleanblast,blastFile)       # the output are three files named blastFile".cleanNetwork", blastFile".cleanNetwork.dico" and blastFile".cleanNetwork.genes" 
        print >> logHandle, "--------------------------------------------------"
        print>> logHandle, "Running",cmd1
        proc1 = Popen(args=[cmd1],shell=True,stdout=PIPE,executable = "/bin/bash")
        out = proc1.communicate()[0]
        print>> logHandle, out
    # b) filter by thresholds on cover and identity percentage
    thresholdString = ",".join(map(lambda x:str(x),ThresholdList))
    for n in ThresholdList:
        print >> logHandle, """\n%d%% ==================================================""" % n
        completeAnalysis(geneNetwork,genome2sequence,n,cover,a=annot,options=options,handle=logHandle)
        os.chdir(rootDir)
    ## Fin ======================================================
    prog = myModule()
    if prog == "__main__.py":
        prog = sys.argv[0].split("/")[-1]
    inext = myTimer(inext,prog)
    ## Sortie ======================================================
    if options.l:
        logHandle.close()
    return

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    options, args = parser.parse_args()
    usage = "\nUsage: %s [options] blastFile genome2sequenceFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 2:
        parser.error(usage)
    Main(args,options)


