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
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton, Scrollbar, Combobox, OptionMenu, Style
from tkinter.constants import HORIZONTAL, VERTICAL, N,S,E,W, END, LEFT, RIGHT, X, Y, YES, NW, BOTTOM
from tkinter import Tk, StringVar, BooleanVar, BOTH, W, E, Canvas, Toplevel
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from utils import CreateToolTip,HelpWindow,center
import factorgraph

WIDTH=30
                                
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
                
                self.inEdgeLabel = Label(master, text = "Input edge file")
                self.inEdgeLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.inEdgeFile = StringVar()
                if self.args.input_edge_file:
                        self.inEdgeFile.set(self.args.input_edge_file)
                self.inEdgeEntry = Entry(master, width = WIDTH, textvariable = self.inEdgeFile)
                column += 1
                self.inEdgeEntry.grid(row=row,column=column, padx=3)
                self.inEdgeSelect = Button(master, text = "Select", command = lambda: self.setRequiredFiles(IN=self.inEdgeFile,OUT=self.outEdgeFile,TRAIL=self.outTrailFile))
                column += 1
                self.inEdgeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText1 = "Edge file for input graph (two columns, tab-delimited)."
                self.inEdgeTip = CreateToolTip(self.inEdgeEntry, helpText1)
                ##
                column += 2
                
                self.outEdgeLabel = Label(master, text = "Output edge file")
                self.outEdgeLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outEdgeFile = StringVar()
                if self.args.output_edge_file:
                        self.outEdgeFile.set(self.args.output_edge_file)
                self.outEdgeEntry = Entry(master, width = WIDTH, textvariable = self.outEdgeFile)
                column += 1
                self.outEdgeEntry.grid(row=row,column=column, padx=3)
                self.outEdgeSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.outEdgeFile))
                column += 1
                self.outEdgeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText2 = "Edge file for output graph"
                self.outEdgeTip = CreateToolTip(self.outEdgeEntry, helpText2)
                #
                row += 1
                column = 0

                self.inTrailLabel = Label(master, text = "Input trail file")
                self.inTrailLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.inTrailFile = StringVar()
                if self.args.t:
                        self.inTrailFile.set(self.args.t)
                self.inTrailEntry = Entry(master, width = WIDTH, textvariable = self.inTrailFile)
                column += 1
                self.inTrailEntry.grid(row=row,column=column, padx=3)
                self.inTrailSelect = Button(master, text = "Select", command = lambda: self.setFile(var1=self.inTrailFile,var2=self.outTrailFile))
                column += 1
                self.inTrailSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText3 = "Links IDs of current graph to IDs of ROOT graph (two columns, tab-delimited).\nIf skipped, current graph is considered ROOT."
                self.inTrailTip = CreateToolTip(self.inTrailEntry, helpText3)
                #
                column += 2

                self.outTrailLabel = Label(master, text = "Output trail file")
                self.outTrailLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outTrailFile = StringVar()
                if self.args.output_trail_file:
                        self.outTrailFile.set(self.args.output_trail_file)
                column += 1     
                self.outTrailEntry = Entry(master, width = WIDTH, textvariable = self.outTrailFile)
                self.outTrailEntry.grid(row=row,column=column, padx=3)
                column += 1
                self.outTrailSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.outTrailFile))
                self.outTrailSelect.grid(row=row,column=column, sticky=W, padx=3)
                column += 1
                self.optionLabel2 = Label(master, text = "required")
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText4 = "Links new IDs to ROOT graph"
                self.outTrailTip = CreateToolTip(self.outTrailEntry, helpText4)
                #
                row += 1
                column = 0

                self.inNodeLabel = Label(master, text = "Input node type file")
                self.inNodeLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.inNodeType = StringVar()
                if self.args.n:
                        self.inNodeType.set(self.args.n)
                self.inNodeEntry = Entry(master, width = WIDTH, textvariable = self.inNodeType)
                column += 1
                self.inNodeEntry.grid(row=row,column=column, padx=3)
                self.inNodeSelect = Button(master, text = "Select", command = lambda: self.setFile(var1=self.inNodeType,var2=self.outNodeType))
                column += 1
                self.inNodeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "for k-partite")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText5 = "Stores node types (two columns, tab-delimited).\nRequired for multipartite (more than bipartite)."
                self.inNodeTip = CreateToolTip(self.inNodeEntry, helpText5)
                #
                column += 2
                
                self.outNodeLabel = Label(master, text = "Output node type file")
                self.outNodeLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outNodeType = StringVar()
                if self.args.N:
                        self.outNodeType.set(self.args.N)
                self.outNodeEntry = Entry(master, width = WIDTH, textvariable = self.outNodeType)
                column += 1
                self.outNodeEntry.grid(row=row,column=column, padx=3)
                self.outNodeSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.outNodeType))
                column += 1
                self.outNodeSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "for k-partite")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText6 = "Updates node types with new nodeIDs.\nRequired when input node type file is given."
                self.outNodeTip = CreateToolTip(self.outNodeEntry, helpText6)
                #
                row += 1
                column = 0
                
                self.componentLabel = Label(master, text = "Community file")
                self.componentLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.componentFile = StringVar()
                if self.args.c:
                        self.componentFile.set(self.args.c)
                self.componentEntry = Entry(master, width = WIDTH, textvariable = self.componentFile)
                column += 1
                self.componentEntry.grid(row=row,column=column, padx=3)
                self.componentSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.componentFile))
                column += 1
                self.componentSelect.grid(row=row,column=column, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 1
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText7 = "Specifies grouping of nodes into communities or super-nodes.\nIf not given, input graph is simply renumbered."
                self.componentTip = CreateToolTip(self.componentEntry, helpText7)
                #
                column += 2
                
                self.outDirLabel = Label(master, text = "Output directory")
                self.outDirLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outDir = StringVar()
                if self.args.d:
                        self.outDir.set(self.args.d)
                else:
                        self.outDir.set("OutputDir")
                self.outDirEntry = Entry(master, width = WIDTH, textvariable = self.outDir)
                column += 1
                self.outDirEntry.grid(row=row,column=column, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 2
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText8 = "Storage directory for output files.\nIf suppressed, check that in- and output filenames do not collide."
                self.outDirTip = CreateToolTip(self.outDirEntry, helpText8)
                #
                row += 1
                column = 0

                self.optionLabel = Label(master, text = "Clustering file format")
                self.optionLabel.grid(row=row,column=column, sticky=W, padx=3)
                option_list = ["Component","Fasta"]
                self.C = StringVar()
                self.C.set(option_list[0])
                if self.args.f:
                        self.C.set(option_list[1])
                self.optionEntry = Combobox(master, width = 10, textvariable = self.C)
                self.optionEntry['values'] = option_list
                column += 1
                self.optionEntry.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText9 = """Specifies format of community file \nComponent=two columns, tab-delimited\nFasta=one line per node, ">" for community ID"""
                self.optionTip = CreateToolTip(self.optionEntry, helpText9)
                #
                column += 2

                self.w = BooleanVar()
                self.w.set(self.args.w)
                self.chk = Checkbutton(master, text="Use weights", var = self.w)
                self.chk.grid (row=row,column=column,padx=3,sticky=W)
                # tip
                helpText10 = "Weighs super-nodes with log(size_of_community)"
                self.chkTip = CreateToolTip(self.chk, helpText10)
                #
                column += 2
                
                self.optionLabel = Label(master, text = "Keep community IDs")
                self.optionLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.K = BooleanVar()
                self.K.set(self.args.C)
                self.chk = Checkbutton(master, text="", var = self.K)
                column += 1
                self.chk.grid (row=row,column=column,padx=3,sticky=W)
                # tip
                helpText11 = "Gives to super-nodes the same ID as in the community file"
                self.keepTip = CreateToolTip(self.optionLabel, helpText11)
                #
                row += 1
                column = 1
                                
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
                
                self.run_button = Button(master, text="Run", command=self.run)
                self.run_button.grid(row=row,column=2)
                
                self.close_button = Button(master, text="Close", command=self.Quit)
                self.close_button.grid(row=row, column=4)

                helpText = factorgraph.processArgs().format_help()
                self.helpbutton = Button(master, text="Help", command = lambda: HelpWindow(text=helpText,name=self.name))
                self.helpbutton.grid(row=row,column=6,sticky=W,padx=3)
                
        def func(self,value):
                print("Set %s " % value)

        def setFile(self,var1=None,var2=None):
                self.openFile(var=var1)
                modfile = os.path.split(var1.get())[1]
                var2.set(modfile)
                self.master.update_idletasks()

        def setRequiredFiles(self,IN=None,OUT=None,TRAIL=None):
                self.openFile(var=IN)
                inFile = os.path.split(IN.get())[1]
                inRad = inFile.split(".")[0]
                trail = inRad+".trail"
                OUT.set(inFile)
                TRAIL.set(trail)
                self.master.update_idletasks()
                
        def openFile(self,var=None):
                var.set(askopenfilename())

        def Quit(self,event=None):
                self.master.destroy()
        
        def run(self,event=None):
                self.arguments['edgeFile'] = self.inEdgeFile.get()
                self.arguments['outEdgeFile'] = self.outEdgeFile.get()
                self.arguments['outTrailFile'] = self.outTrailFile.get()
                self.arguments['direct'] = self.outDir.get()
                if self.C.get() == 'Component':
                        self.arguments['community'] = self.componentFile.get()
                else:
                        self.arguments['comm_fasta'] = self.componentFile.get()
                self.arguments['comm_id'] = self.K.get()
                self.arguments['in_trail'] = self.inTrailFile.get()
                self.arguments['inType'] = self.inNodeType.get()
                self.arguments['outType'] = self.outNodeType.get()
                self.arguments['weight'] = self.w.get()
                self.arguments['log'] = self.l.get()
                if self.arguments['log'] == 'stderr':
                        self.arguments['log'] = sys.stderr
                self.arguments['sep'] = self.args.s
                self.arguments = renorm(self.arguments)
                self.arguments['header'] = genHeader(self.name,self.arguments)
                self.master.destroy()


def genHeader(prog,args):
        DIR,EDGE = os.path.split(args['edgeFile'])
        header = "%s" % prog
        if args['direct']:
                header += " -d %s" % args['direct']
        try:
                if args['community']:
                        COMM = os.path.abspath(args['community'])
                        header += " -c %s" % COMM
        except KeyError:
                pass
        try:
                if args['comm_fasta']:
                        FASTA = os.path.abspath(args['comm_fasta'])
                        header += " -f %s" % FASTA
        except KeyError:
                pass
        if args['comm_id']:
                header += " -C"
        if args['in_trail']:
                header += " -t %s" % args['in_trail']
        if args['inType']:
                header += " -n %s" % args['inType']
        if args['outType']:
                header += " -N %s" % args['outType']
        if args['weight']:
                header += " -w"
        if args['outEdgeFile']:
                header += " -o %s" % args['outEdgeFile']
        if args['outTrailFile']:
                header += " -T %s" % args['outTrailFile']
        header += " -i %s" % args['edgeFile']
        return header
                
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
        newArgs = MyGUI(root,title=prog,args=args)
        root.update_idletasks()
        RHeight = root.winfo_reqheight()
        RWidth = root.winfo_reqwidth()
        root.geometry(("%dx%d+300+300") % (RWidth,RHeight))
        root.bind("<Return>", newArgs.run)
        root.bind("<Escape>", newArgs.Quit)
        center(root)
        root.wait_window(newArgs.master)
        try:
                #print(args.arguments)
                factorgraph.Main(**newArgs.arguments)
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
