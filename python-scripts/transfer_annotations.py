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
import time
import argparse

##
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog

##
# Function definitions
#

def transferAnnotations(annotFile,trailFile,newID,header=None,skip=None):
    """Given an annotation file key: annotations, transfer the annotations through the dictionary as dictionary[key]: annotations."""
    ann = ut.loadLineDict(annotFile,header=header)
    if skip:
        trail = loadMapping2(trailFile,skip=2)  ## Since the header modification of the trail file, this is mandatory
    else:
        trail = loadMapping2(trailFile,skip=0)  ## For any other use
    newDict = dict()
    if header:
        newDict['header'] = [ann['header'].pop(0)]
        newDict['header'].append(newID) 
        newDict['header'].extend(ann['header'])
        del ann['header']
    for i,v in iter(ann.items()):
        try:
            newKey = trail[i]
            newValue = [newKey]
            newValue.extend(v)
            newDict[i] = newValue
        except:
            pass
    return newDict

def transferAnnotationsSkipOld(annotFile,trailFile,newID,header=None,skip=None):
    """Given an annotation file key: annotations, transfer the annotations through the dictionary as dictionary[key]: annotations."""
    ann = loadLineDict(annotFile,header=header)
    if skip:
        trail = loadMapping2(trailFile,skip=2)  ## Since the header modification of the trail file, this is mandatory
    else:
        trail = loadMapping2(trailFile,skip=0)  ## For any other use
    newDict = dict()
    if header:
        ann['header'].pop(0)
        newDict['header'] = [newID]
        newDict['header'].extend(ann['header'])
        del ann['header']
    for i,v in iter(ann.items()):
        try:
            newKey = trail[i]
            newValue = v
            newDict[newKey] = newValue
        except KeyError:
            pass
    return newDict

def loadMapping2(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2,skip=0):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    if skip:
        i = 0
        while i < skip:
            f.readline()
            i += 1
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
        mapping[nodeID] = compID
    f.close()
    return mapping

def loadLineDict(fileName,header=False,split_char="\t",keyIndex=1,valueIndexList=None):
    """Given a file, select field keyIndex as key, and the rest as valueList. 
    Careful: works as loadMapping, rather than loadDict, i.e will not support multiple keys!! This should be carefully investigated (21/10/2015)"""
    f = open(fileName,'U')
    newDict = dict()
    if header:
        HEADER = f.readline().strip().split(split_char)
        if valueIndexList:
            HEADER = sliceList(HEADER,valueIndexList)
        newDict['header'] = HEADER
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID = lineItems.pop(keyIndex-1)
        if valueIndexList:
            lineItems = sliceList(lineItems,valueIndexList)
        newDict[nodeID] = lineItems
    f.close()
    return newDict

def outputDict2(composedDict,outFile,sep="\t",header=False):
    g = open(outFile,"w")
    n = len(composedDict[list(composedDict.keys())[0]])
    FORMAT = """%s\t"""*n+"""%s\n"""
    if header:
        outKeys = tuple(header)
        headline = FORMAT % outKeys
        g.write(headline)
        del composedDict['header']
    for i,v in iter(composedDict.items()):
        valueList = [i]
        valueList.extend(v)
        vals = map(lambda x:str(x),valueList)
        outString = sep.join(vals)+"\n"
        g.write(outString)
    g.close()

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Renames attributes according to trailFile')
    parser.add_argument("annotFile", help="Input graph edge file",type=str)
    parser.add_argument("trailFile", help="Output graph edge file",type=str)
    parser.add_argument("outFile", help="Output trailing file",type=str)
    parser.add_argument("-H", "--header", dest="h",action="store_true",help="Specify if there's a header line")
    parser.add_argument("-n", "--new", dest="n",help="Give name of new ID", default="newID")
    parser.add_argument("-S", "--skip-old", action="store_true", dest="S",help="Skip old identifier", default=False)
    parser.add_argument("-s", "--skip", action="store_false", dest="s",help="Skip 2 rows (new trail format): activated by default (select flag to unactivate)", default=True)
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    return(parser)

def Main(annotFile=None,trailFile=None,outFile=None,header=None,new=None,old=None,skip=None,log=None):
    """ Main program """
    ### Argument/options listing
    ### Option processing ===========================================
    ## Filename definitions ======================================== 
    i0 = time.clock()
    inext = i0
    ## File reading options ======================================== 
    ## Body ======================================================== The dictionary old_nodes --> new_nodes obtained as the completion of the clustering file.
    if old:
        newAnnot = transferAnnotationsSkipOld(annotFile,trailFile,new,header=header,skip=skip)
    else:
        newAnnot = transferAnnotations(annotFile,trailFile,new,header=header,skip=skip)
    ## Sortie ======================================================
    try:
        HEADER = newAnnot['header']
    except:
        HEADER = None
    print(HEADER)
    outputDict2(newAnnot,outFile,header=HEADER)
    inext = myTimer(inext,"New annotation writing",handle=log)
    ## Output options ======================================================
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
    print(vars(args))
    Main(annotFile=args.annotFile,trailFile=args.trailFile,outFile=args.outFile,header=args.h,new=args.n,old=args.S,skip=args.s,log=args.l)
