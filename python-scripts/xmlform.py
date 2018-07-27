#!/usr/bin/python3

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of multitwin.
        
        multitwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import sys
import argparse
import os
from xml.etree import ElementTree as ET

from ttkthemes import themed_tk as tk 
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton, Scrollbar, Style,Separator
from tkinter.constants import HORIZONTAL, VERTICAL, N,S,E,W, END, LEFT, RIGHT, X, Y, YES, NW, BOTTOM
from tkinter import Tk, StringVar, BooleanVar, BOTH, W, E, Canvas
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from utils import CreateToolTip,HelpWindow,center
import description

WIDTH=30

def printf (format, *args):
        sys.stdout.write (format % args)

def fprintf (fp, format, *args):
        fp.write (format % args)

# get an XML element with specified name
def getElement (parent,name):
        return(parent.findall(name))

# get value of an XML element with specified name
def getElementValue (parent,name):
        return(parent.find(name).text)

# set value of an XML element with specified name
def setElementValue (parent,name,value):
        parent.find(name).text = value
        
# set value of an XML element with specified name
def setElementAttribute (parent, attribute, value):
        parent.set(attribute,value)
        
class xmlModule():

        def __init__(self,mod):
                self.xml = mod
                self.ModFile = StringVar()
                try:
                        self.ModFile.set(getElementValue (mod,"filename"))
                except AttributeError:
                        self.ModFile.set('')
                self.ModName = StringVar()
                self.ModName.set (getElementValue (mod,"name"))
                self.Keys = dict()
                for Key in getElement (mod,"key"):
                        i = int(Key.attrib['type'])
                        self.Keys[i] = mod_Key(Key)

class xmlTrail():

        def __init__(self,trail):
                self.xml = trail
                self.rank = int(getElementValue(trail,"rank"))
                self.filename = getElementValue(trail,"filename")
                #self.filename = os.path.relpath(getElementValue(trail,"filename"), start=self.RootDir)
                self.Keys = dict()
                for Key in getElement (trail,"key"):
                        i = int(Key.attrib['type'])
                        self.Keys[i] = mod_Key(Key)

class mod_Key():

        def __init__(self,modKey):
                self.xml = modKey
                self.type = modKey.attrib['type']
                self.display = BooleanVar()
                try:
                        self.display.set(eval(modKey.attrib['display']))
                except:
                        self.display.set(False)
                self.name = StringVar()
                self.name.set (getElementValue(modKey, "name"))

class Attr():

        def __init__(self,attr):
                self.xml = attr
                self.name = getElementValue(attr,"name")
                self.Keys = dict()
                for node in getElement (attr,"node"):
                        i = int(node.attrib['type'])
                        self.Keys[i] = xmlKey(node)

class xmlKey():

        def __init__(self,node):
                self.xml = node
                self.display = BooleanVar()
                try:
                        self.display.set(eval(node.attrib['display']))
                except:
                        self.display.set(False)
                                                
class Application (Frame):

        def __init__(self, parent, XML=None):

                # initialize frame
                Frame.__init__(self,parent)

                style = Style()
                style.configure(".",background="lightgrey")
                
                labelStyle = Style()
                labelStyle.configure("TLabel", background="lightgrey")
                buttonStyle = Style()
                buttonStyle.configure("TButton", background = "lightgrey")
                chkbuttonStyle = Style()
                chkbuttonStyle.configure("TCheckbutton", background = "lightgrey")
                rbuttonStyle = Style()
                rbuttonStyle.configure("TRadiobutton", background = "lightgrey")

                self.XML = XML
                
                self.returnValue = None

                # set root as parent
                self.parent = parent

                # read and parse XML document
                self.DOMTree = ET.parse(self.XML)

                # create attribute for XML document
                self.xmlDocument = self.DOMTree.getroot()

                # create attribute for root directory
                self.RootDir = getElementValue (self.xmlDocument,"root")
                
                # create attribute for "mod" elements
                self.xmlModList = getElement (self.xmlDocument,"mod")

                # create attribute for "trail" elements
                self.xmlTrailList = getElement (self.xmlDocument,"trail")

                # create attribute for "attr" elements
                self.xmlAttrList = getElement (self.xmlDocument,"attr")
                
                # identify node types
                self.nodeTypes = []
                attr =  self.xmlAttrList[0]
                for KEY in getElement (attr,"node"):
                        nT = int(KEY.attrib['type'])
                        self.nodeTypes.append(nT)

                # Module setting
                self.xmlMod = self.xmlModList[0]
                self.mod = xmlModule(self.xmlMod)
                self.mod.KEYS = dict()
                for KEY in getElement (self.xmlMod,"key"):
                        nT = int(KEY.attrib['type'])
                        self.mod.KEYS[nT] = KEY

                # Trails setting
                self.trails = dict()
                for trail in self.xmlTrailList:
                        rank = int(getElementValue(trail,"rank"))
                        self.trails[rank] = xmlTrail(trail)
                        self.trails[rank].KEYS = dict()
                        for KEY in getElement (trail,"key"):
                                nT = int(KEY.attrib['type'])
                                self.trails[rank].KEYS[nT] = KEY

                #Attributes setting
                self.attrs = dict()
                for attr in self.xmlAttrList:
                        name = getElementValue(attr,"name")
                        self.attrs[name] = Attr(attr)
                        self.attrs[name].KEYS = dict()
                        for KEY in getElement (attr,"node"):
                                nT = int(KEY.attrib['type'])
                                self.attrs[name].KEYS[nT] = KEY
                self.M = len(self.xmlModList)
                self.T = len(self.xmlTrailList)
                self.A = len(self.xmlAttrList)
                self.K = len(self.nodeTypes)
                print("""%s displays %d module(s), %d trail file(s) and %d node attribute(s). The graph is %d-partite.""" % (self.XML,self.M,self.T,self.A,self.K))
                
                # initialize UI
                self.initUI()

        def initUI(self):
                # set frame title
                self.parent.title ("Configuration settings for %s" % self.XML)

                # pack frame
                self.pack (fill=BOTH, expand=1)
                
                # configure grid columns
                #NCols = max(3,self.K+1)
                NCols = 3
                for i in range(NCols):
                        self.columnconfigure (i, pad=3)

                # configure grid rows
                NRows = self.M+self.T+self.A
                for i in range(NRows):
                        self.rowconfigure (i, pad=3)                
                row = 0

                label = Label (self,text = "ROOT directory: %s" % self.RootDir)
                label.grid (row=row,columnspan=WIDTH,sticky=W,padx=3)
                row += 1
                
                # Module selection
                # File
                self.compLabel = Label(self, text = "Component file")
                self.compLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.compEntry = Entry(self, width = WIDTH, textvariable = self.mod.ModFile)
                self.compEntry.grid(row=row,column=1, padx=3)
                self.compSelect = Button(self, text = "Select", command = self.selectModFile)
                self.compSelect.grid(row=row,column=2, sticky=W, padx=3)
                helpText1 = "Terminal clustering file whose component's contents one wishes to analyze.\nIf left empty, each node of the graph is a component."
                self.compTip = CreateToolTip(self.compEntry, helpText1)
                row += 1
                # Name
                self.lab1 = StringVar()
                #self.lab1.set("Name of components")
                modfile = os.path.split(self.mod.ModFile.get())[1]
                #comp_name = os.path.relpath(self.mod.ModFile.get(), start=self.RootDir)
                self.lab1.set("Name of components in file %s" %  modfile)
                label1 = Label (self,textvariable = self.lab1)
                label1.grid (row=row,column=0,sticky=W,padx=3)
                entry1 = Entry (self,width=WIDTH,textvariable = self.mod.ModName)
                entry1.grid (row=row,column=1)
                CreateToolTip(entry1, "Name that will identify each component")
                row += 1
                
                # Module keys
                """
                if self.mod.Keys:
                        for nT in self.nodeTypes:
                                label = Label (self,text = "Name of type %d nodes" % nT)
                                label.grid (row=row,column=0,sticky=W,padx=3)

                                entry = Entry (self,width=WIDTH,textvariable = self.mod.Keys[nT].name)
                                entry.grid (row=row,column=1)
                                
                                chk = Checkbutton(self, text="Display?", var = self.mod.Keys[nT].display)
                                chk.grid (row=row,column=2)
                                row +=1
                """        
                # Trails selection
                for trail_index in self.trails:
                        trail = self.trails[trail_index]
                        fname = os.path.relpath(trail.filename, start=self.RootDir)
                        label = Label (self,text = "Trail file ROOT/%s of rank %d" % (fname,trail_index))
                        #label = Label (self,text = "Trail file %s of rank %d" % (trail.filename,trail_index))
                        label.grid (row=row,columnspan=WIDTH,sticky=W,padx=3)
                        row += 1
                        
                        # Trail keys
                        for nT in self.nodeTypes:
                                label = Label (self,text = "Name of type %d nodes" % nT)
                                label.grid (row=row,column=0,sticky=W,padx=3)

                                entry = Entry (self,width=WIDTH,textvariable = trail.Keys[nT].name)
                                entry.grid (row=row,column=1)
                                CreateToolTip(entry, "Name for node of type %d in trail file of rank %d" % (nT,trail_index))

                                chk = Checkbutton(self, text="Display?", var = trail.Keys[nT].display)
                                chk.grid (row=row,column=2,sticky=W)
                                CreateToolTip(chk, "Select if node of type %d should appear in description" % nT)
                                row +=1
                
                Separator(self,orient=HORIZONTAL).grid(row=row, column=0,columnspan=WIDTH,sticky=E+W)
                row += 1
                label = Label (self,text = "List of attributes")
                label.grid (row=row,column=0,sticky=W,padx=3)
                label = Label (self,text = "Display attribute for key type?")
                label.grid (row=row,column=1)
                row += 1
                Separator(self,orient=HORIZONTAL).grid(row=row, column=0,columnspan=WIDTH,sticky=E+W)
                row += 1
                
                # Attributes selection
                for attr_index in self.attrs:
                        attr = self.attrs[attr_index]

                        label = Label (self,text = attr.name)
                        label.grid (row=row,column=0,sticky=W,padx=3)

                        # Attr Keys
                        column = 0
                        cbFrame = Frame(self)
                        for nT in self.nodeTypes:
                                chk = Checkbutton(cbFrame, text="Key "+str(nT), var = attr.Keys[nT].display)
                                chk.pack(side="left", fill=None, expand=False, padx=3) 
                                CreateToolTip(chk, "Select if attribute %s is relevant for node of type %d" % (attr.name,nT))
                        cbFrame.grid(row=row,column=1)
                        row +=1

                # create OK button 
                button1 = Button (self, text="OK", command=self.onOK)
                button1.grid (row=row,column=0,sticky=E)
                self.parent.bind("<Return>", self.onOK)
                
                # create Cancel button
                button2 = Button (self, text="Cancel", command=self.onCancel)
                button2.grid (row=row,column=2,sticky=W)
                self.parent.bind("<Escape>", self.onCancel)

        def selectModFile(self,var=None):
                self.openFile(var=self.mod.ModFile)
                modfile = os.path.split(self.mod.ModFile.get())[1]
                self.lab1.set("Name of components in file %s" %  modfile)
                self.update_idletasks()
                self.parent.canvas.configure(width = self.winfo_reqwidth(), height = self.winfo_reqheight())

                
        def openFile(self,var=None):
                var.set(askopenfilename())
                 
        def onOK(self,event=None): 
                # set values in xml document
                #######################
                setElementValue (self.xmlMod,"filename",self.mod.ModFile.get())
                # Module
                setElementValue (self.xmlMod,"name",self.mod.ModName.get())
                # Module keys
                if self.mod.Keys:
                        for nT in self.nodeTypes:
                                setElementValue (self.mod.Keys[nT].xml,"name",self.mod.Keys[nT].name.get())
                                setElementAttribute (self.mod.Keys[nT].xml,"display", str(self.mod.Keys[nT].display.get()))
                # Trails
                for trail_index in self.trails:
                        trail = self.trails[trail_index]
                        # Trail keys
                        for nT in self.nodeTypes:
                                setElementValue (self.trails[trail_index].Keys[nT].xml,"name",trail.Keys[nT].name.get())
                                setElementAttribute (self.trails[trail_index].Keys[nT].xml, "display", str(trail.Keys[nT].display.get()))
                # Attributes
                for attr_index in self.attrs:
                        attr = self.attrs[attr_index]
                        for nT in self.nodeTypes:
                                setElementAttribute (self.attrs[attr.name].Keys[nT].xml, "display", str(attr.Keys[nT].display.get()))

                # write XML document to XML file
                self.DOMTree.write (self.XML)

                self.returnValue = "Ok"
                # exit program
                self.quit();
                
        def onCancel(self,event=None): 
                # exit program
                self.returnValue = "Cancel"
                self.quit();

def main(xmlFile=None):
        if not xmlFile:
                sys.exit("No configuration file given; exiting")

        def on_configure(event):
                # update scrollregion after starting 'mainloop'
                # when all widgets are in canvas
                canvas.configure(scrollregion=canvas.bbox('all'))

        # initialize root object
        root = tk.ThemedTk()
        root.configure(background="lightgrey")
        s = Style()
        s.theme_use('radiance')

        canvas = Canvas(root)
        canvas.pack(side=LEFT)
        scrollbar = Scrollbar(root, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        canvas.configure(yscrollcommand = scrollbar.set)

        # call object
        app = Application (root,XML=xmlFile)
        
        root.update_idletasks()

        root.canvas = canvas
        
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.bind('<Configure>', on_configure)
        canvas.create_window((0,0), window=app, anchor='nw')
        RHeight = min(700,app.winfo_reqheight())
        RWidth = app.winfo_reqwidth()       
        canvas.configure(width = RWidth, height = RHeight)
        root.bind('<Button-4>', lambda event: canvas.yview_scroll(-1, 'units'))
        root.bind('<Button-5>', lambda event: canvas.yview_scroll(1, 'units'))
        center(root)

        # enter main loop
        root.mainloop()
        return(app.returnValue)

def processArgs():
        """ Parser function of main """
        parser = argparse.ArgumentParser(description='Outputs description files based on an annotation file for a trail history hierarchy of graphs')
        parser.add_argument("xmlFile", help="XML config file",type=str)
        return(parser)
        
        # if this is the main thread then call main() function
if __name__ == '__main__':
        prog = sys.argv[0].split("/")[-1]
        parser = processArgs()
        args = parser.parse_args()
        CMD = " ".join(sys.argv)
        print(vars(args))
        main(xmlFile=args.xmlFile)
