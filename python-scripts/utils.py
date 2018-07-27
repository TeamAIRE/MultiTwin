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
import os
import time
import inspect
import math
import random
import copy
from collections import Counter,defaultdict,deque
from igraph import *
from subprocess import Popen
from itertools import chain, combinations
import contextlib
from bs4 import BeautifulSoup
from bs4 import Tag
import tkinter as tk
from tkinter import Canvas
from tkinter.constants import LEFT, RIGHT
from tkinter.ttk import Label, Scrollbar, Style
from ttkthemes import themed_tk as TTk 
from screeninfo import get_monitors

##
# Tkinter class definitions
#

def screenSize():
    for m in get_monitors():
        if (m.x,m.y) == (0,0):
            return (m.width,m.height)

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    W,H = screenSize()
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = W // 2 - win_width // 2
    y = H // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class HelpWindow:

    def __init__(self,text=None,name=None):
    
        def on_configure(event):
            # update scrollregion after starting 'mainloop'
            # when all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))
        # initialize root object
        self = TTk.ThemedTk()
        self.configure(background="lightgrey")
        style = Style()
        style.theme_use('radiance')
        self.title("Help interface for %s" % name)
        canvas = Canvas(self)
        canvas.pack(side=LEFT)
        scrollbar = Scrollbar(self, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        canvas.configure(yscrollcommand = scrollbar.set)
        # call object
        app = tk.Label(self,text=text, fg="dimgrey", justify='left', font=('Courier',14))
        app.pack()
        self.update_idletasks()
        self.canvas = canvas
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', on_configure)
        canvas.create_window((0,0), window=app, anchor='nw')
        RHeight = min(300,app.winfo_reqheight())
        RWidth = app.winfo_reqwidth()       
        canvas.configure(width = RWidth, height = RHeight)
        self.bind('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units'))
        self.bind('<Button-5>', lambda event: canvas.yview_scroll(1, 'units'))

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 450   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.configure(background="lightgrey")
        label = tk.Label(self.tw, text=self.text, fg="dimgrey", justify='left', wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

##
# XML Class definitions
#

class Trail(object):
    
    def __init__(self,filename=None,rank=None,keys=None):
        self.name = filename
        self.rank = rank
        if keys:
            self.keys = keys
        else:
            self.keys = []

class Module(object):
    
    def __init__(self,filename=None,name=None,keys=None):
        self.filename = filename
        self.name = name
        if keys:
            self.keys = keys
        else:
            self.keys = []

class Key(object):
    
    def __init__(self,name=None,Type=None,display=None):
        self.name = name
        self.Type = Type
        self.display = display

class Attribute(object):
    """Modified wrt original one by having as Type and display objects a dictionary, so as to be able to specify the status of the attribute for all nodeTypes at once."""
    
    def __init__(self,name=None,Type=None,display=None):
        self.name = name
        self.Type = Type
        self.display = display

##
# XML generator
#

def generateXML(nodeTypes,trailObjects=None,compObject=None,attDict=None,outFile=None,display=False,root=None):
    if not outFile:
        outFile = "config.xml"
    if not root:
        root = os.getcwd()
    with smart_open(outFile) as g:
        header = """<?xml version="1.0" encoding="UTF-8"?>

<!-- DTD declaration -->

<!DOCTYPE conf [
<!ELEMENT root (#PCDATA) >
<!ELEMENT trail (rank,filename,key*) >
<!ELEMENT mod (filename,name,key*) >
<!ELEMENT key (type,name,display) >
<!ATTLIST key type CDATA #REQUIRED display (True|False) "False" >
<!ELEMENT attr (name,node*) >
<!ELEMENT node EMPTY>
<!ATTLIST node type CDATA #REQUIRED display (True|False) "False" >
<!ELEMENT rank (#PCDATA) >
<!ELEMENT filename (#PCDATA) >
<!ELEMENT name (#PCDATA) >
]>

<!-- Body of the configuration file -->

<conf>

<root>%s</root>

<!-- List here all trail files -->
""" % root
        g.write(header)
        if trailObjects:
            for trailObject in trailObjects:
                g.write(genTrail(trailObject,nodeTypes=nodeTypes,display=display))
        else:
            g.write(genTrail(trailObject=None,nodeTypes=nodeTypes,display=display))
        g.write(genMod(modObject=compObject,nodeTypes=nodeTypes,display=display))
        g.write("""
<!-- List of annotation attributes -->
""")
        if attDict:
            ATT = defaultdict(list)
            for i,v in attDict.items():
                for val in v:
                    ATT[val].append(i)
            #print(ATT)
            for val, keys in ATT.items():
                g.write(genAtt(attName=val,nodeType=keys,display=display))
        else:
            g.write(genAtt())
        g.write("""</conf>""")
        return outFile

def genTrail(trailObject=None,nodeTypes=None,display=None):
    if not trailObject:
        rank = '1'
        filename = ''
    else:
        rank = trailObject.rank
        filename = trailObject.file
    trailString = """<trail>
	<rank>%s</rank>
	<filename>%s</filename>
""" % (rank,filename)
    for nodeType in nodeTypes:
        try:
            typeString = trailObject.attribute[int(nodeType)]
        except:
            typeString = None
        trailString += genKey(nodeType,typeString=typeString,display=display)
    trailString += """</trail>
""" 
    return trailString

def genKey(nodeType,typeString=None,display=None):
    if not typeString:
        typeString = "NodeType%d" % nodeType
    if display:
        displayString = str(display)
    else:
        displayString = ""

    keyString = """        <key type="%d" display="%s">
		<name>%s</name>
        </key>
""" % (nodeType,displayString,typeString)
    return keyString

def genMod(modObject=None,nodeTypes=None,display=None):
    if not modObject:
        modFile = ""
        modName = "Component"
    else:
        modFile = modObject.file
        modName = modObject.attribute[0]
    modString = """
<!-- Set the module file -->

<mod>
        <filename>%s</filename>
        <name>%s</name>
""" % (modFile,modName)
    if modFile:
        for nodeType in nodeTypes:
            modString += genKey(nodeType,display=display)
    modString += """</mod>
""" 
    return modString

def genAtt(attName=None,nodeType=None,display=None):
    if not attName:
        attName = ""
        nodeType = ""
        display = None
    attString = """<attr>
        <name>%s</name>""" % attName
    if display:
        displayString = str(display)
    else:
        displayString = ""
    for t in nodeType:
        attString += """
        <node type="%d" display="%s"></node>""" % (t,displayString)
    attString += """
</attr>
"""
    return attString

##
# XML Output
#

def xmlDescription(annot=None,nodeDict=None,entries=None,compObject=None,trails=None,nodeType=None,keyDict=None,xmlOutFile=None,outFile=None,track=None,debug=None,X=None,verbose=False,handle=sys.stderr):
    """
    annot: UniqID -> dict_of_annot_values {annot1: value1,...}
    nodeDict: currentID -> UniqID  --  if None, should be able to return currentID -> currentID
    entries: list of UniqIDs to use
    compObject: if None, should correspond to the nodes of the current graph
    trails: list of trailObjects
    nodeType: currentID -> nodeType_of_currentID
    keyDict: output of the options.k process
    outFile: options.o
    """
    inext = time.clock()
    XML = X
    if verbose:
        for k,v in iter(XML.items()):
            print(k)
            if k == 'trails':
                for obj in v:
                    print(obj)
                    print(obj.rank)
                    print(obj.name)
                    for key in obj.keys:
                        if key.display == "Yes":
                            print(key)
                            print(key.name)
            elif k == 'attributes':
                for obj in v:
                    if obj.display == 'Yes':
                        print(obj)
                        print(obj.name)
                        print(obj.Type)
            elif k == 'mod':
                for obj in v:
                    print(obj)
                    print(obj.filename)
                    print(obj.name)
                    for key in obj.keys:
                        if key.display == "Yes":
                            print(key)
                            print(key.name)
    # 1) Preparing the description
    k = 0                                                                           # counter for the number of components/modules
    if not compObject.file:                                                         # We define a compIter that enumerates the elements of the module (or the nodes if not given)
        try:
            compIter = myIter(list(nodeDict.keys()))
        except:
            compIter = myIter(entries)
        compObject.attribute = ['Node']
    else:
        compObject.getDict()
        compIter = myIter(compObject.dico)
    if trails:
        ntypes = dict()
        attributes = dict()
        trails.sort(key=lambda x:x.rank)
        trails.reverse()
        for trail in trails:
            trail.getDict()
            ntypes[trail] = [att for att in trail.attribute if trail.attribute[att]]
            attributes[trail] = list(map(lambda x:keyDict[x],ntypes[trail]))
    att2key = dict()                                                                # This is only used to sort the values in the display
    if track:
        att2key[track] = max(keyDict.keys())+1
    for t,v in iter(keyDict.items()):
        for vv in v:
            att2key[vv] = t   
    inext = myTimer(inext,"Preparing description",handle=handle)
    # 2) Constructing the actual description
    storeDict = dict()
    with smart_open(outFile) as g:                                                  # output File
        for c,C in compIter:
            k += 1
            if k % 10000 == 0:
                printLog(k,sys.stderr)
            try:
                U = unList(map(lambda x:nodeDict[x],C))                             # component's content (original IDs)
            except:
                U = C
            try:
                nTypes = dict(zip(U,list(map(lambda x:nodeType[trails[0].dico.dict[x]],U))))  # get types of the involved nodes
            except:
                nTypes = restrictDico(nodeType,U)                                  # get types of the involved nodes
            valDict = mapValues(annot,U)                                           # get the annotations of the members of the group
            val = reduceAnnot(valDict,track=track)                                 # assemble them according to similar values
            compString = """%s %s\n""" % (compObject.attribute[0],c) 
            vals = list(val.keys())[:]
            vals.sort(key=lambda x:att2key[x])
            for i in vals:
                compString += str(i)+"\t"+str(val[i])+"\n"
            xmlString = """<mod name="%s" id="%s">\n""" % (compObject.attribute[0],c)
            xmlString += """<content>\n"""
            xmlString += displayDic(val,att2key,pad="\t")[1]
            xmlString += """</content>\n"""
            for trail in trails:                                                   # We assemble the component content according to the hierarchy of trail files
                nodes = set(map(lambda x:trail.dico.dict[x],U))                    # component content (nodeIDs at level t without repetition)
                nodeGroups = list(map(lambda x:trail.dict_inv[x],nodes))                 # original nodes below nodeIDs (original IDs split in groups having the same nodeID at level t)
                nType = lambda group:list(set(map(lambda x:nTypes[x],group)))[0]   # here we sort the groups by type: otherwise it's not very clean. NB: this assumes that groups are type-homogeneous (!!)
                nodeGroups = [ng for ng in nodeGroups if nType(ng) in ntypes[trail]]
                nodeGroups.sort(key=nType)
                count = len(nodeGroups)
                if count:
                    compString += "=========================================== level %d\n" % trail.rank
                    xmlString += """<trail level="%d">\n""" % trail.rank                    
                    compString += "++++++++++++++++++++++++++++++++++++++++ %d %s\n" % conj(count,"group") 
                res = []
                for group in nodeGroups:                                           # consider each group in turn
                    groupID = list(map(lambda x:trail.dico.dict[x],group))[0]
                    valDict = mapValues(annot,group)                               # get the annotations of the members of the group: here we would like to restrict to the keysForType
                    nt = nType(group)
                    val = reduceAnnot(valDict,track=track)                         # assemble them according to similar values
                    if val:
                        res.append((val,trail.attribute[nType(group)],groupID,nt))
                res.sort(key=lambda x:len(x[0]))
                res.reverse()
                for v in res:
                    compString += """%s %s\n""" % (v[1],v[2])
                    compString += str(v[0])+"\n"
                    compString += "---------------------------------------\n"
                    xmlString += """<key name="%s" type="%s" id="%s">\n""" % (v[1],v[3],v[2])
                    xmlString += displayDic(v[0],att2key,pad="\t")[1]
                    xmlString += "</key>\n"
                if count:
                    xmlString += "</trail>\n"
            compString += "#############################################\n"
            xmlString += "</mod>\n"
            storeDict[c] = {'string' : compString, 'value' : len(U), 'xml': xmlString}
    printLog("End of description: processed %d components" % k,handle)
    comps = list(storeDict.keys())
    comps.sort(key=lambda x:storeDict[x]['value'])
    comps.reverse()
    if xmlOutFile:
        with smart_open(xmlOutFile) as g:                                                 # output File
            header = headerConf()
            g.write(header)
            for c in comps:
                g.write(storeDict[c]['xml'])
            g.write("""</desc>\n""")
    if outFile:
        with smart_open(outFile) as g:                                                 # output File
            for c in comps:
                g.write(storeDict[c]['string'])
    return storeDict

def displayDic(val,att2key,pad=""):
    compString = ""
    xmlString = ""
    vals = list(val.keys())[:]
    vals.sort(key=lambda x:att2key[x])
    for i in vals:
        i = str(i)
        v = str(val[i])
        compString += str(i)+"\t"+str(val[i])+"\n"
        xmlString += """%s<attr name="%s">\n%s\t%s\n%s</attr>\n""" % (pad,i,pad,v,pad) 
    return compString,xmlString


def headerConf():
    header = """<?xml version="1.0" encoding="UTF-8"?>\n

<!-- DTD declaration -->

<!DOCTYPE desc [
<!ELEMENT mod (content,trail*,key*) >
<!ELEMENT trail (key*) >
<!ELEMENT key (attr*) >
<!ELEMENT attr (#PCDATA) >
]>

<!-- Body of the description file -->

<desc>

"""
    return header

##
# XML parser
#

##
# BS4 version
#

def parse(xmlFile):
    handle = open(xmlFile,'U')
    gDict = BeautifulSoup(handle,'xml')
    return(gDict)

def loadMod(mod):
    filename = mod.find('filename').string
    name = mod.find('name').string
    keys = []
    KEYS = mod.find_all('key')
    for KEY in KEYS:
        kName = KEY.find('name').string
        disp = KEY.attrs['display']
        TYPE =  KEY.attrs['type']
        keys.append(Key(name=kName,Type=TYPE,display=disp))
    module = Module(filename=filename,name=name,keys=keys)
    return(module)

def loadTrail(trail):
    filename = trail.find('filename').string
    #print(filename)
    rank = trail.find('rank').string
    keys = []
    KEYS = trail.find_all('key')
    for KEY in KEYS:
        kName = KEY.find('name').string
        disp = KEY.attrs['display']
        TYPE =  KEY.attrs['type']
        keys.append(Key(name=kName,Type=TYPE,display=disp))
    TRAIL = Trail(filename=filename,rank=rank,keys=keys)
    return(TRAIL)

def loadAttr(attr):
    name = attr.find('name').string
    ATTR = []
    KEYS = attr.find_all('node')
    for KEY in KEYS:
        disp = KEY.attrs['display']
        TYPE =  KEY.attrs['type']
        ATT = Attribute(name=name,display=disp,Type=TYPE)
        ATTR.append(ATT)
    return(ATTR)

def parseXML(configFile):
    XML_dict = {'trails' : [], 'mod': [], 'attributes': []}
    soup = parse(configFile)
    MOD = soup.find_all('mod')
    for mod in MOD:
        XML_dict['mod'].append(loadMod(mod))
    TRAIL = soup.find_all('trail')
    for trail in TRAIL:
        XML_dict['trails'].append(loadTrail(trail))
    ATTR = soup.find_all('attr')
    for attr in ATTR:
        XML_dict['attributes'].extend(loadAttr(attr))
    return(XML_dict)

##
# Class definitions
#

class myMod(object):
    
    def __init__(self,fileName=None,attDict=None):
        self.file = fileName
        self.attribute = attDict
        self.dico = dict()

    def getDict(self):
        self.dico = loadDict(self.file,keyIndex=2,valueIndex=1)

class myTrail(object):
    
    def __init__(self,fileName=None,rank=None,attDict=None):
        self.file = fileName
        self.rank = rank
        self.attribute = attDict
        self.dico = myLocalDict()
        self.header = None
        self.dict_inv = dict()

    def getDict(self):
        self.dico.dict,self.dico.header = loadMappingWithHeader(self.file)
        self.dict_inv = InvertMap(self.dico.dict)

class myLocalDict():
    
    def __init__(self):
        self.dict = dict()
        self.header = None

###################### CLASS myDict

class myDict(dict):
    
    def __init__(self,dic=None,keys=None,values=None,empty='-'):
        self.empty = empty
        try:
            keys = dic.keys()
            values = dic.values()
        except:
            pass
        if keys:
            if len(keys) != len(values):
                raise ValueError
            n = len(keys)
            for i in range(n):
                if values[i] != empty:
                    self[keys[i]] = values[i]

    def myGetKey(self,key):
        try:
            return self[key]
        except:
            pass

    def subDict(self,keyList):
        subDict = myDict()
        subDict = dict(zip(keyList,list(map(lambda x:self.myGetKey(x),keyList))))
        return subDict

    def subDictIter(self,keyIter):
        subDict = myDict()
        subDict = dict((k,self.myGetKey(k)) for k in keyIter)
        return subDict

    def myHasKey(self,key):
        try:
            return (key in self)
        except:
            pass

class myDict0(dict):
    
    def __init__(self,dic=None,keys=None,values=None,empty='-'):
        self.empty = empty
        if keys:
            if len(keys) != len(values):
                raise ValueError
            n = len(keys)
            for i in range(n):
                if values[i] != empty:
                    self[keys[i]] = values[i]

    def myGetKey(self,key):
        try:
            return self[key]
        except:
            pass

    def myHasKey(self,key):
        try:
            return (key in self)
        except:
            pass

    def subDict(self,keyList):
        subDict = myDict()
        subDict = dict(zip(keyList,list(map(lambda x:self.myGetKey(x),keyList))))
        return subDict

##
# Functions from Utils
#

@contextlib.contextmanager
def smart_open(filename=None,mode='w'):
    if filename and filename != '-':
        fh = open(filename, mode)
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
            
def myTimer(i_first,string="",handle=sys.stderr,delim=None):
    if not string:
        string = "Computation"
    i_next = time.clock()
    t1 = i_next-i_first
    printLog("%s: %f seconds" % (string,t1),handle)
    if delim:
            printLog("--------------------------------------------------",handle)
    return(i_next)

def myModule():
    caller = inspect.currentframe().f_back
    return caller.f_globals['__name__']+".py"

def unList(List_of_Lists):
    return [item for sublist in List_of_Lists for item in sublist]

def composeDict(dico1,dico2):
    """
    Given a dictionary1 key1 -> value1 and a dictionary2 key2 -> value2, such that {value1} has the same range as {key2}, construct dictionary key1 -> dict2[value1]
    This is the composition of mappings: dico2 o dico1
    If range of dico1 exceeds domain of dico2, what do we do? -- Let's say nothing, so that one can give several annotation files
    """
    newDict = dict()
    for i,v in iter(dico1.items()):
        try:
            newDict[i] = dico2[v]
        except KeyError:
            pass
    return(newDict)

##
# Clustering 
#

def node2community(communityFile,sep=None,ID=False,verbose=None): 
    """ From a communityFile input, create a dictionary in order to assign a community for each node.
    This function renames the communities in order for them to be numbered from 0 to n-1  where n is the number of communities."""
    newName = dict()
    clusterDict = dict()
    k = 0
    if verbose:
        print("Reading "+communityFile+"...")
    f = open(communityFile,'U')
    for line in f:
        lineItems = line.rstrip().split(sep)
        clustID = int(lineItems[1])
        try:
            n = clusterDict[clustID]
        except KeyError:
            if not ID:
                clusterDict[clustID] = k
                k += 1
            else:
                clusterDict[clustID] = clustID
            n = clusterDict[clustID]
        newName[lineItems[0]] = n
    f.close()
    if verbose:
        print("...done")
    return(newName)

def node2communityFasta(communityFile,sep=None,verbose=None): 
    """ From a communityFile input, create a dictionary in order to assign a community for each node.
    This function keeps the original community IDs."""
    newName = dict()
    if verbose:
        print("Reading "+communityFile+"...")
    f = open(communityFile,'U')
    for line in f:
        if line.startswith(">"):
            line = line.rstrip()
            p = re.search(">[A-Za-z]*([0-9]*)",line)
            clustID = int(p.group(1))
        else:
            lineItems = line.rstrip().split(sep)
            newName[lineItems[0]] = clustID
    f.close()
    if verbose:
        print("...done")
    return(newName)

def network2communityNetwork(network_filename,dictionary=None,sep=None,verbose=None,useWeights=False):
    """ from a network_filename and a dictionary which for a node, gives its community, the function builds a weighted community network. 
    The weight corresponds to (1+) the log 10 of the number of edges between the two communities 
    Output: a dictionary storing the complete renumbering of nodes : node -> community
    the edge_dict : community1 -- community2 with the corresponding weight.
    """ 
    edges_dict = defaultdict(float)
    edges_std = defaultdict(float)
    edges_count = defaultdict(int)
    try:
        maxCommunity = max(map(lambda x:int(x),dictionary.values()))+1
    except AttributeError:
        dictionary = dict()
        maxCommunity = 0
    if verbose:
        print("Getting initial community value %d" % maxCommunity)
        print("Reading "+network_filename)
    f = open(network_filename,"r")
    for line in f:
        lineItems = line.rstrip().split(sep)
        node1 = lineItems[0]
        node2 = lineItems[1]
        try:
            weight = float(lineItems[2])
            myWeight = useWeights*weight+(1-useWeights)
        except IndexError:
            myWeight = 1
        try:
            community1 = dictionary[node1]
        except KeyError:
            community1 = maxCommunity
            dictionary[node1] = maxCommunity
            maxCommunity += 1
        try:
            community2 = dictionary[node2]
        except KeyError:
            community2 = maxCommunity
            dictionary[node2] = maxCommunity
            maxCommunity += 1
        if community1 == community2 :
            continue # edge intra community
        else :
            edge = (community1,community2)
            #print edge
            edges_dict[edge] = (edges_dict[edge]*edges_count[edge] + myWeight)/(edges_count[edge]+1)  # mean of (current weight,count) (new weight,1)
            edges_std[edge] = (edges_std[edge]*edges_count[edge] + myWeight**2)/(edges_count[edge]+1) # mean of squared (current weight,count) (new weight,1)
            edges_count[edge] += 1
    f.close()
    if verbose:
        print("done")
    return dictionary,edges_dict,edges_std

##
# I/O
#

def loadDict(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> [b], i.e. store all values attached to a given key."""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
        try:
            mapping[nodeID].append(compID)
        except KeyError:
            mapping[nodeID] = [compID]
    f.close()
    return mapping

def loadMapping(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
        mapping[nodeID] = compID
    f.close()
    return(mapping)

def loadMappingInt(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],int(lineItems[valueIndex-1])
        mapping[nodeID] = compID
    f.close()
    return(mapping)

def loadMappingWithHeader(fileName,headerChar="#",split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    headerList = []
    for line in f:
        if line.startswith(headerChar):
            line = line.strip(headerChar).strip()
            headerList.append(line)
        elif line:
            lineItems = line.strip().split(split_char)
            nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
            mapping[nodeID] = compID
    f.close()
    try:
        return(mapping,headerList[1])
    except IndexError:
        return(mapping,headerList)

def outputEdgesDict_Weights(edges_dict,edges_std=None,outFile=None,sep=None):
    """Outputs the new graph as an edgefile between communities."""
    print("Writing "+outFile)
    output = open(outFile,"w")
    for edge,weight in iter(edges_dict.items()):
        head = str(edge[0])
        tail = str(edge[1])
        mean = weight
        try:
            std = math.sqrt(edges_std[edge]-mean**2)
        except:
            std = 0
        outString = """%s\t%s\t%.3f\t%.3f\n""" % (head,tail,mean,std)
        output.write(outString)
    output.close()

def outputEdgesDict_NoWeights(edges_dict,outFile=None,sep=None):
    """Outputs the new graph as an edgefile between communities."""
    print("Writing "+outFile)
    output = open(outFile,"w")
    for edge,weight in iter(edges_dict.items()):
        head = str(edge[0])
        tail = str(edge[1])
        outString = """%s\t%s\t%.2f\n""" % (head,tail,1+math.log(weight))
        output.write(outString)
    output.close()

def outputDict(dico,outFile,sep=None):
    g = open(outFile,'w')
    for key,val in iter(dico.items()):
        outString = str(key)+sep+str(val)+"\n"
        g.write(outString)
    g.close()

def outputFile(dictionary,outfile=None,sep=None,header=None):
    """Outputs the dictionary of new node names."""
    f = open(outfile,'w')
    if header:
        wdString = """# Root directory: %s""" % os.getcwd()
        header += "\n"+wdString
        f.write("# "+header+"\n")
    for i,v in iter(dictionary.items()):
        outString = str(i)+sep+str(v)+"\n"
        f.write(outString)
    f.close()

def outputTrailFile(dictionary,trail_file,outfile=None,sep=None,header=None):
    """
    Outputs the dictionary of new node names; if a trailing file old_node -> node was given, it will take the form old_node -> new_node, and bypass the current name of node.
    Beware: if some nodes that are present in the trail_file are not renumbered by the dictionary, an exception will be raised! Update: silently ignore them since they
    should be absent from the new network. Pb: is this really the case?
    """
    trail,wd = loadMappingWithHeader(trail_file)
    f = open(outfile,'w')
    if header:
        wdString = """# %s""" % wd
        header += "\n"+wdString        
        f.write("# "+header+"\n")
    for i,v in iter(trail.items()):
        try:
            w = dictionary[v]
            outString = str(i)+sep+str(w)+"\n"
            f.write(outString)
        except KeyError:
            pass
    f.close()

def outputTypeFile(dictionary,type_file,outfile=None,sep=None):
    """
    Outputs the translation of the type_file witht the new identifiers from the communities.
    """
    outDict = defaultdict(set)
    F = open(type_file,'U')
    for line in F:
        n,t = line.strip().split(sep)
        w = dictionary[n]
        outDict[w].add(t)
    F.close()
    f = open(outfile,'w')
    for a,b in iter(outDict.items()):
        B = ','.join(b)
        outString = str(a)+sep+str(B)+"\n"
        f.write(outString)
    f.close()

def printLog(string,log,mode="a"):
    if type(log) == str:
        logHandle = open(log,mode)
    else:
        logHandle = log
    print(string,file=logHandle)

def unMult(dico):
    """remove multiple values from the valueList of a dico"""
    newDico = dict()
    for i,v in iter(dico.items()):
        newDico[i] = list(set(v))
    return(newDico)
    
def adjacencyList(edgeFile,directed=False,header=False,mult=False,split_char="\t",keyIndex=1,valueIndex=2):
    """From an (undirected) edgeFile, compute and print out the adjacency list representation -- in order to be usable with bipartite graphs, we treat sequentially (and separately) the
    nodes that appear as head or tail of the edge.
    Input : a file with two columns a b
    build the dictionaries a -> [b] and b -> [a]"""
    f = open(edgeFile,'U')
    h2t = dict()
    t2h = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
        try:
            h2t[nodeID].append(compID)
        except KeyError:
            h2t[nodeID] = [compID]
        try:
            t2h[compID].append(nodeID)
        except KeyError:
            t2h[compID] = [nodeID]
    f.close()
    if not mult:
        h2t,t2h = unMult(h2t),unMult(t2h)
    return h2t,t2h

def myCompare(a,b,opt):
    if opt == 1:
        c = a and b
    elif opt == 0:
        c = a or b
    elif opt == -1:
        c = not(a or b)
    return c

def inducedSubgraph(networkFile,subnodes,nodeType=None,outFile=None,sep=None):
    myDict = dict(zip(subnodes,[1 for i in subnodes]))
    operators = {1 : 'and', 0 : 'or', -1: 'not'}
    print("Reading "+networkFile)
    f = open(networkFile,"r")
    g = open(outFile,"w")
    op = operators[int(nodeType)]
    opt = int(nodeType)
    for line in f:
        line = line.rstrip()
        lineItems = line.split(sep)
        node1 = lineItems[0]
        node2 = lineItems[1]
        try:
            F1 = myDict[node1]
        except:
            F1 = 0
        try:
            F2 = myDict[node2]
        except:
            F2 = 0
        cond = myCompare(F1,F2,opt)
        if cond:
            g.write(line+"\n")
    f.close()
    g.close()
    print("done")

def myReadGraph(edgeFile):
    try:
        g = Graph.Read_Ncol(edgeFile,directed=False)
    except SystemError as e:
        printLog("""Error while reading %s: %s\nExiting.\nCheck whether any variable names in %s contain white space. If so replace them (with, say "_") and try again.""" % (edgeFile,e,edgeFile),sys.stderr)
        sys.exit(0)
    g.simplify()
    g.summary()
    return(g)

def getAdjlist(g,nodes=None):
    if not nodes:
        nodes = range(g.vcount())
    return(dict([(node,g.neighbors(node)) for node in nodes]))

def detectRepeated(dico,k_init=0,debug=None):
    """
    Find repeated values in dictionary dico, and assemble corresponding keys.
    """
    twins = dict()                   # dictionary key -> groupID_of_twin
    supp = dict()                    # dictionary groupID_of_twin -> {members, common_value_of_this_twin}
    vals = list(set(map(mySort,(list(val) for val in dico.values() if len(val)>=1))))
    ind = range(k_init+len(vals))[k_init:]
    supp2twin = dict(zip(vals,ind))    
    for key,val in iter(dico.items()):
        try:
            Adj = mySort(list(val))             # and convert it into tuple (invariable and uniquely recognisable)
            group = supp2twin[Adj]
            twins[key] = group
            supp[group] = Adj
        except KeyError:
            pass
    return(supp,twins)

def mySort(itemList):
    adj = itemList[:]
    adj.sort()       
    return tuple(adj)

def InvertMap(dico):
    """Given a dictionary key: value, return the dictionary value: list_of_keys_having_value"""
    inv_map = {}
    for k, v in iter(dico.items()):
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)
    return inv_map

def printPartDict(dico,k=0,sortOption=None,display=False,out=False):
    try:
        kk = list(dico.keys())[:]
    except AttributeError:
        print("Error: Empty dictionary")
        return()
    if not sortOption:
        kk.sort()
    else:
        try:
            kk.sort(key=lambda x:int(x))
        except TypeError:
            kk.sort()
    if k == 0:
        k=len(kk)
    else:
        k = min(k,len(kk))
    for i in range(k):
        if display:
            print(str(kk[i])+"\t",)
        else:
            print(kk[i])
        print(dico[kk[i]])
    if out:
        return(dict([(i,dico[i]) for i in kk[:k]]))

def loadNodeType(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = lineItems[keyIndex-1],int(lineItems[valueIndex-1])
        mapping[nodeID] = compID
    f.close()
    return(mapping)

def rawNodeType(edgeFile,split_char="\t",header=None,keyIndex=1,valueIndex=2):
    f = open(edgeFile,'U')
    nodeType = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID1 = lineItems[keyIndex-1].strip()
        nodeID2 = lineItems[valueIndex-1].strip()
        nodeType[nodeID1] = 1
        nodeType[nodeID2] = 2
    f.close()
    return(nodeType)

def readNodes(edgeFile,sep="\t"):
    """More efficient version of the previous function, avoiding try/except: specially designed for ID1\tID2 format for edgeFiles"""
    outList = set([])
    f = open(edgeFile,'U')
    for line in f:
        ID1,ID2 = line.strip().split(sep)[0:2]
        outList.add(ID1)
        outList.add(ID2)
    f.close()
    return list(outList)

def readNodeType(edgeFile,Type=None):
    """With these functions, we return an **integer-valued** dictionary : node -> type""" 
    if Type == '1':          # unipartite graph
        nodeTypes = None   # previous version with attempt to keep memory lower
    elif Type == '2' or not Type:                    # default behaviour: bipartite graph
        nodeTypes = nodeTypeRaw(edgeFile)
    elif type(Type) == str:  # nodeType file given
        nodeTypes = loadMappingInt(Type)
    else:
        sys.exit("Something wrong with the node types")
    return(nodeTypes)

def nodeTypeRaw(edgeFile,split_char="\t",header=None,keyIndex=1,valueIndex=2,part=2):
    """Rather weird nodeType reading function."""
    f = open(edgeFile,'U')
    ind = dict()
    if part == 1:
        ind[1] = 1
        ind[2] = 1
    else:
        ind[1] = 1
        ind[2] = 2
    nodeType = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID = lineItems[keyIndex-1]
        compID = lineItems[valueIndex-1]
        nodeType[nodeID] = ind[1]
        nodeType[compID] = ind[2]
    f.close()
    return(nodeType)

def getHeader(annotFile,split_char="\t"):
    f = open(annotFile,'U')
    line = None
    while not line:
        line = f.readline().strip()                                                # read first line, which should be the header line.
    allFieldNames = line.strip().split(split_char)                                    # ...parse header and get field names...
    headerDict = dict(zip(allFieldNames,range(len(allFieldNames))))
    f.close()
    return(headerDict)

def readConfigFile(configFile):
    XML = parseXML(configFile)
    trailObjects = []
    for trail in XML['trails']:
        #print(dir(trail))
        myKeys = trail.keys
        keyDict = dict()
        for k in myKeys:
            if k.display == 'True':
                keyDict[int(k.Type)] = k.name
        Trail = myTrail(fileName=trail.name,rank=int(trail.rank),attDict=keyDict)
        if Trail.file:
            trailObjects.append(Trail)
    mod = XML['mod'][0]
    myKeys = mod.keys
    keyDict = dict()
    keyDict[0] = mod.name
    for k in myKeys:
        if k.display == 'True':
            keyDict[int(k.Type)] = k.name    
    compObject = myMod(fileName=mod.filename,attDict=keyDict)    
    keyDict = defaultdict(list)
    selectedKeys = set([])
    for attr in XML['attributes']:
        if attr.display == 'True':
            keyDict[int(attr.Type)].append(attr.name)
            selectedKeys.add(attr.name)
    trailObjects.sort(key=lambda x:x.rank)
    return trailObjects,compObject,keyDict,list(selectedKeys),XML

def myIter(iterator):
    if type(iterator) == dict:
        return iterator.items()
    elif type(iterator) == list:               # ?? (i,i) or (i,[i]) ?? #
        return ((i,[i]) for i in iterator)

def conj(count,name):
    if count <= 1:
        return (count,name)
    else:
        return (count,name+"s")

def processOptions(optionList,nodeTypes):
    keyDict = defaultdict(list)
    #print(optionList)
    opt = optionList.strip().split(",")
    for t in nodeTypes:
        for o in opt:
            keyDict[t].append(o)
    return(keyDict)
    
def processOptions0(optionString,nodeTypes):
    """Function to read old-fashioned key option"""
    opt = optionString.strip().split(",")
    keyDict = defaultdict(list)
    for o in opt:
        keyOptions = o.split("-")   # Error when attribute has an "-" (eg E-value)!!!!
        if len(keyOptions) == 1:    # case where attribute is considered for all types
            key = keyOptions[0]
            for t in nodeTypes:
                keyDict[t].append(key)
        else:
            key,val = keyOptions
            vals = val.split(":")
            for t in vals:
                keyDict[int(t)].append(key)
    return keyDict

def printDescription(trailObjects,compObject,keyDict,selectedKeys,handle=sys.stderr):
    for trail in trailObjects:
        printLog(str(trail.file)+" "+str(trail.rank)+" "+str(trail.attribute),handle)
    printLog(str(compObject.file)+" "+str(compObject.attribute),handle)
    printLog(keyDict,handle)
    printLog(selectedKeys,handle)

def describeGraph(nodeType,nodeTypes):
    FORMAT = """Graph has """+"""%d nodes of type %d, """*len(nodeTypes)+""" and %d total nodes"""
    nT = []
    for j in nodeTypes:
        nT.extend([len([nodeType[i] for i in nodeType if nodeType[i] == j]),j])
    nT.append(len(nodeType.keys()))
    print(FORMAT % tuple(nT))

##
# For getTrailHistory
#

def myGetHeader(trailFile):
    f = open(trailFile,'U')
    cmd = f.readline().strip("#").strip()
    wd = f.readline().strip("#").strip().split(":")[1].strip()
    f.close()
    return(cmd,wd)

def trailHist(trailFile):
    cmd,root = myGetHeader(trailFile)
    CMD = cmd.split()
    cmdDict = dict()
    cmdDict['root'] = root
    cmdDict['cmd'] = cmd
    key = False
    while CMD:
        cmdItem = CMD.pop(0)
        if cmdItem.startswith("-"):
            key = cmdItem.strip("-")
        elif key:
            cmdDict[key] = cmdItem.strip("'")
            key = False
    return(cmdDict)

def trailTrack(trailFile):
    trailFile = os.path.join(os.getcwd(),trailFile)
    wd = os.path.dirname(trailFile)
    ## Lecture des fichiers ========================================
    history = [trailFile]
    while trailFile:
        try:
            previous = trailHist(trailFile)
        except IndexError:
            break
        try:
            directory = previous['d']
            wd = os.path.dirname(wd.rstrip("/"))
        except:
            pass
        try:
            trailFile = os.path.join(wd,previous['t'])
            history.append(trailFile)
        except:
            break
    history.reverse()
    return(history)

##
# For Description
#

def mergeDico(dico1,dico2,track=None):
    """
    Given two dictionaries, merge them with the following rules:
    - values of common keys are appended in a list (or in a list extending both value lists) ## Careful: if values are themselves dictionaries, we get a list of dictionaries...
    - disjoint keys are included in the resulting dictionary
    - the track option is here to account for empty annotation dictionaries; if given, then increase the counter with key 'track' (or create it if not yet created) 
    """
    newDico = dict()
    try:
        k1 = set(dico1.keys())
    except AttributeError:        # usually the error comes from an empty merge dictionary
        if track:
            if track in dico2:
                dico2[track] += 1
            else:
                dico2[track] = 1
        return dico2
    try:
        k2 = set(dico2.keys())
    except AttributeError:       # usually the error comes from an empty merge dictionary (idem)
        if track:
            if track in dico1:
                dico1[track] += 1
            else:
                dico1[track] = 1
        return dico1
    k12 = k1.intersection(k2)
    k1 = k1.difference(k12)
    k2 = k2.difference(k12)
    for k in k12:
        d1 = dico1[k]
        d2 = dico2[k]
        if type(d1) == list:
            newDico[k] = d1[:]
            if type(d2) == list:
                newDico[k].extend(d2)
            else:
                newDico[k].append(d2)
        else:
            if type(d2) == list:
                newDico[k] = d2[:]
                newDico[k].append(d1)
            else:
                newDico[k] = [d1,d2]
    for k in k1:
        newDico[k] = dico1[k]
    for k in k2:
        newDico[k] = dico2[k]
    return newDico

### TrailObjects:

def formatTrailList(trailOption):
    """Version with the myFile class objects"""
    trailList = []              # store the trailFile names
    try:
        trailOptionList = trailOption.strip().split(",")
    except AttributeError:
        return(trailList)
    trailNb = len(trailOptionList)
    k = 1
    for trail in trailOptionList:
        try:
            keyNames,trailName = trail.split("=")
            keyNames_byType = keyNames.split(":")
        except:
            trailName = trail
            keyName = "Key_"+str(k)
            keyNames_byType = [keyName]
        typeNb = len(keyNames_byType)
        keyDict = dict(zip(list(map(lambda x:x+1,range(typeNb))),keyNames_byType))
        myTrail = myFile(fileName=trailName,rank=k,attDict=keyDict)
        k += 1
        trailList.append(myTrail)
    return(trailList)

def formatComp(compOption):
    try:
        comp = compOption.split("=")
    except AttributeError:
        comp = [compOption]
    if len(comp) > 1:
        keyNames,compFile = comp
        keyNames_byType = keyNames.split(":")
    else:
        compFile = comp[0]
        keyName = ""
        keyNames_byType = [keyName]
    typeNb = len(keyNames_byType)
    keyDict = dict(zip(list(map(lambda x:x,range(typeNb))),keyNames_byType))
    Comp = myComp(fileName=compFile,rank=0,attDict=keyDict)        
    return(Comp)

### Annotations

def restrictAnnot(annotFile,tempFile=None,split_char="\t",mainKey=None,valueKeyList=None):
    if not valueKeyList:
        sys.exit("No annotation keys given: exiting.")
    header = getHeader(annotFile)
    KEYS = [mainKey]
    KEYS.extend(valueKeyList)
    indices = list(map(lambda x:str(header[x]+1),KEYS))
    indList = ",".join(indices)
    if not tempFile:
        randID = str(random.randint(1000000,10000000))
        tempFile = randID+".annot"
    cmd = """cut -f %s %s > %s""" % (indList,annotFile,tempFile)
    proc = Popen(args=[cmd],shell=True,executable = "/bin/bash")
    proc.communicate()
    fileDict,fields = myLoadAnnotations(tempFile,mainKey=mainKey,valueKeyList=valueKeyList)
    cmd = """rm %s""" % tempFile
    proc = Popen(args=[cmd],shell=True,executable = "/bin/bash")
    proc.communicate()
    return(fileDict,fields)

def myLoadAnnotations(annotFile,entries=None,split_char="\t",mainKey=None,valueKeyList=None,counter=0):
    """This generic read function can emulate more or less R's read.table behaviour, but with possibly REPEATED indexKeys (as in our annotation Files):
    Input: a tabulated (or whatever split_char'd) file with obligate header with names for all columns.
    Options: 
    mainKey = main column identifier; 
    valueKeyList = list of fields to consider (among header fieldNames; default all); 
    entries =  sublist of key identifiers (line identifiers; default all)
    Output: a dictionary 
    lineId : value 
    where the value is a list of dictionaries {key1 : val1,...}, where the keys are in the header keyList
    Comment: in progress; we try to keep only the relevant information directly: it is not entirely satisfactory, because we have to parse all the annotFile anyway (23/10/2015)
    New comment 30/10/2015: this is so complicated, I don't even see where the bugs are...
    Next comment (27/06/206): maybe selecting all keys when valueKeyList is None is a bad idea: explicitly set to "all" if we want that.
    """
    if not valueKeyList:
        sys.exit("No annotation keys given: exiting.")
    if counter:                
        line_nb = 0
        step = int(counter)
    f = open(annotFile,'U')
    line = None
    k = 0
    if entries:                                                                    # this option seems to imply a very bad time performance
        entrySet = set(entries)
    fileDict = myDict()                                                            # will store the correspondence lineID -> valueDict 
    while not line:
        line = f.readline().strip()                                                # read first line, which should be the header line.
    ## Set fieldNames by reading the first non header line ===================================================================
    allFieldNames = line.strip().split(split_char)                                 # ...parse header and get field names...
    origKeys = allFieldNames[:]
    origKeys.remove(mainKey)
    indices = None
    if type(valueKeyList) == list:                                                 # NB: if we give the valueKeyList, we have to add the mainKey to extract all the relevant fields
        if len(valueKeyList) == 1 and valueKeyList[0] == 'all':
            fieldNames = allFieldNames
        else:
            origKeys = valueKeyList[:]
            valueKeyList[:0] = [mainKey]
            indices = [allFieldNames.index(i) for i in valueKeyList]
            fieldNames = [allFieldNames[i] for i in indices]
    else:
        fieldNames = None
        printLog("No annotation keys given: no output. Please specify keys with -k option or in the XML configuration file",sys.stderr)
        sys.exit(0)
    for line in f:
        if counter:
            line_nb += 1
            if line_nb % step == 0 :
                print(str(line_nb))
        fields = list(map(lambda x:x.strip(),line.strip().split(split_char)))
        if indices:
            fields = [fields[i] for i in indices]
        tempDict = myDict0(keys=fieldNames,values=fields)                          # we store temporarily the dictionary of values corresponding to line until we know if we have to store it or not
        keyVal = tempDict[mainKey]
        try:
            flag = keyVal in entries
            if flag:
                fileDict[keyVal] = tempDict 
                if mainKey not in origKeys:
                    try:
                        del fileDict[keyVal][mainKey]
                    except:
                        print(mainKey,keyVal,tempDict)
        except:
            fileDict[keyVal] = tempDict 
            if mainKey not in origKeys:
                try:
                    del fileDict[keyVal][mainKey]
                except:
                    print(mainKey,keyVal,tempDict)
        k += 1
    f.close()
    return(fileDict,fieldNames)

### Components (or modules)

def loadComponentFile(compFile):
    dico = loadDict(compFile,keyIndex=2,valueIndex=1)
    return dico

def mapValues(dico,keyList):
    return list(map(lambda x:dico.myGetKey(x),keyList))

def reduceDict(dico,track=None):
    newDico = dict()
    for i in dico.keys():
        if isinstance(dico[i],list):
            try:
                newDico[i] = dict(Counter(dico[i]))
            except TypeError:
                newDico[i] = dico[i]
        elif i == track:
            newDico[i] = dico[i]
        else:
            newDico[i] = {dico[i]: 1}
    return newDico

def reduceAnnot(compList,track=None):
    outAnnot = dict()
    for w in compList:
        outAnnot = mergeDico(outAnnot,w,track=track)
    composition = reduceDict(outAnnot,track=track)
    return composition

def nodeType(edgeFile,split_char="\t",header=None,keyIndex=1,valueIndex=2):
    f = open(edgeFile,'U')
    nodeType = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        try:
            nodeID, compID = int(lineItems[keyIndex-1]),int(lineItems[valueIndex-1])
        except ValueError:
            nodeID, compID = lineItems[keyIndex-1],lineItems[valueIndex-1]
        nodeType[nodeID] = 1
        nodeType[compID] = 2
    f.close()
    return nodeType

def loadIntMapping(fileName,header=False,split_char="\t",keyIndex=1,valueIndex=2):
    """Given a file with several columns, select column a with keyIndex column b with valueIndex, and build the dictionary a -> b
    Careful: in case of multiple keys, only stores the last one!! (see loadDict)"""
    f = open(fileName,'U')
    mapping = dict()
    if header:
        f.readline()
    for line in f:
        lineItems = line.strip().split(split_char)
        nodeID, compID = int(lineItems[keyIndex-1]),int(lineItems[valueIndex-1])
        mapping[nodeID] = compID
    f.close()
    return mapping

def myGetHeader(trailFile):
    f = open(trailFile,'U')
    cmd = f.readline().strip("#").strip()
    wd = f.readline().strip("#").strip().split(":")[1].strip()
    f.close()
    return cmd,wd

def trailHist(trailFile):
    cmd,root = myGetHeader(trailFile)
    CMD = cmd.split()
    cmdDict = dict()
    cmdDict['root'] = root
    cmdDict['cmd'] = cmd
    key = False
    while CMD:
        cmdItem = CMD.pop(0)
        if cmdItem.startswith("-"):
            key = cmdItem.strip("-")
        elif key:
            cmdDict[key] = cmdItem.strip("'")
            key = False
    return cmdDict

