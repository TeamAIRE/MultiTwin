#!/usr/bin/python3

"""
        Written by Eduardo COREL, 2018.
        
        This file is part of multitwin.
        
        multitwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import argparse
import sys
import os
import threading
from ttkthemes import themed_tk as tk 
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton, Scrollbar, Combobox, OptionMenu, Style
from tkinter.constants import HORIZONTAL, VERTICAL, N,S,E,W, END, LEFT, RIGHT, X, Y, YES, NW, BOTTOM
from tkinter import Tk, StringVar, BooleanVar, BOTH, W, E, Canvas
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from utils import CreateToolTip,HelpWindow,center
import bitwin

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
        
                self.blastLabel = Label(master, text = "Blast/Diamond output file")
                self.blastLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.blastFile = StringVar()
                if self.args.b:
                        self.blastFile.set(self.args.b)
                self.blastEntry = Entry(master, width = WIDTH, textvariable = self.blastFile)
                self.blastEntry.grid(row=row,column=1, padx=3)
                self.blastSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.blastFile))
                self.blastSelect.grid(row=row,column=2, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.blastEntry,"Sequence similarity file produced by BLAST or DIAMOND.\nUses specific format (see README).")
                row += 1

                self.networkLabel = Label(master, text = "Genome to gene file")
                self.networkLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.networkFile = StringVar()
                if self.args.g:
                        self.networkFile.set(self.args.g)
                self.networkEntry = Entry(master, width = WIDTH, textvariable = self.networkFile)
                self.networkEntry.grid(row=row,column=1, padx=3)
                self.networkSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.networkFile))
                self.networkSelect.grid(row=row,column=2, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "required")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.networkEntry,"Input bipartite graph edge file (Tab-separated).\nCheck for the ordering of the items on each line:\nGenome first, then sequence ID.")
                row += 1
                
                self.annotLabel = Label(master, text = "Annotation file")
                self.annotLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.a = StringVar()
                if self.args.a:
                        self.a.set(self.args.a)
                self.annotEntry = Entry(master, width = WIDTH, textvariable = self.a)
                self.annotEntry.grid(row=row,column=1, padx=3)
                self.annotSelect = Button(master, text = "Select", command = lambda: self.openAnnotFile(var=self.a))
                self.annotSelect.grid(row=row,column=2, sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "recommended")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.annotEntry,"Common annotation file for genomes and genes.\nTab-delimited, compulsory header with attribute names.\nSpecify empty annotations with '-'.")
                row += 1

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
                                
                self.optionLabel = Label(master, text = "Identity threshold(s)")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.n = StringVar()
                if self.args.n:
                        self.n.set(self.args.n)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.n)
                self.optionEntry.grid(row=row,column=1, padx=3)
                self.optionLabel2 = Label(master, text = "comma-separated")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"List of thresholds considered.\nOne subdirectory will be created for each value.")
                row += 1
                
                self.optionLabel = Label(master, text = "Mutual cover")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.c = StringVar()
                if self.args.c:
                        self.c.set(self.args.c)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.c)
                self.optionEntry.grid(row=row,column=1, sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"Set new value for minimum mutual cover for sequence similarity.")
                row += 1
                
                self.optionLabel = Label(master, text = "Clustering method")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                option_list = ["cc","families"]
                self.C = StringVar()
                self.C.set(option_list[0])
                self.optionEntry = Combobox(master, width = 10, textvariable = self.C)
                self.optionEntry['values'] = option_list
                self.optionEntry.grid(row=row,column=1,sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"""Select method for the definition of gene families.\ncc = connected components of sequence similarity network.\nfamilies = communities produced by the "Louvain" multilevel algorithm.""")
                row += 1
                
                self.optionLabel = Label(master, text = "Input network")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.I = StringVar()
                if self.args.I:
                        self.I.set(self.args.I)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.I)
                self.optionEntry.grid(row=row,column=1, padx=3)
                self.optionSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.I))
                self.optionSelect.grid(row=row,column=2, sticky=W, padx=3)                                   
                self.optionLabel2 = Label(master, text = "optional")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"Supply directly sequence similarity network.\nSkips use of cleanblast on the blast file output.")
                row += 1
                
                self.optionLabel = Label(master, text = "Fasta file")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.f = StringVar()
                if self.args.f:
                        self.f.set(self.args.f)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.f)
                self.optionEntry.grid(row=row,column=1, padx=3)
                self.optionSelect = Button(master, text = "Select", command = lambda: self.openFile(var=self.f))
                self.optionSelect.grid(row=row,column=2, sticky=W, padx=3)                                
                self.optionLabel2 = Label(master, text = "optional")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"Supply fasta file for the protein sequences.\nAdds sequence similarity detection step.\nWARNING: this could take a long time.")
                row += 1
                
                self.optionLabel = Label(master, text = "Similarity search software")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                option_list = ["Blast","Diamond"]
                self.A = StringVar()
                self.A.set(option_list[0])
                self.optionEntry = Combobox(master, width =10,  textvariable = self.A)
                self.optionEntry['values'] = option_list
                self.optionEntry.grid(row=row,column=1,sticky=W, padx=3)
                self.optionLabel2 = Label(master, text = "optional (requires fasta file)")
                self.optionLabel2.grid(row=row,column=3,sticky=W, padx=3)
                CreateToolTip(self.optionEntry,"Selects sequence similarity detection software.\nSilently ignored if no fasta file is given.")
                row += 1
                
                self.optionLabel = Label(master, text = "Unique node identifier")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.i = StringVar()
                if self.args.i:
                        self.i.set(self.args.i)
                self.optionEntry = Entry(master, width = WIDTH, textvariable = self.i)
                self.optionEntry.grid(row=row,column=1, padx=3)
                CreateToolTip(self.optionEntry,"""Name of first column in %s file.\nCheck that the items in this column match the node IDs in the ROOT graph.""" % self.args.a)
                row += 1

                self.optionLabel = Label(master, text = "Graphic interface for Description")
                self.optionLabel.grid(row=row,column=0, sticky=W, padx=3)
                self.K = BooleanVar()
                self.K.set(self.args.K)
                self.chk = Checkbutton(master, text="Display?", var = self.K)
                self.chk.grid (row=row,column=1,padx=3,sticky=W)
                CreateToolTip(self.chk,"Displays graphic customization interface for the last description.py step.\nIf not selected, displays all attributes for all key types and all trail levels.")
                row += 1
                column = 0
                self.outDirLabel = Label(master, text = "Output directory")
                self.outDirLabel.grid(row=row,column=column, sticky=W, padx=3)
                self.outDir = StringVar()
                if self.args.D:
                        self.outDir.set(self.args.D)
                else:
                        self.outDir.set('')
                self.outDirEntry = Entry(master, width = WIDTH, textvariable = self.outDir)
                column += 1
                self.outDirEntry.grid(row=row,column=column, padx=3)
                self.optionLabel2 = Label(master, text = "optional")
                column += 2
                self.optionLabel2.grid(row=row,column=column,sticky=W, padx=3)
                # tip
                helpText8 = "Storage directory for output files."
                self.outDirTip = CreateToolTip(self.outDirEntry, helpText8)
                #
                row += 1
                
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

                helpText = bitwin.processArgs().format_help()
                self.helpbutton = Button(master, text="Help", command = lambda: HelpWindow(text=helpText,name=self.name))
                self.helpbutton.grid(row=row,column=2,sticky=W,padx=3)
                
        def func(self,value):
                print("Set %s " % value)

        def openFile(self,var=None):
                var.set(askopenfilename())
                self.master.update_idletasks()

        def openAnnotFile(self,var=None):
                var.set(askopenfilename())
                row = 3
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
                CreateToolTip(self.optionEntry,"""List of available attributes in file %s.\nIf you wish to remove some, click on line and edit.\nTo change annotation file, click on 'Select' """ % ann)
                self.master.update_idletasks()
                RHeight = self.master.winfo_reqheight()
                RWidth = self.master.winfo_reqwidth()
                self.master.geometry(("%dx%d+300+300") % (RWidth,RHeight))
                center(self.master)
                          
        def Quit(self,event=None):
                self.master.destroy()
        
        def run(self,event=None):
                self.arguments['blastFile'] = self.blastFile.get()
                self.arguments['genome2sequence'] = self.networkFile.get()
                self.arguments['annot'] = self.a.get()
                self.arguments['thr'] = self.n.get()
                self.arguments['cov'] = self.c.get()
                self.arguments['clust'] = self.C.get()
                self.arguments['in_network'] = self.I.get()
                self.arguments['fasta'] = self.f.get()
                self.arguments['aln'] = self.A.get()
                self.arguments['key'] = self.i.get()
                self.arguments['log'] = self.l.get()
                if self.arguments['log'] == 'stderr':
                        self.arguments['log'] = sys.stderr
                if self.arguments['aln'] == 'Blast':
                        self.arguments['aln'] = 'b'
                elif self.arguments['aln'] == 'Diamond':
                        self.arguments['aln'] = 'd'
                self.arguments['sep'] = self.args.s
                self.arguments['keyList'] = self.args.k
                if self.k.get():
                        #print("KeyList defined: %s" % self.k.get()) 
                        self.arguments['keyList'] = self.k.get()
                if self.outDir.get():
                        self.arguments['directory'] = self.outDir.get()
                else:
                        self.arguments['directory'] = self.args.D
                if self.K.get():
                        self.arguments['config'] = self.K
                self.arguments = renorm(self.arguments)
                print(self.arguments)
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
        root.minsize(width=500,height=300)
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
                bitwin.Main(**args.arguments)
        except:
                root.destroy

def processArgs():
        """ Parser function of main """
        parser = argparse.ArgumentParser(description='Configures and launches the bitwin.py software')
        parser.add_argument("prog", help="program",type=str)
        return(parser)

if __name__ == '__main__':
        prog = sys.argv[0].split("/")[-1]
        parser = processArgs()
        args = parser.parse_args()
        CMD = " ".join(sys.argv)
        print(vars(args))
        main()
