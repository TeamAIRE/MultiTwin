_MultiTwin_ package for the analysis of multipartite graphs.

Authors: Eduardo Corel & Jananan S. Pathmanathan -- 2014-2018.

# Prerequisites

To run the _MultiTwin_ suite, you need the following software. If already installed, you can skip the corresponding paragraph.

|Program|Comment|
|--------|:-----------|
|`Python 2`|version `>= 2.4` , recommended `2.7` ; not Python 3|
|`g++`|version `>= 4.8` |
|`igraph`| source `C`  code + `python`  bindings (version `>= 0.7.1` )| 
|`blast`  | complete NCBI suite (version `>= 2.6` )|
|`exonerate` | EBI software package (version `>= 2.2` )|
|`diamond` | Huson lab software package (version >= `0.9.6`)|


1. Python: Minimum `Python 2.4`, recommended version: `2.7.X`

   _Attention_: The code will likely not work under `Python 3`. 
   If your default version is `Python 3`, replace all `#! /usr/bin/python` headers with the appropriate path.

2. C++: compiler `g++`  version `>= 4.8` 

   To check what version is currently installed, type:

       $ g++ --version

   If an update is required, type the following commands:

       $ sudo add-apt-repository ppa:ubuntu-toolchain-r/test
       $ sudo apt-get update
       $ sudo apt-get install g++-4.8
       $ sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50

3. `igraph` library: 

  * Install the `igraph` C code: download the latest version of the `igraph` library (here `0.7.1`) to your `DOWNLOAD_DIR`

        $ mkdir DOWNLOAD_DIR
        $ cd DOWNLOAD_DIR/.
        $ wget http://igraph.org/nightly/get/c/igraph-0.7.1.tar.gz 
        $ tar -xvf igraph-0.7.1.tar.gz 
        $ rm igraph-0.7.1.tar.gz 
        $ cd igraph-0.7.1
        $ less INSTALL

      and follow the install instructions -- usually

        $ ./configure 
        $ make
        $ sudo make install

      _NB_: You might need to run additionally

        $ sudo ldconfig

       If you get an error message for missing libraries `libxml2-dev` or `zlib1g-dev`, type accordingly

        $ sudo apt-get install libxml2-dev 
        $ sudo apt-get install zlib1g-dev

     and redo the install instructions above.

     _WARNING_: installing the `igraph` library can take a rather long time.

  * Install the `python-igraph` bindings. The easiest way is to use the `easy_install` or `pip` procedure

       If you have neither python installers:

     - Install `easy_install` by typing

           $ sudo apt-get install python-setuptools python-dev build-essential 

     - Install the `pip` python installer, type the following commands

           $ sudo apt-get install python-pip python-dev build-essential 
           $ sudo pip install --upgrade pip 
           $ sudo pip install --upgrade virtualenv 
	
     And then run 
	
        $ sudo easy_install python-igraph
    or
 
        $ sudo pip install python-igraph

4. `BLAST`

* Install the `blastp` software from the NCBI repository:

      $ mkdir BLAST_DIRECTORY
      $ cd BLAST_DIRECTORY
      $ wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.6.0+-x64-linux.tar.gz
      $ tar -xvf ncbi-blast-2.6.0+-x64-linux.tar.gz
      $ rm ncbi-blast-2.6.0+-x64-linux.tar.gz

     If you download a later version, change the version number accordingly.

* Install the `exonerate` package

      $ mkdir EXO_DIRECTORY
      $ cd EXO_DIRECTORY
      $ wget http://ftp.ebi.ac.uk/pub/software/vertebrategenomic/exonerate/exonerate-2.2.0-x86_64.tar.gz
      $ tar -xvf exonerate-2.2.0-x86_64.tar.gz 
      $ rm exonerate-2.2.0-x86_64.tar.gz 

     or install from source (if the architecture differs from `x86_64`):
 
      $ cd EXO_DIRECTORY
      $ wget http://ftp.ebi.ac.uk/pub/software/vertebrategenomics/exonerate/exonerate-2.2.0.tar.gz
      $ tar -xvf exonerate-2.2.0.tar.gz
      $ rm exonerate-2.2.0.tar.gz
      $ cd exonerate-2.2.0/
   and follow the INSTALL instructions.

* Update the PATH variable:

     Add `BLAST_DIRECTORY/ncbi-blast-2.6.0+/bin` and `EXO_DIRECTORY/exonerate-2.2.0-x86_64/bin` to the `PATH` variable in `~/.profile`

5. `DIAMOND` 

* Install the `diamond` software from https://github.com/bbuchfink/diamond into a `DIAMOND_DIRECTORY`

      $ cd DIAMOND_DIRECTORY
      $ tar xzf diamond.tar.gz 
      $ cd diamond
      $ ./configure
      $ make
      $ make install
    Alternatively, for having a local copy of `Boost`  installed as well:

      $ tar xzf diamond.tar.gz
      $ cd diamond
      $ ./install-boost
      $ ./configure --with-boost=boost
      $ make
      $ make install
    This will install the `DIAMOND` binary to `/usr/local/bin` and requires write permission to that directory. You may also pass `--prefix=DIR` to the configure script to choose a different installation directory.

* Update the PATH variable:

     Add `DIAMOND_DIRECTORY/` to the `PATH` variable in `~/.profile`


# INSTALLATION of the _MultiTwin_ package

* Download the tar file in a directory `INSTALL_DIR`

      $ cd INSTALL_DIR
      $ tar -xvf MultiTwin_2018-1.1.tar
      $ rm MultiTwin_2018-1.1.tar
      $ cd MultiTwin1.1/
      $ chmod 751 config.sh
      $ ./config.sh

    The executable scripts `CleanBlast` and `FamilyDetector` should have been generated in `BlastProg/`. 
If this is not the case, check the version of the `g++` compiler (see Prerequisites above).

* Refresh the `PATH` and `PYTHONPATH` variables in the `.profile` configuration file, by typing
   
      $ source ~/.profile

* Test if the installation was successful:

    Run the following:

      $ cd data
      $ BiTwin.py -a seq.annot -n 30 seq.blastp genome2seq.txt

### The `data`  DIRECTORY initially contains:

| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`seq.blastp` | The result of the `BLAST` or `diamond`  run.| First compulsory argument for the `BiTwin.py`  program.|
|`genome2seq.txt` | Contains the correspondence between sequences and genomes: `X TAB Y`  where X is the identifier of a genome and Y the identifier of a sequence. | Second compulsory argument for `BiTwin.py`.| 
|`seq.annot` | Annotation file for both sequences and genomes. Fields having no match for a given row are shown with a dash ("-"). | This file is optional (option `-a` ).|

### The previous command produces the following hierarchy of directories and files:
1. in `data` 

  | File | DESCRIPTION | COMMENT |
  |--------|:-----------|:------|
  |`seq.blastp.cleanNetwork` |  Sequence-similarity graph obtained by keeping the best reciprocal hit (>=30% ID) with reciprocal minimum coverage of 80% | Sequence IDs are renumbered.|
  |`seq.blastp.cleanNetwork.genes` |  List of new sequence IDs | Internal use only.|
  | `seq.blastp.cleanNetwork.dico` |   Correspondence between initial IDs and sequence ids. | Internal use only.|

2. in `data/graphs30/` 

  | File | DESCRIPTION | COMMENT |
  |--------|:-----------|:------|
  |`CC.nodes` | Community file for gene families| at 30% identity| 
	  222147474	17
	  153932043	12
	  117618069	15
	  187476667	23
	  59712147	6
	  (...)

  ||||
  |--------|:-----------|:------|
  | `CC.edges` | Fasta-formatted list of edges for each gene family|includes singletons _i.e._ families without edges.|
     >CC1
   	(...)
	>CC5
	7	13
	>CC6
	8	11
	(...)

  ||||
  |--------|:-----------|:------|
  |`CC.info` | Graph statistics for the gene families.||

    #CCid	  nodes	  edges
	1	1	0
	2	1	0
	3	1	0
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph.edges` | The bipartite graph obtained by factoring the `GenomeToSeq.txt`  ROOT graph by the gene family file| The weight in the third column is _log_(nb of original edges).|
        
    38	1	1.00
	28	22	1.00
	38	20	1.00
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph.trail` |The corresponding trail file.|Recalls `ROOT`  directory and calling command.|
    # FactorGraph.py -d 'graphs30' -k 'UniqID' -c 'graphs30/CC.nodes' -s '\t' genome2seq.txt graph.edges graph.trail 
    # Root directory: data_directory`
    93006436	6 
    213155360	39
    (...)

  ||||
  |--------|:-----------|:------|
  |`graph0.edges` |The bipartite graph obtained by removing all degree one gene families.||
    28	22	1.00
    29	23	1.00 
    40	6	1.69 
    (...)

  ||||
  |--------|:-----------|:------|
  |`graph0.twins` |The community file describing the twin mapping. ||
    15	1
	14	3
	17	4
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph0.twin_comp` |The community file describing the twin+support overlapping clustering.|| 
    15	1
	14	3
	17	4
	23	0
	(...)

3. in `data/graphs30/TwinQuotient/` 

  ||||
  |--------|:-----------|:------|
  |`graph1.edges` |The bipartite graph obtained by factoring `graph0.edges`  by the `graph0.twins`  file.||
    17	5	1.00
	16	0	1.00
	10	6	1.00
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.trail` |The corresponding trail file.||
    # FactorGraph.py -d 'TwinQuotient' -k 'UniqID' -c 'graph0.twins' -s '\t' -t 'graph.trail' graph0.edges graph1.edges graph1.trail
	# Root directory: data_directory
	59251	10
	222147474	4
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.art` |List of articulation points of `graph1` ||
    5
	16
	0
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.twins` | Twin file of `graph1`  ||
    1	0
	0	3
	3	6
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.twin_comp` |   Community file describing the twin support overlapping clustering of `graph1`.||
    1	0
	0	3
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.config` |  XML Configuration file for the `Description.py`   script (embedded in `BiTwin.py`)||


  ||||
  |--------|:-----------|:------|
  |`graph1.desc` | Description file: every `Module` is a twin of gene families plus its support|The fields at the beginning of each row match the column names in the annotation file `seq.annot`).
	Module 3
	COGID	{'COG1629': 5}
	DESCRIPTION	{'Outer membrane receptor proteins, mostly Fe transport': 5}
	Genome Project ID	{'PRJNA59083': 1, 'PRJNA59899': 1, 'PRJNA61563': 1, 'PRJNA52575': 1}
	CC	{'6402': 5}
	COGCAT	{'P': 5}
	Species	{'Acinetobacter baumannii AB0057': 1, 'Bordetella avium 197N': 1, 'Actinobacillus pleuropneumoniae serovar 11 str. 56153': 1, 'Achromobacter xylosoxidans A8': 1}
	PATH	{'1': 4, '2': 1}
	Shorthand ID	{'Bav': 1, 'Aba': 1, 'Axy': 1, 'Apl': 1}
	SPECIES	{'61563': 1, '59899': 1, '52575': 1, '59083': 2}
	Pathogen	{'1': 3, '2': 1}
	(...)

  ||||
  |--------|:-----------|:------|
  |`graph1.xml_desc` | XML version of the description file (easier to parse than `graph1.desc`  | The same `Module 3`  is described as follows| 

	<mod "name"=Module "id"=3>
	<content>
        <attr "name"=COGID>
                {'COG1629': 5}
        </attr>
        <attr "name"=DESCRIPTION>
                {'Outer membrane receptor proteins, mostly Fe transport': 5}
        </attr>
        <attr "name"=Genome Project ID>
                {'PRJNA59083': 1, 'PRJNA59899': 1, 'PRJNA61563': 1, 'PRJNA52575': 1}
        </attr>
        <attr "name"=CC>
                {'6402': 5}
        </attr>
        <attr "name"=COGCAT>
                {'P': 5}
        </attr>
        <attr "name"=Species>
                {'Acinetobacter baumannii AB0057': 1, 'Bordetella avium 197N': 1, 'Actinobacillus pleuropneumoniae serovar 11 str. 56153': 1, 'Achromobacter xylosoxidans A8': 1}
        </attr>
        <attr "name"=PATH>
                {'1': 4, '2': 1}
        </attr>
        <attr "name"=Shorthand ID>
                {'Bav': 1, 'Aba': 1, 'Axy': 1, 'Apl': 1}
        </attr>
        <attr "name"=SPECIES>
                {'61563': 1, '59899': 1, '52575': 1, '59083': 2}
        </attr>
        <attr "name"=Pathogen>
                {'1': 3, '2': 1}
        </attr>
	</content>

For more information on each type of file, see the `README`  file with the complete attached data `MultiTwin1.1_Data.tar.gz` 


