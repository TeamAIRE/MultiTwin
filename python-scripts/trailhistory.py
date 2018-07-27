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
# local personal libraries

import utils as ut
from utils import myModule,myTimer,printLog

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = argparse.ArgumentParser(description='Recalls commands from ROOT graph to current graph')
    parser.add_argument("trailFile", help="Input graph edge file",type=str)
    parser.add_argument("-r", "--reverse", dest="r", action="store_true",help="Print history in chronological order (starting from the root)")
    parser.add_argument("-l", "--log", dest="l", help="Specify log file",default=sys.stderr)
    return(parser)

def Main(trailFile=None,reverse=None,log=None):
    """ Main program """
    trailFile = os.path.join(os.getcwd(),trailFile)
    wd = os.path.dirname(trailFile)
    ## Lecture des fichiers ========================================
    history = []
    while trailFile:
        previous = ut.trailHist(trailFile)
        try:
            directory = previous['d']
            wd = os.path.dirname(wd.rstrip("/"))
        except:
            pass
        histString = """>In directory %s:\n%s\n""" % (wd,previous['cmd'])
        history.append(histString)
        try:
            trailFile = os.path.join(wd,previous['t'])
        except:
            break
    if reverse:
        history.reverse()
    for hist in history:
        print(hist)
    return

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    args = parser.parse_args()
    header = " ".join(sys.argv)
    printLog(header,args.l,mode="w")
    print(vars(args))
    Main(trailFile=args.trailFile,reverse=args.r,log=args.l)
