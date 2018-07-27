#! /usr/bin/python3

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of multitwin.
        
        multitwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

##
# standard libraries -- Version Python 3.5 and higher.
#

import sys
import os
import time
import random
import argparse
from subprocess import Popen, PIPE
import multiprocessing 
from igraph import *

##
# Additional libraries from multitwin
#

import utils as ut
from utils import myModule,myTimer,printLog
import factorgraph as FG
import simplify_graph as SG
import detect_twins as DT
import description as D
import blast_all as BA

## Graphical interface

import bt_launcher
import xmlform

##
# Local executable definitions
#

blastDir = os.environ["MT_BLAST"]
diamondDir = os.environ["MT_DIAMOND"]
exonerateDir = os.environ["MT_EXONERATE"]

blastp = os.path.join(blastDir,"blastp")
makeblastdb = os.path.join(blastDir,"makeblastdb")
diamond = os.path.join(diamondDir,"diamond")

cleanblast = "cleanblast"
FactorGraph = "factorgraph.py"
DetectTwins = "detect_twins.py"
familydetector = "familydetector"
shaveGraph = "simplify_graph.py"
Description = "description.py"

##
# Function definitions
#

def runBlast(fastaFile,blastFile):
    """Run (multithreaded when possible) BLAST on the fastaFile and output the result with option 6 format as the blastFile"""
    i0 = time.clock()
    nbCPU = multiprocessing.cpu_count()
    n = nbCPU-2
    tag = random.randint(100000,1000000)
    dbFile = fastaFile+"_"+str(tag)+".db"
    dbCmd = """makeblastdb -in %s -input_type "fasta" -dbtype prot -out %s -hash_index""" %  (fastaFile,dbFile)
    proc1 = Popen(args=[dbCmd],shell=True,executable = "/bin/bash")
    proc1.communicate()
    blastCmd = """%s -i %s -out %s -db %s -th %d -evalue 1e-5""" % (blastAll,fastaFile,blastFile,dbFile,n)
    try:
        BA.main(inFile=fastaFile,out=blastFile,db=dbFile,th=n)
    except IOError as e:
        printLog("Error in %s: %s\nExiting." % (blastCmd,e),handle)
        return()
    cleanCmd = """rm %s*""" % dbFile
    proc3 = Popen(args=[cleanCmd],shell=True,executable = "/bin/bash")
    proc3.communicate()
    myTimer(i0,"Completed runBlast")

def runDiamond(fastaFile,blastFile):
    """Run DIAMOND on the fastaFile and output the result with option 6 format as the blastFile"""
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
    myTimer(i0,"Completed runDiamond")

def runDescription(annotFile,radical=None,ID=None,keyList=None,handle=sys.stderr,config=None):
    """Compute the result of Description.py on the trailFile hierarchy with basis the annotFile."""
    if not ID:
        ID = "UniqID"
    if keyList:
        keyString = ",".join(keyList)
    descFile = radical+".desc"
    xmlFile = radical+".xml_desc"
    configFile = radical+".config"
    trailFile = radical+".trail"
    edgeFile = radical+".edges"
    compFile = radical+".twin_comp"
    #cmd8 = """%s -i %s -o %s -X %s -a -D -c %s -k %s -H %s %s %s""" % (Description,ID,descFile,configFile,compFile,keyString,trailFile,edgeFile,annotFile)
    cmd8 = """%s -i %s -o %s -X %s -a -D -c %s -H %s %s %s""" % (Description,ID,descFile,configFile,compFile,trailFile,edgeFile,annotFile)
    printLog("--------------------------------------------------\nConfiguring %s" % cmd8,handle)
    try:
        if config:
            D.Main(edgeFile,annotFile,nodeID=ID,outFile=descFile,X=configFile,restrAnnot=True,display=False,comp=compFile,hist=trailFile,keyList=keyString,log=handle)
        else:
            D.Main(edgeFile,annotFile,nodeID=ID,outFile=descFile,X=configFile,restrAnnot=True,display=True,comp=compFile,hist=trailFile,keyList=keyString,log=handle)
    except IOError as e:
        printLog("Error in %s: %s\nExiting." % (cmd8,e),handle)
        return()
    #time.sleep(15)
    if config:
        xmlform.main(xmlFile=configFile)
    cmd8bis = """%s -i %s -o %s -O %s -x %s -a -H %s %s %s""" % (Description,ID,descFile,xmlFile,configFile,trailFile,edgeFile,annotFile)
    printLog("--------------------------------------------------\nRunning %s" % cmd8bis,handle)
    try:
        D.Main(edgeFile,annotFile,nodeID=ID,outFile=descFile,Xout=xmlFile,x=configFile,restrAnnot=True,display=True,hist=trailFile,keyList=keyList,log=handle)
    except IOError as e:
        printLog("Error in %s: %s\nExiting." % (cmd8bis,e),handle)
        return()

def getArticulationPoints(edgeFile):
    """Returns a description of biconnected components of the graph edgeFile."""
    g = Graph.Read_Ncol(edgeFile,directed=False)
    bic,aps = g.biconnected_components(return_articulation_points=True)
    art = []
    for node in aps:
        art.append(g.vs[node]['name'])
    bi_comp = []
    for comp in bic:
        COMP = []
        for node in comp:
            COMP.append(g.vs[node]['name'])
        bi_comp.append(COMP)
    bi_comp.sort(key=len)
    bi_comp.reverse()
    BIC = dict(zip(range(len(bi_comp)),bi_comp))
    COMP = defaultdict(list)
    for cID in BIC:
        for node in BIC[cID]:
            COMP[node].append(cID)
    return(art,COMP)

def completeAnalysis(geneNetwork,genome2sequence,n,c,a=None,clustType=None,UniqID=None,sep=None,keyList=None,handle=sys.stderr,config=None):
    """Perform complete bipartite and twin analysis at a given identity threshold n"""
    directory = "graphs"+str(n)
    try:
        os.mkdir(directory)
    except OSError:
        pass
    # Names and file definitions
    if clustType == 'cc':
        seqCompFile = "CC.nodes"                       # compFile for sequences
        eFile = "CC.edges"
        iFile = "CC.info"
    elif clustType == 'families':
        seqCompFile = "family.nodes"                       # compFile for sequences
        eFile = "family.edges"
        iFile = "family.info"
    else:
        sys.exit("Bad clustering type -- see -C option")
    edgeFile = "graph.edges"                       # edgeFile
    trailFile = "graph.trail"                      # trailFile
    geneNetworkDico = geneNetwork+".dico"
    geneNetworkGenes = geneNetwork+".genes"
    ## ==============================
    # c) assemble sequence families by computing the connected components
    cmd2 = """%s -i %s -d %s -n %s -m %s -p %d""" % (familydetector,geneNetwork,directory,geneNetworkGenes,clustType,n)
    printLog("--------------------------------------------------\nRunning %s" % cmd2,handle)
    proc2 = Popen(args=[cmd2],shell=True,stdout=PIPE,executable = "/bin/bash")
    out = proc2.communicate()[0]
    printLog(out.decode('utf-8'),handle)
    mySeqCompFile = os.path.join(directory,seqCompFile)
    myiFile = os.path.join(directory,iFile)
    myeFile = os.path.join(directory,eFile)
    # renumber back families through geneNetworkDico
    dic1 = ut.loadMapping(geneNetworkDico)
    dic2 = ut.node2communityFasta(mySeqCompFile,sep=sep)
    compDict = ut.composeDict(dic1,dic2)
    ut.outputDict(compDict,mySeqCompFile,sep=sep)
    cleanCmd = """rm %s %s""" % (myiFile,myeFile)
    procClean = Popen(args=[cleanCmd],shell=True,executable = "/bin/bash")
    procClean.communicate()
    ## B) from the sequence families to the bipartite graph
    # a) Cluster sequence families and quotient the graph
    cmd3 = """%s -c %s -k %s -d %s %s %s %s""" % (FactorGraph,mySeqCompFile,UniqID,directory,genome2sequence,edgeFile,trailFile)
    printLog("--------------------------------------------------\nRunning %s" % cmd3,handle)
    FG.Main(edgeFile=genome2sequence,outEdgeFile=edgeFile,outTrailFile=trailFile,direct=directory,community=mySeqCompFile,comm_id=UniqID,sep=sep,log=handle,header=cmd3)
    os.chdir(directory)
    printLog("--------------------------------------------------\ncd %s" % directory,handle)
    ##
    rad = "graph0"
    # b) Remove the degree one nodes from the sequence side
    edges = rad+".edges"
    cmd4 = """%s -d 1 -u 2 %s %s""" % (shaveGraph,edgeFile,edges)
    printLog("--------------------------------------------------\nRunning %s" % cmd4,handle)
    SG.Main(edgeFile=edgeFile,outEdgeFile=edges,degree=1,nodeType=2,sep=sep,log=handle)
    # d) Compute twins and twin supports of the bipartite graph
    twins = rad+".twins"
    twinComp = rad+".twin_comp"
    cmd6 = """%s -o %s -u 2 -c %s %s """ % (DetectTwins,twins,twinComp,edges)
    printLog("--------------------------------------------------\nRunning %s" % cmd6,handle)
    try:
        DT.Main(edgeFile=edges,outFile=twins,sep=sep,unilat='2',comp=twinComp,log=handle)
    except IOError as e:
        printLog("Error in %s: %s\nExiting." % (cmd6,e),handle)
        return()
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
    printLog("--------------------------------------------------\nRunning %s" % cmd7,handle)
    try:
        FG.Main(edgeFile=edges,outEdgeFile=newEdges,outTrailFile=newTrail,direct=twinDir,community=twins,comm_id=UniqID,in_trail=trailFile,sep=sep,log=handle,header=cmd7)
    except IOError as e:
        printLog("Error in %s: %s\nExiting." % (cmd7,e),handle)
        return()
    os.chdir(twinDir)
    printLog("--------------------------------------------------\ncd %s" % twinDir,handle)
    # b) Computing articulation points and biconnected components
    ART,BIC = getArticulationPoints(newEdges)
    artPoints = rad+".art"
    aP = open(artPoints,"w")
    printLog("--------------------------------------------------\nPrinting %d articulation points in %s" % (len(ART),artPoints),handle)
    for node in ART:
        outString = """%s\t%s\n""" % (node,",".join([str(ID) for ID in BIC[node]]))
        aP.write(outString)
    aP.close()
    bcNb = 0
    bicFile = rad+".bic_comp"
    bC = open(bicFile,"w")
    for node in BIC:
        for ID in BIC[node]:
            bcNb = max(bcNb,ID)
            bC.write("""%s\t%d\n""" % (node,ID))
    bC.close()
    printLog("--------------------------------------------------\nPrinting %d biconnected components in %s" % (bcNb+1,bicFile),handle)    
    ## D) annotations and twin component analysis
    if a:
        edges = rad+".edges"
        twins = rad+".twins"
        twinComp = rad+".twin_comp"
        cmd9 = """%s -o %s -u 2 -c %s %s """ % (DetectTwins,twins,twinComp,edges)
        printLog("--------------------------------------------------\nRunning %s" % cmd9,handle)
        try:
            DT.Main(edgeFile=edges,outFile=twins,sep=sep,unilat='2',comp=twinComp,log=handle)
        except IOError as e:
            printLog("Error in %s: %s\nExiting." % (cmd9,e),handle)
            return()
        runDescription(a,radical=rad,ID=UniqID,keyList=keyList,handle=handle,config=config)
    #return()
        
##
# Main procedure ====================================================
#

def processArgs():
    parser = argparse.ArgumentParser(description='Runs a complete bipartite graph analysis') 
    parser.add_argument("-b", "--blast/diamond_output_file", dest="b", help="Output of BLAST/DIAMOND program",type=str)
    parser.add_argument("-g", "--genome_to_gene_file", dest="g",help="Initial bipartite genomeGene file")
    parser.add_argument("-a", "--annotation_file", dest="a", help="Annotation file, referenced by UniqID")
    parser.add_argument("-k", "--annotation_keys", dest="k", help="Optional list of keys in annotFile to consider (requires option -a -- default All)",default=None)
    parser.add_argument("-n", "--identity_threshold", dest="n", help="Threshold(s) for sequence similarity (comma-separated)",default="30,40,50,60,70,80,90,95")
    parser.add_argument("-c", "--mutual_cover", dest="c", help="Threshold for reciprocal sequence length cover",default=80)
    parser.add_argument("-C", "--clustering_method", dest="C", help="Clustering type for family detection (cc or families)",default="cc")
    parser.add_argument("-I", "--input_network", dest="I", help="Skips CleanBlast step with supplied networkFile FILE")
    parser.add_argument("-f", "--fasta_file", dest="f", help="Fasta file -- if supplied, then the blast-all will be run first to generate the blastFile.\nAttention, the supplied blastFile NAME will be used for the output")
    parser.add_argument("-A", "--similarity_search_software", dest="A", help="Use ALN (b=BLAST/d=Diamond) sequence comparison program (only with -f option)",default="b")
    parser.add_argument("-i", "--unique_node_identifier", dest="i", help="Key identifier (default: UniqID)",default="UniqID")
    parser.add_argument("-K", "--graphic_interface_for_Description", dest="K", action="store_true", help="Launch graphical configuration interface for description.py module")
    parser.add_argument("-D", "--output_dir", dest="D", help="Store everything under DIR")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    parser.add_argument("-s", "--separator", dest="s", help="Field separator (default '\\t')",default="\t")
    parser.add_argument("-G", "--graphical", dest="G", action="store_true", help="Launch graphical interface")
    return(parser)

def Main(blastFile=None,genome2sequence=None,sep=None,thr=None,cov=None,in_network=None,fasta=None,aln=None,clust=None,annot=None,key=None,keyList=None,log=None,directory=None,config=None):
    """ Main program """
    ###
    try:
        startWD = os.path.abspath(os.path.dirname(blastFile))
    except:
        startWD = os.path.abspath(os.getcwd())
    os.chdir(startWD)
    if directory:
        rootDir = os.path.abspath(directory)
        if not os.path.exists(rootDir):
            os.makedirs(rootDir)
    else:
        rootDir = os.getcwd()
    if log != sys.stderr:
        log = os.path.join(rootDir,log)
    ### Argument processing =============================================================================================================
    if not blastFile or not genome2sequence:
        sys.exit("Required files %s and %s" % ("blastFile","genome2sequence"))
    blastFile = os.path.abspath(blastFile)
    genome2sequence = os.path.abspath(genome2sequence)
    ThresholdList = list(map(int,thr.strip().split(",")))
    cover = float(cov)
    print("Starting directory: %s" % startWD)
    print("Root directory: %s" % rootDir)
    if fasta:
        if aln == "b":
            runBlast(fasta,blastFile)
        elif aln == "d":
            runDiamond(fasta,blastFile)
        else:
            sys.exit("Wrong sequence comparison option -- use (b) for BLAST - (d) for DIAMOND")
    UniqID = key
    ## Filename definitions =============================================================================================================
    if in_network:
        geneNetwork = os.path.abspath(in_network)
    else:
        geneNetwork = blastFile+".cleanNetwork"
    if annot:
        annot = os.path.abspath(os.path.join(startWD,annot))
        if keyList:
            keyList = keyList.split(",")
        else:
            with open(annot,'r') as ANNOT:
                keyList = ANNOT.readline().strip().split(sep)[1:]
    else:
        annot = None
        keyList = None
    ## Corps du programme ===========================================
    inext = time.clock()
    os.chdir(rootDir)
    ## A) from the blast output to the sequence families
    # a) filter self-hits and keep only best hit
    if not in_network:
        cmd1 = "%s -n 1 -i %s" % (cleanblast,blastFile)       # the output are three files named blastFile".cleanNetwork", blastFile".cleanNetwork.dico" and blastFile".cleanNetwork.genes" 
        printLog("--------------------------------------------------\nRunning %s" % cmd1,log)
        proc1 = Popen(args=[cmd1],shell=True,stdout=PIPE,executable = "/bin/bash")
        out = proc1.communicate()[0]
        printLog(out.decode('utf-8'),log)
    # b) perform complete analysis for each threshold
    for n in ThresholdList:
        STR = """--------------------------------------------------\nSimilarity threshold %d%%""" % n
        printLog(STR,log)
        completeAnalysis(geneNetwork,genome2sequence,n,cover,a=annot,clustType=clust,UniqID=key,sep=sep,keyList=keyList,handle=log,config=config)
        os.chdir(rootDir)
    ## Fin ======================================================
    prog = myModule()
    if prog == "__main__.py":
        prog = sys.argv[0].split("/")[-1]
    ## Sortie ======================================================
    return()

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    args = parser.parse_args()
    CMD = " ".join(sys.argv)
    #printLog(CMD,args.l)
    #print(vars(args))
    if not args.G:
        Main(blastFile=args.b,genome2sequence=args.g,sep=args.s,thr=args.n,cov=args.c,in_network=args.I,\
             fasta=args.f,aln=args.A,clust=args.C,annot=args.a,key=args.i,keyList=args.k,log=args.l,directory=args.D,config=args.K)
    else:
        bt_launcher.main(prog,args)
