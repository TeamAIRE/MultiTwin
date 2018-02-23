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
import  time
from optparse import OptionParser
import inspect
import math
import random
from subprocess import *
from collections import defaultdict
from collections import Counter

##
# Personal libraries 
#

from Utils import *

##
# Main procedure ====================================================
#

def processArgs():
    """ Parser function of main """
    parser = OptionParser()
    parser.add_option("-r", "--reverse", dest="r", action="store_true",help="Print history in chronological order (starting from the root)")
    return parser

def Main(args,options):
    """ Main program """
    ### Argument processing ========================================
    trailFile = args[0]
    ## Filename definitions ======================================
    trailFile = os.path.join(os.getcwd(),trailFile)
    wd = os.path.dirname(trailFile)
    ## Lecture des fichiers ========================================
    history = []
    while trailFile:
        previous = trailHist(trailFile)
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
    if options.r:
        history.reverse()
    for hist in history:
        print hist
    return

#========= Main program

if __name__ == '__main__':
    prog = sys.argv[0].split("/")[-1]
    parser = processArgs()
    options, args = parser.parse_args()
    usage = "\nUsage: %s [options] trailFile; \nTry %s -h for details" % (prog,prog)
    if len(args) < 1:
        parser.error(usage)
    Main(args,options)	

