#! /usr/bin/python

# -*-coding:utf-8 -*-

"""
        Written by Romain LANNES, 2018.
        
        This file is part of MultiTwin.
        
        MultiTwin is shared under Creative commons licence: 
        
        Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
        
        See https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import argparse
import subprocess
import os

import time
import re
from multiprocessing import Pool


parser = argparse.ArgumentParser(description='will make a blast all against all')
parser.add_argument('-i', help='input', required=True)

parser.add_argument('-db', help='database for the blast')
parser.add_argument('-evalue', help='E-value', default=10)
parser.add_argument('-out', help='outfile', required=True)
parser.add_argument('-th', help='n_thread', required=True, type=int)
parser.add_argument('-fasta_spl', help='path to fastasplit', default='fastasplit', type=str)
args = parser.parse_args()



def blast(args_tuple):
	"""Just launch the blast"""

	query, database, evalue, output_file = args_tuple
	cmd = 'blastp -query %s -evalue %s -db %s -out %s -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend sstart send qlen slen"' % (query, evalue, database, output_file)
	try:
		print(cmd)
		child = subprocess.Popen(cmd, shell=True)
		child.wait()
	except:
		raise
	else:
		return 0


# we create a working dir
list_of_file = os.listdir('.')
cpt = 0
working_dir = "Allagainstallwd_%d" % cpt

while working_dir in list_of_file:
	cpt += 1
	working_dir = working_dir = "Allagainstallwd_%d" % cpt

# database directory
db_dir = working_dir + '/' + 'db_'
# fasta split directory
split_dir = working_dir + '/' + 'split_'
# result directory
res_dir = working_dir + '/' + 'res'
os.makedirs(db_dir)
os.makedirs(split_dir)
os.makedirs(res_dir)

# if database does not exist we create it
if not args.db:
	db = db_dir + '/db_b'
	# make the db
	child = subprocess.Popen('makeblastdb -dbtype prot -hash_index -in %s -out %s' % (args.i, db), stdout=subprocess.DEVNULL, shell=True)
	child.wait()
else:
	db = args.db

# for the split we need to know how many sequence we have
num_seq = int(subprocess.check_output("grep -c '>' %s" % args.i, shell=True).decode('utf-8'))

if args.th < num_seq:
	nb_split = args.th
else:
	nb_split = num_seq

# split the fasta
child = subprocess.Popen('%s -f %s -o %s -c %d' % (args.fasta_spl, args.i, split_dir, nb_split), shell=True)
child.wait()

# making a list with the absolute path to each splitted fasta
all_split = os.listdir(split_dir)
abs_path = os.path.abspath(split_dir)
all_split = [abs_path + '/' + element for element in all_split]


# for the pool.map we need a tuple by process
# each tuple contain the blast arguments
liste_args = list()
cpt = 0
evalue = args.evalue
for file in all_split:
	cpt += 1
	tuple_args = (file, db, evalue, res_dir + '/' + os.path.basename(file) + str(cpt))
	liste_args.append(tuple_args)
	
# define the pool
pool = Pool(processes=args.th)

# launch the process
out_code = pool.map(blast, liste_args)

# cat result
child = subprocess.Popen("cat %s > %s" % (res_dir+'/*', args.out), shell=True)
child.wait()

# remove working dir
subprocess.Popen("rm -rf %s" % working_dir, shell=True)
