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
import detect_twins

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
                if self.args.input_edge_file:
                        self.inEdgeFile.set(self.args.input_edge_file)
                self.inEdgeEntry = Entry(master, width = WIDTH, textvariable = self.inEdgeFile)
                column += 1
                self.inEdgeEntry.grid(row=row,column=column, padx=3)
                self.inEdgeSelect = Button(master, text = "Select", command = lambda: self.setOutputFiles(IN=self.inEdgeFile,TWIN=self.outTwinFile,TWINCOMP=self.twinCompFile))
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

                # Output twin file
                self.outTwinLabel = Label(master, text = "Output twin file")
                self.outTwinLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outTwinFile = StringVar()
                if self.args.o:
                        self.outTwinFile.set(self.args.o)
                self.outTwinEntry = Entry(master, width = WIDTH, textvariable = self.outTwinFile)
                column += 1
                self.outTwinEntry.grid(row=row,column=column, padx=3)
                self.outTwinSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.outTwinFile))
                column += 1
                self.outTwinSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText2 = "Links a nodeID to its twin class ID (two columns, tab-delimited)."
                self.outTwinTip = CreateToolTip(self.outTwinEntry, helpText2)
                ##
                row += 1
                column = 0

                # Twin component file
                self.twinCompLabel = Label(master, text = "Twin component file ")
                self.twinCompLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.twinCompFile = StringVar()
                if self.args.c:
                        self.twinCompFile.set(self.args.c)
                self.twinCompEntry = Entry(master, width = WIDTH, textvariable = self.twinCompFile)
                column += 1
                self.twinCompEntry.grid(row=row,column=column, padx=3)
                self.twinCompSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.twinCompFile))
                column += 1
                self.twinCompSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText3 = "Links a nodeID and its neighbours to the twin class ID.\nThis is usually an overlapping clustering."
                self.twinCompTip = CreateToolTip(self.twinCompEntry, helpText3)
                ##
                row += 1
                column = 0

                # Populate outFiles if edge file given
                if self.args.input_edge_file:
                        inFile = os.path.split(self.args.input_edge_file)[1]
                        inRad = inFile.split(".")[0]
                        twin = inRad+".twins"
                        twinComp = inRad+".twin_comp"
                        self.outTwinFile.set(twin)
                        self.twinCompFile.set(twinComp)

                # Partiteness options
                self.inNodeLabel = Label(master, text = "Partitneness")
                self.inNodeLabel.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                MODES = [("Unipartite", "1"),("Bipartite", "2"),]
                self.inNodeType = StringVar()
                self.v = StringVar()
                if str(self.args.n) == '1' or str(self.args.n) == '2':
                        self.v.set(self.args.n) # initialize at bipartite
                elif self.args.n:
                        self.v.set("m")
                        self.inNodeType.set(self.args.n)
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
                self.inNodeEntry = Entry(master, width = WIDTH, textvariable = self.inNodeType, validate='focusin',validatecommand = lambda: self.v.set("m"))
                CreateToolTip(self.inNodeEntry,"""Select node type file for multipartite graphs.\nThis will reset the partiteness to "Multipartite".""")
                column += 1
                self.inNodeEntry.grid(row=row,column=column, padx=3)
                self.inNodeSelect = Button(master, text = "Select", command = lambda: self.openFile2(var=self.inNodeType,var2=self.v,value="m")) # reset value to "multipartite" when type file is chosen.
                column += 1
                self.inNodeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "for multipartite")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                CreateToolTip(self.inNodeSelect,"""Select node type file for multipartite graphs.\nThis will reset the partiteness to "Multipartite".""")
                row += 1
                column = 0

                # unilat
                self.twinSelectLabel = Label(master, text = "Restrict to node types")
                self.twinSelectLabel.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                self.unilat = StringVar()
                if self.args.u:
                        self.unilat.set(self.args.u)
                self.twinSelectEntry = Entry(master, width = WIDTH, textvariable = self.unilat)
                self.twinSelectEntry.grid(row=row,column=column, padx=3)
                column += 2
                self.optionLabel2 = Label(master, text = "optional (comma-separated)")
                self.optionLabel2.grid(row=row,column=column, padx=3)
                CreateToolTip(self.twinSelectEntry,"Computes twins for nodes of specified types only.")
                row += 1
                column = 0

                # Min support 
                self.minsuppLabel = Label(master, text = "Minimum support")
                self.minsuppLabel.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                self.minsupp = StringVar()
                if self.args.thr:
                        self.minsupp.set(self.args.thr)
                self.minsuppEntry = Entry(master, width = WIDTH, textvariable = self.minsupp)
                self.minsuppEntry.grid(row=row,column=column, padx=3)
                column += 2
                self.optionLabel2 = Label(master, text = "optional")
                self.optionLabel2.grid(row=row,column=column, padx=3,sticky=W)
                CreateToolTip(self.minsuppEntry,"Returns twins only if their neighbourhood has at least this number of elements.")
                row += 1
                column = 0

                # min size
                self.minsizeLabel = Label(master, text = "Minimum twin size")
                self.minsizeLabel.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                self.minsize = StringVar()
                if self.args.M:
                        self.minsize.set(self.args.M)
                self.minsizeEntry = Entry(master, width = WIDTH, textvariable = self.minsize)
                self.minsizeEntry.grid(row=row,column=column, padx=3)
                column += 2
                self.optionLabel2 = Label(master, text = "optional")
                self.optionLabel2.grid(row=row,column=column, padx=3,sticky=W)
                CreateToolTip(self.minsizeEntry,"Returns twins only if they have at least this number of elements.")
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

                cbFrame = Frame(master)  # create subframe for command buttons

                self.run_button = Button(cbFrame, text="Run", command=self.run)
                self.run_button.grid(row=row,column=0,padx=12)
                
                self.close_button = Button(cbFrame, text="Close", command=self.Quit)
                self.close_button.grid(row=row,column=1,padx=12)

                cbFrame.grid(row=row,column=1,columnspan=2,sticky=E+W)

                helpText = detect_twins.processArgs().format_help()
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
                
        def openFile(self,var=None):
                var.set(askopenfilename())

        def openFile2(self,var=None,var2=None,value=None):
                var.set(askopenfilename())
                var2.set(value)
                self.master.update_idletasks()

        def Quit(self,event=None):
                self.master.destroy()
        
        def run(self,event=None):
                self.arguments['edgeFile'] = self.inEdgeFile.get()
                self.arguments['outFile'] = self.outTwinFile.get()
                self.arguments['comp'] = self.twinCompFile.get()
                self.arguments['unilat'] = self.unilat.get()
                if self.v.get() == '1' or self.v.get() == '2':
                        self.arguments['nodeType'] = self.v.get()
                else:
                        self.arguments['nodeType'] = self.inNodeType.get()
                self.arguments['min_supp'] = self.minsupp.get()
                self.arguments['min_size'] = self.minsize.get()
                self.arguments['log'] = self.l.get()
                if self.arguments['log'] == 'stderr':
                        self.arguments['log'] = sys.stderr
                self.arguments['sep'] = self.args.s
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
                detect_twins.Main(**args.arguments)
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
        main()
