#!/usr/bin/python3

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of multitwin.
        
        multitwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import os
import argparse
import sys
import threading
from ttkthemes import themed_tk as tk 
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton, Radiobutton, Scrollbar, Combobox, OptionMenu, Style
from tkinter.constants import HORIZONTAL, VERTICAL, N,S,E,W, END, LEFT, RIGHT, X, Y, YES, NW, BOTTOM
from tkinter import Tk, StringVar, BooleanVar, BOTH, W, E, Canvas
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from utils import CreateToolTip,HelpWindow,center
import description

WIDTH=40

class MyGUI:
    
        def __init__(self, master,title=None,args=None):

                self.master = master
                self.args = args
                self.name = title
                master.title("Startup interface for %s" % title)
                self.arguments = dict()

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

                row = 0
                column = 0
                
                # Input edge file
                self.inEdgeLabel = Label(master, text = "Input edge file")
                self.inEdgeLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.inEdgeFile = StringVar()
                if self.args.i:
                        self.inEdgeFile.set(self.args.i)
                self.inEdgeEntry = Entry(master, width = WIDTH, textvariable = self.inEdgeFile)
                column += 1
                self.inEdgeEntry.grid(row=row,column=column, padx=3)
                self.inEdgeSelect = Button(master, text = "Select",\
                                           command = lambda: self.setOutputFiles2(IN=self.inEdgeFile,OUT=[(self.configFile,"config"),(self.outFile,"desc"),(self.outFile2,"xml_desc")]))
                column += 1
                self.inEdgeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText1 = "Edge file for input graph (two columns, tab-delimited)."
                self.inEdgeTip = CreateToolTip(self.inEdgeEntry, helpText1)
                ##
                row += 1
                column = 0

                self.annotLabel = Label(master, text = "Annotation file")
                self.annotLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.a = StringVar()
                if self.args.a:
                        self.a.set(os.path.abspath(os.path.normpath(self.args.a)))
                self.annotEntry = Entry(master, width = WIDTH, textvariable = self.a)
                column += 1
                self.annotEntry.grid(row=row,column=column, padx=3)
                self.annotSelect = Button(master, text = "Select", command = lambda: self.openAnnotFile(var=self.a))
                column += 1
                self.annotSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                CreateToolTip(self.annotEntry,"Common annotation file for genomes and genes.\nTab-delimited, compulsory header with attribute names.\nSpecify empty annotations with '-'.")
                row += 1
                column = 0
                
                self.k = StringVar()
                if self.a.get():
                        with open(self.a.get(),'r') as ANNOT:
                                keyList = ANNOT.readline().strip().split("\t")[1:]
                                #print(keyList)
                                keyList.sort()
                                keyString = ",".join(keyList)
                        self.optionLabel = Label(master, text = "Annotation keys")
                        self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                        self.k = StringVar()
                        self.k.set(keyString)
                        self.optionEntry = Entry(master, width = WIDTH, textvariable = self.k)
                        self.optionEntry.grid(row=row,column=1, padx=3)
                        self.optionLabel2 = Label(master, text = "comma-separated")
                        self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                        CreateToolTip(self.optionEntry,"List of available attributes in file %s.\nIf you wish to remove some, click on line and edit." % self.args.a)
                row += 1

                self.configLabel = Label(master, text = "Configuration file")
                self.configLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.configFile = StringVar()
                self.generateConfig = BooleanVar()
                self.generateConfig.set(bool(self.args.X))
                self.useConfig = BooleanVar()
                self.useConfig.set(bool(self.args.x))                
                if self.args.x or self.args.X:
                        if self.args.x and self.args.X:
                                if self.args.x == self.args.X:
                                        cFile = self.args.x
                                        self.configFile.set(cFile)
                                else:
                                        sys.exit("Conflicting fields -x and -X. Check and run again.")
                        elif self.args.x:
                                cFile = self.args.x
                        else:
                                cFile = self.args.X
                        self.configFile.set(cFile)
                else:
                        self.configFile.set('')
                self.configEntry = Entry(master, width = WIDTH, textvariable = self.configFile)
                column += 1
                self.configEntry.grid(row=row,column=column, padx=3)
                self.configSelect = Button(master, text = "Select", command = lambda: self.setFile(var1=self.configFile,var2=self.outTrailFile))
                column += 1
                self.configSelect.grid(row=row,column=column, sticky=W, padx=3)
                """self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                """
                # tip
                helpText3 = "XML file specifying component, trails and annotations for all node types."
                self.configTip = CreateToolTip(self.configEntry, helpText3)
                #
                column += 1
                #row += 1
                #column = 0
                
                cbFrame = Frame(master)
                chk1 = Checkbutton(cbFrame, text="Generate", var = self.generateConfig)
                chk1.pack(side="left", fill=None, expand=False, padx=3) 
                CreateToolTip(chk1, "Generate configuration file %s" % self.configFile.get())
                chk2 = Checkbutton(cbFrame, text="Use", var = self.useConfig)
                chk2.pack(side="left", fill=None, expand=False, padx=3) 
                CreateToolTip(chk2, "Use configuration file %s" % self.configFile.get())
                cbFrame.grid(row=row,column=column,sticky=W)
                row += 1
                column = 0
                
                self.TrailLabel = Label(master, text = "Use trail file")
                self.TrailLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.inTrailFile = StringVar()
                self.T = StringVar()
                if self.args.t:
                        self.T.set("1")
                        self.inTrailFile.set(self.args.t)
                elif self.args.H:
                        self.T.set("2")
                        self.inTrailFile.set(self.args.H)
                else:
                        self.T.set("0")
                MODES = [("No", "0"),("Unique level", "1"),("Follow history", "2"),]
                trailVal = {"0": "Toto", "1": self.inTrailFile.get(), "2": self.inTrailFile.get()}
                helpVal = {"0": "Do not use trail file.\nCheck that annotations refer to IDs of current graph.",
                           "1": "Use only level described by trail file.", "2": "Use all levels found in the trail history."}
                rbFrame = Frame(master)  # create subframe for radiobuttons
                i = 0
                MODE = MODES[0]
                b = Radiobutton(rbFrame, text=MODE[0], variable=self.T, value=MODE[1], command = lambda: self.inTrailFile.set(''))
                # tip
                CreateToolTip(b,helpVal[str(i)])
                ##
                b.pack(side="left", fill=None, expand=False, padx=3)
                for text,mode in MODES[1:]:
                        b = Radiobutton(rbFrame, text=text, variable=self.T, value=mode, command = lambda: self.openFileCheck(var=self.inTrailFile))
                        # tip
                        CreateToolTip(b,helpVal[mode])
                        ##
                        b.pack(side="left", fill=None, expand=False, padx=3)
                rbFrame.grid(row=row,column=1)
                row += 1
                column = 0

                self.inTrailLabel = Label(master, text = "Trail file")
                self.inTrailLabel.grid(row=row,column=column, sticky=W, padx=18)
                #self.inTrailEntry = Entry(master, width = WIDTH, textvariable = self.inTrailFile)

                self.inTrailEntry = Entry(master, width = WIDTH, textvariable = self.inTrailFile, validate='focusin',validatecommand = lambda: self.T.set("2"))
                CreateToolTip(self.inTrailEntry,"""Select node type file for multipartite graphs.\nThis will reset the partiteness to "Multipartite".""")
                
                column += 1
                self.inTrailEntry.grid(row=row,column=column, padx=3)
                self.inTrailSelect = Button(master, text = "Select", command = lambda: self.openFile2(var=self.inTrailFile,var2=self.T,value="2"))
                column += 1
                self.inTrailSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "if option set")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText3 = "Links IDs of current graph to IDs of ROOT graph (two columns, tab-delimited).\nIf skipped, current graph is considered ROOT."
                self.inTrailTip = CreateToolTip(self.inTrailEntry, helpText3)
                #
                """
                cbFrame = Frame(master)
                self.uniqueTrail = BooleanVar()
                chk1 = Checkbutton(cbFrame, text="Unique trail file", var = self.uniqueTrail)
                chk1.pack(side="left", fill=None, expand=False, padx=3) 
                CreateToolTip(chk1, "Consider only level given by %s" % self.inTrailFile.get())
                self.history = BooleanVar()
                chk2 = Checkbutton(cbFrame, text="Use trail history", var = self.history)
                chk2.pack(side="left", fill=None, expand=False, padx=3) 
                CreateToolTip(chk2, "Follow trail history of trail file %s" % self.inTrailFile.get())
                cbFrame.grid(row=row,column=1)
                """
                row += 1
                column = 0
                
                # Component file
                self.CompLabel = Label(master, text = "Component file ")
                self.CompLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.CompFile = StringVar()
                if self.args.c:
                        self.CompFile.set(self.args.c)
                self.CompEntry = Entry(master, width = WIDTH, textvariable = self.CompFile)
                column += 1
                self.CompEntry.grid(row=row,column=column, padx=3)
                self.CompSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.CompFile))
                column += 1
                self.CompSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText3 = "Links a nodeID and its neighbours to the twin class ID.\nThis is usually an overlapping clustering.\nIf left empty, consider nodes of current graph as components."
                self.CompTip = CreateToolTip(self.CompEntry, helpText3)
                ##
                row += 1
                column = 0

                # Partiteness options
                self.inNodeLabel = Label(master, text = "Partiteness")
                self.inNodeLabel.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                MODES = [("Unipartite", "1"),("Bipartite", "2"),]
                self.inNodeType = StringVar()
                self.v = StringVar()
                if str(self.args.N) == '1' or str(self.args.N) == '2':
                        self.v.set(self.args.N) # initialize at value
                elif self.args.N:
                        self.v.set("m")
                        self.inNodeType.set(self.args.N)
                else:
                        self.v.set("2")
                rbFrame = Frame(master)  # create subframe for radiobuttons
                for text,mode in MODES:
                        b = Radiobutton(rbFrame, text=text, variable=self.v, value=mode, command = lambda: self.inNodeType.set(''))
                        # tip
                        CreateToolTip(b,"Select if graph is %s" % text.lower())
                        ##
                        b.pack(side="left", fill=None, expand=False, padx=3)
                b = Radiobutton(rbFrame, text="Multipartite", variable=self.v, value="m", command = lambda: self.openFile(var=self.inNodeType))
                CreateToolTip(b,"Select if graph is multipartite.\nThis will open a select box for the node type file.")
                b.pack(side="left", fill=None, expand=False, padx=3)                        
                rbFrame.grid(row=row,column=column, padx=3)
                row += 1
                column = 0
                self.Label = Label(master, text = "Node type file")
                self.Label.grid(row=row,column=column, sticky=W, padx=18)
                self.inNodeEntry = Entry(master, width = WIDTH, textvariable = self.inNodeType, validate='focusin',validatecommand = lambda: self.v.set("m"))
                CreateToolTip(self.inNodeEntry,"""Select node type file for multipartite graphs.\nThis will reset the partiteness to "Multipartite".""")
                column += 1
                self.inNodeEntry.grid(row=row,column=column, padx=3)
                self.inNodeSelect = Button(master, text = "Select", command = lambda: self.openFile2(var=self.inNodeType,var2=self.v,value="m")) # reset value to "multipartite" when type file is chosen.
                column += 1
                self.inNodeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "for multipartite only")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                CreateToolTip(self.inNodeSelect,"""Select node type file for multipartite graphs.\nThis will reset the partiteness to "Multipartite".""")
                row += 1
                column = 0

                # Output file
                self.outLabel = Label(master, text = "Output plain file")
                self.outLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outFile = StringVar()
                if self.args.o:
                        self.outFile.set(self.args.o)
                self.outEntry = Entry(master, width = WIDTH, textvariable = self.outFile)
                column += 1
                self.outEntry.grid(row=row,column=column, padx=3)
                self.outSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.outFile))
                column += 1
                self.outSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText2 = "Set name of the plain text description file"
                self.outTip = CreateToolTip(self.outEntry, helpText2)
                ##
                row += 1
                column = 0

                # Output file
                self.outLabel2 = Label(master, text = "Output XML file")
                self.outLabel2.grid(row=row,column=column, sticky=W, padx=3)
                self.outFile2 = StringVar()
                if self.args.O:
                        self.outFile.set(self.args.O)
                self.outEntry2 = Entry(master, width = WIDTH, textvariable = self.outFile2)
                column += 1
                self.outEntry2.grid(row=row,column=column, padx=3)
                self.outSelect2 = Button(master, text = "Select", command = lambda: self.openFile(var=self.outFile2))
                column += 1
                self.outSelect2.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText2 = "Set name of the XML description file"
                self.outTip = CreateToolTip(self.outEntry2, helpText2)
                ##
                row += 1
                column = 0

                self.optionLabel = Label(master, text = "Unique node identifier")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.I = StringVar()
                if self.args.I:
                        self.I.set(self.args.I)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.I)
                self.optionEntry.grid(row=row,column=1, padx=3)
                CreateToolTip(self.optionEntry,"""Name of first column in annotation %s file.\nCheck that the items in this column match the node IDs in the ROOT graph.""" % os.path.basename(self.a.get()))
                row += 1
                column = 0

                self.trackLabel = Label(master, text = "Missing annotation label")
                self.trackLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.trackName = StringVar()
                if self.args.T:
                        self.trackName.set(self.args.T)
                self.trackEntry = Entry(master, width = WIDTH, textvariable = self.trackName)
                column += 1
                self.trackEntry.grid(row=row,column=column, padx=3)
                # tip
                helpText3 = "Name replacing missing annotations"
                self.trackTip = CreateToolTip(self.trackEntry, helpText3)
                #
                column += 2
                
                self.Track = BooleanVar()
                chk1 = Checkbutton(master, text="Skip", var = self.Track)
                CreateToolTip(chk1, "Skip missing annotations")
                chk1.grid(row=row,column=column,sticky=W,padx=9)
                row += 1
                column = 0

                self.optionLabel = Label(master, text = "Graphic interface for %s" % self.configFile.get())
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.K = BooleanVar()
                self.K.set(self.args.K)
                self.chk = Checkbutton(master, text="Display?", var = self.K)
                self.chk.grid (row=row,column=1,padx=3,sticky=W)
                CreateToolTip(self.chk,"Displays graphic customization interface for the last description.py step.\nIf not selected, displays all attributes for all key types and all trail levels.")
                row += 1
                column = 0
                # Log
                self.optionLabel = Label(master, text = "Log file")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.l = StringVar()
                try:
                        log = self.args.l.name.strip("(<,>")
                except:
                        log = log
                self.l.set(log)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.l)
                self.optionEntry.grid(row=row,column=1, padx=3)
                row += 2

                # Populate outFiles if edge file given
                if self.args.i:
                        self.setOutputFiles2(IN=self.inEdgeFile,OUT=[(self.configFile,"config"),(self.outFile,"desc"),(self.outFile2,"xml_desc")],OPEN=False)
                
                cbFrame = Frame(master)  # create subframe for command buttons

                self.run_button = Button(cbFrame, text="Run", command=self.run)
                self.run_button.grid(row=row,column=0,padx=12)
                
                self.close_button = Button(cbFrame, text="Close", command=self.Quit)
                self.close_button.grid(row=row,column=1,padx=12)

                cbFrame.grid(row=row,column=1,columnspan=2,sticky=E+W)

                helpText = description.processArgs().format_help()
                self.helpbutton = Button(master, text="Help", command = lambda: HelpWindow(text=helpText,name=self.name))
                self.helpbutton.grid(row=row,column=2,sticky=W,padx=3)

        def func(self,value):
                print("Set %s " % value)

        def setFile(self,var1=None,var2=None):
                self.openFile(var=var1)
                modfile = os.path.split(var1.get())[1]
                var2.set(modfile)
                self.master.update_idletasks()

        def setOutputFiles(self,IN=None,TWIN=None,TWINCOMP=None):
                self.openFile(var=IN)
                inFile = os.path.split(IN.get())[1]
                inRad = inFile.split(".")[0]
                twin = inRad+".twins"
                twinComp = inRad+".twin_comp"
                TWIN.set(twin)
                TWINCOMP.set(twinComp)
                self.master.update_idletasks()

        def setOutputFiles2(self,IN=None,OUT=None,OPEN=True):
                if OPEN:
                        self.openFile(var=IN)
                inFile = os.path.split(IN.get())[1]
                inRad = inFile.split(".")[0]
                for items in OUT:
                        FILE,EXT = items
                        FILE.set(inRad+"."+EXT)
                self.master.update_idletasks()
                
        def openFile(self,var=None):
                var.set(askopenfilename())

        def openFileCheck(self,var=None):
                if not var.get():
                        var.set(askopenfilename())

        def openFile2(self,var=None,var2=None,value=None):
                var.set(askopenfilename())
                var2.set(value)
                self.master.update_idletasks()

        def openAnnotFile(self,var=None):
                var.set(askopenfilename())
                row = 2
                master = self.master
                try:
                        with open(var.get(),'r') as ANNOT:
                                keyList = ANNOT.readline().strip().split("\t")[1:]
                                #print(keyList)
                                keyList.sort()
                                keyString = ",".join(keyList)
                except FileNotFoundError:
                        return
                self.optionLabel = Label(master, text = "Annotation keys")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.k = StringVar()
                self.k.set(keyString)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.k)
                self.optionEntry.grid(row=row,column=1, padx=3)
                self.optionLabel2 = Label(master, text = "comma-separated")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                ann = os.path.basename(self.a.get())
                CreateToolTip(self.optionEntry,"""List of available attributes in file %s.\nIf you wish to remove some, click on line and edit.""" % ann)
                self.master.update_idletasks()
                RHeight = self.master.winfo_reqheight()
                RWidth = self.master.winfo_reqwidth()
                self.master.geometry(("%dx%d+300+300") % (RWidth,RHeight))
                center(self.master)
                
        def Quit(self,event=None):
                self.master.destroy()
        
        def run(self,event=None):
                self.arguments['edgeFile'] = self.inEdgeFile.get()
                self.arguments['annotFile'] = self.a.get()
                if self.k.get():
                        #print("KeyList defined: %s" % self.k.get()) 
                        self.arguments['keyList'] = self.k.get()
                if self.useConfig.get():
                        self.arguments['x'] = self.configFile.get()
                if self.generateConfig.get():
                        self.arguments['X'] = self.configFile.get()
                if self.T.get() == '1':
                        self.arguments['trail'] = self.inTrailFile.get()
                elif self.T.get() == '2':
                        self.arguments['hist'] = self.inTrailFile.get()
                self.arguments['comp'] = self.CompFile.get()
                if self.v.get() == '1' or self.v.get() == '2':
                        self.arguments['NodeType'] = self.v.get()
                else:
                        self.arguments['NodeType'] = self.inNodeType.get()
                self.arguments['outFile'] = self.outFile.get()
                self.arguments['Xout'] = self.outFile2.get()
                self.arguments['log'] = self.l.get()
                if self.arguments['log'] == 'stderr':
                        self.arguments['log'] = sys.stderr
                self.arguments['sep'] = self.args.s
                self.arguments['track'] = self.trackName.get()
                self.arguments['empty'] = self.Track.get()
                if self.K.get():
                        self.arguments['K'] = self.K
                else:
                        self.arguments['display'] = True
                if self.k.get():
                        self.arguments['keyList'] = self.k.get()
                if self.I.get():
                        self.arguments['nodeID'] = self.I.get()
                self.arguments = renorm(self.arguments)
                self.master.destroy()

def renorm(dico):
        for k in dico:
                if dico[k] == 'None':
                        dico[k] = None
        return(dico)

def main(prog,args=None):
        root = tk.ThemedTk()
        root.configure(background="lightgrey")
        s = Style()
        s.theme_use('radiance')
        root.minsize(width=500,height=200)
        my_gui = MyGUI(root,title=prog,args=args)
        root.update_idletasks()
        RHeight = root.winfo_reqheight()
        RWidth = root.winfo_reqwidth()
        root.geometry(("%dx%d+300+300") % (RWidth,RHeight))
        args = my_gui
        root.bind("<Return>", my_gui.run)
        root.bind("<Escape>", my_gui.Quit)
        center(root)
        root.wait_window(my_gui.master)
        try:
                #print(args.arguments)
                description.Main(**args.arguments)
        except:
                root.destroy

def processArgs(prog):
        """ Parser function of main """
        parser = argparse.ArgumentParser(description='Configures and launches the %s software' % prog)
        return(parser)

if __name__ == '__main__':
        prog = sys.argv[0].split("/")[-1]
        parser = processArgs(prog)
        args = parser.parse_args()
        CMD = " ".join(sys.argv)
        print(vars(args))
        main(prog)
