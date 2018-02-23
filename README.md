*MultiTwin* package for the analysis of multipartite graphs.

Authors: Eduardo Corel & Jananan S. Pathmanathan – 2014-2018.

CONTENTS:
=========

Download the tarball `MultiTwin_2018-1.1.tar` into an `INSTALL_DIR`

    $ cd INSTALL_DIR
    $ tar -cvf MultiTwin_2018-1.1.tar
    $ cd MultiTwin_2018
    $ ls

-   `BlastProg/`

-   `config.sh`

-   `data/`

-   `INSTALL.txt`

-   `python-scripts/`

-   `README.txt`

        $ ls python-scripts/

-   `BiTwin.py`

-   `BlastAll.py`

-   `Cluster.py`

-   `Description.py`

-   `DetectTwins.py`

-   `FactorGraph.py`

-   `InducedSubgraph.py`

-   `ShaveGraph.py`

-   `TrailHistory.py`

-   `TransferAnnotations.py`

-   `Utils.py`

> Except maybe for the `Utils.py` file, all files should be executable
> (if not, change the status with `$ chmod +x *.py`)

    $ ls BlastProg/

-   `cleanBlast/`
-   `CleanBlast`
-   `familyDetector/`
-   `FamilyDetector`
-   `makefile`

> `CleanBlast` and `FamilyDetector` should be executable (same remark as
> above)

    $ ls data/

-   `genome2seq.txt`
-   `seq.annot`
-   `seq.blastp`

> This is a toy example to test the installation.

FORMATS:
========

A graph is specified by one compulsory and several optional files

-   edge file (*compulsory*)
-   node type file (*optional*: for multipartite graphs)
-   trail file (*optional*)

The edge file describes the graph by its edges in a standardized way:

`Node1 TAB Node2`

> This format is most convenient for storing large graph files, although
> its main drawback is the unability to store singletons.  
> Nodes can be any string (with or without whitespace, although they
> should definitely avoid TAB characters)

-   UNIPARTITE GRAPHS: no further specification needed.

-   BIPARTITE GRAPHS: Bipartite graphs are graphs containing two sets of
    nodes (conventionally called “white” nodes and “black” nodes), such
    that every edge connects only nodes of different sets.

    -   For bipartite graphs, our code implicitly considers all nodes
        appearing in the same column to be of the same colour:  
        `Node1 TAB Node2`  
        `Node3 TAB Node4`  
        `Node1 TAB Node4`  
        (…)  
        `Node1` and `Node3` are then, say, white, and `Node2` and
        `Node4`, black.

       > NOTE: Any inconsistency in the input file will NOT be caught! If
        a node appears in both columns, then the graph is not bipartite,
        but this should be specified (usually by a `-k 1` option)

-   MULTIPARTITE GRAPHS: k-partite graphs are graphs whose set of nodes
    *V*, is partitioned in k subsets *V\_1,…,V\_k* such that an edge
    only connects nodes from different subsets.

    -   They must be described with an additional node type file:  
        `Node1 TAB nodeType1`  
        `Node2 TAB nodeType1`  
        `Node3 TAB nodeType2`  
        `Node4 TAB nodeType2`  
        `Node5 TAB nodeType3`  
        (…)

EXECUTABLES:
============

1.  `DetectTwins.py [options] edgeFile`  
    Twins are nodes in a graph that have exactly the same set of
    neighbours.

-   Input: a graph
-   Output (by default): a single file containing the twins in the
    graph.  
    `Node1 TAB TwinClass1`  
    `Node2 TAB TwinClass1`  
    `Node3 TAB TwinClass2`  
    `Node4 TAB TwinClass2`  
    `Node5 TAB TwinClass2`  
    (…)

> Nodes that form a singleton (ie whose set of neighbours is unique) are
> not given a twin identifier: the output file can therefore have less
> lines than the number of nodes.

* Options:

| Option                          |                                                    MESSAGE                                                    |                                                                                                                  COMMENT                                                                                                                 |
|---------------------------------|:-------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`                    |                                        show this help message and exit                                        |                                                                                                                                                                                                                                          |
| `-s S, --separator=S`           |                                                Field separator                                                |                                                                                             Use another separator than TAB (not recommended)                                                                                             |
| `-o O, --outfile=O`             |                                              Give name to outfile                                             |                                                                 Code gives output the default name: `edgeFile.twins` . Use this option to override with your own choice.                                                                 |
| `-u U, --unilateral=U`          |        Only detect twins from one side (1/2/3…) depending on the `typeFile` supplied (comma-separated).       | All twins are computed by default: use this option to restrict to nodes of chosen types (`-u 1` for twins for type1 nodes only). Twins are nodes having exactly the same set of neighbours: they are identified by an arbitrary integer. |
| `-t T, --twin-support=T`        |         Output twinSupport file (format: ID nbTwinNodes nbSupportNodes SupportNodesIDs (tab-separated)        |                                                                                       Twin support = common set of neighbours. Formatting option 1                                                                                       |
| `-T T, --Twin-Support=T`        |  Output twinSupport file (another format: ID TwinNodesIDs (comma-separated) SupportNodesIDs (comma-separated) |                                                                                                    Alternative format for twin support                                                                                                   |
| `-m THR, --minimal-support=THR` |                               Minimal threshold for the size of the twin support                              |                                                                           Do not consider as twins nodes whose number of neighbours (degree) is lower than THR.                                                                          |
| `-M M, --minimal-size=M`        |                                   Minimal threshold for the size of the twin                                  |                                                                                              Exclude twin sets composed of less than M nodes                                                                                             |
| `-n N, --inNodeType=N`          |    Input node type file : Original\_nodeName -\> type of node (in k-partite) – Syntax : 1/2 or nodeTypeFile   |                                                           PARTITENESS OPTION: Default is 2. If 1, consider the graph as unipartite; otherwise, you must specify a nodeType file                                                          |
| `-c C, --comp=C`                | Output comp file for twin and support (ie both twin nodes and nodes in support receive the same component ID) |                       Output a file where twin nodes and their support are identified by the same integer.ATTENTION: One node will usually have SEVERAL identifiers (all the twin supports that contain this node).                      |
| `-d, --debug`                   |                                                     Debug                                                     |                                                                                                               Not relevant.                                                                                                              |

2.  `FactorGraph.py [options] inNetworkFile outNetworkFile outTrailingFile`

> This script is the central piece of the *MultiTwin* software: it is
> meant to construct a factor graph (or quotient graph) from an input
> graph, and allow to track the modifications that have been applied to
> its nodes.  
> The factor graph is constructed from a community file: its nodes
> correspond to the communities, and an edge is drawn between two
> communities whenever members of these communities were connected.  
> If no community file is supplied however, it simply recasts the input
> graph by renaming its nodes, and outputs the dictionary of the
> renaming as an `outTrailingFile` .  
> The essential usefulness of this script is provided through the `-c`
> (and `-t` ) options.

A community file and a trail file follow the same syntax:

`Node1 TAB identifier1`  
`Node2 TAB identifier1`  
`Node3 TAB identifier2`  
`Node4 TAB identifier2`  
(…)

A community file simply specifies the community id of the nodes in the
graph.

> The trail file is central in the whole software: it links the original
> node ID to the current node ID it has been mapped to, since the root
> graph has started to be transformed.

| ROOT GRAPH                      | (community file 1) | GRAPH1                          | (community file 2) | GRAPH2                          | …   | GRAPH\_k                          |
|:--------------------------------|:-------------------|:--------------------------------|:-------------------|:--------------------------------|:----|:----------------------------------|
| edgeFile: UniqID                |                    | edgeFile: newID1                |                    | edgeFile: newID2                |     | edgeFile: newID\_k                |
| (nodeType: UniqID TAB nodeType) |                    | (nodeType: newID1 TAB nodeType) |                    | (nodeType: newID2 TAB nodeType) |     | (nodeType: newID\_k TAB nodeType) |
|                                 |                    | trailFile: UniqID TAB newID1    |                    | trailFile: UniqID TAB newID2    |     | trailFile: UniqID TAB newID\_k    |

> Note: if one supplies no trailFile to `FactorGraph.py` , then it is
> implicitly assumed that the edgeFile provided is the `ROOT` graph (and
> its node identifiers the reference ones).

-   Options:

| Option                  | MESSAGE                                                                                         | COMMENT                                                                                                                                                                                                                                                                |
|:------------------------|:------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`            | show this help message and exit                                                                 |                                                                                                                                                                                                                                                                        |
| `-d D, --directory=D`   | Subdirectory where results will be saved                                                        | Create subdirectory and store output files                                                                                                                                                                                                                             |
| `-c C, --community=C`   | Input community cluster file for the graph factoring                                            | Pass the community file where the first column are current graph node identifiers and the second are the community identifiers.                                                                                                                                        |
| `-C, --community-ID`    | Keep the identifiers from the community file – requires `-c` option, otherwise silently ignored | By default, all communities are renumbered from 0. Use this option to override and keep original community identifiers. *Attention*: the renumbering for singleton nodes (ie not belonging to any non trivial community) will start after the largest available label. |
| `-t T, --trailing=T`    | Input trailing file : Original\_nodeName -\> current\_nodeName                                  | *VERY IMPORTANT*: the trail file attaches to the `ROOT` node Ids the value of its current super-node: passing the trailFile allow to keep a consistent renumbering of the nodes                                                                                        |
| `-n N, --inNodeType=N`  | Input node type file : Original\_nodeName -\> type of node (in k-partite)                       | MULTIPARTITE GRAPH: supply the nodeType file with the node types.                                                                                                                                                                                                      |
| `-N N, --outNodeType=N` | Output node type file : New\_nodeName -\> type of node (in k-partite)                           | MULTIPARTITE GRAPH: update the nodeType file with the new node identifiers.                                                                                                                                                                                            |
| `-w, --weight`          | Use weights (BOOLEAN)                                                                           | When creating the super-nodes, endow them with a weight (currently the number of nodes).                                                                                                                                                                               |
| `-s S, --separator=S`   | Field separator                                                                                 | Specify new separator character (not recommended).                                                                                                                                                                                                                     |

Deprecated options:

|                                   |                                                        |
|:----------------------------------|:-------------------------------------------------------|
| `-a A, --attribute-file=A`        | Give attribute FILE                                    |
| `-A A, --output-attribute-File=A` | Give FILE name to new attributeFile                    |
| `-k K, --keep=K`                  | Keep the original\_id as a newAttribute with name NAME |

3.  `Description.py [options] edgeFile annotFile`

> This script produces a complete summary of the contents of the graph
> contained in the edgeFile, in terms of the descriptors contained in an
> annotation file.

The annotFile is a flat TAB-separated file with columns containing the
attributes of the nodes in the graph.  
It has the following syntax:

|                           |        |     |            |     |            |     |     |              |
|:--------------------------|:-------|:----|:-----------|:----|:-----------|:----|:----|:-------------|
| COMPULSORY header line    | UniqID | TAB | Attribute1 | TAB | Attribute2 | TAB | …   | Attribute\_n |
| OPTIONAL attribute lines: | Node1  | TAB | Value1     | TAB | Value2     | TAB |     | Value\_n     |

The expected output of this script is the content in all attributes of
all nodes in the graph.

This script was conceived to be as flexible as possible: it has
therefore a lot of parameterizing options!  
Basically, it works as follows:

-   Construct an XML configuration file specifying
    -   what components (terminal clustering)
    -   what nodes (node types)
    -   what attributes (list of attributes)
    -   what levels of clustering (trail files)

> The configuration file is generated as a template (named `config.xml`
> by default) when the code is run without one. It is complete (*i.e*
> contains all attributes, for all node types and for all levels) when
> called as follows:

    $ Description.py -c COMP_FILE -H TRAIL_FILE EDGE_FILE ANNOT_FILE

-   COMP\_FILE generates

        * one <mod> element comprising
        * one <filename> field (COMP_FILE)
        * one <name> field ("Module" by default)
        * as many <key> elements as node types, containing each
               - one <type> field (the node type, say 1)
               - one <name> field (NodeType1 by default)
               - one <display> field (Yes/No)

-   TRAIL\_FILE generates

         * as many <trail> elements as levels from the root graph 
           (see the output of $ TrailHistory.py TRAIL_FILE) each comprising
                * one <rank> field (the index in the trail file sequence)
                * one <name> field (the trailFile name)
                * as many <key> elements as node types (same as before)

-   ANNOT\_FILE generates

         *  as many <attr> elements as column names in the ANNOT_FILE header comprising each
               * one <name> field (the column name)
               * one <type> field (the node type for the attribute)
               * one <display> field (Yes/No)

> The complete description file can be **VERY** verbose. The
> configuration file can be manually edited to restrict to some
> elements, according to the following rules:

-   if no `COMP_FILE` is given, every node of the current graph will
    form one component.
-   trail files can be skipped, but take care to adapt the `<rank>`
    field accordingly (as consecutive integers starting from 1).
-   the `<display>` field should be set to *Yes* when the corresponding
    key/attribute should be taken into account, and can be set to
    `<display></display>` for *No*.
-   the `<name>` field of the `<mod>` element can be set at will to
    describe the components, depending on their nature (*e.g.*
    **Connected component**, **Twin component**…)
-   the `<name>` field of the `<key>` element can also be chosen to
    describe the nature of the node types (*e.g.* **Genome** for
    *NodeType1*, and **Twin** or **Gene Family** for *NodeType2* in the
    `BiTwin.py` example).

When passed to the script along with an `edgeFile` and an `annotFile`, 
the code
-   parses all components in the terminal clustering of the current
    graph (`-c COMP-FILE` ; if none is given, then we parse each node of
    the current graph)

-   for each one, visits the previous levels of clustering up to the
    `ROOT` graph (by visiting the tree representing the sequence of
    trail files in a depth-first search).

-   summarizes all the values of the attributes contained in each node
    at each specified level of clustering.

-   The output can be any one of:

    -   a plain text file (readable but difficult to parse) (`-o`
        option)
    -   an XML-formatted file (less readable but parsable) (`-O` option)

-   Options:

| Option                          |                                                       MESSAGE                                                      |                                                                COMMENT                                                               |
|---------------------------------|:------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`                    |                                           show this help message and exit                                          |                                                                                                                                      |
| `-s S, --separator=`            |                                                   Field separator                                                  |                                Modify default separator (as always, not recommended, default = “\\t”)                                |
| `-o O, --outfile=O`             |                                                Give name to outfile                                                |                                                         Default edgeFile.out                                                         |
| `-O O, --xml-Output=O`          |                          Generate XML parsable output description file (no default value)                          |                                                           No default value                                                           |
| `-a, --annotation`              |                                     Restrict annotation file - speedup expected                                    |           Boolean: if the annotation file has many columns that are not used, construct first a temporary restricted file.           |
| `-n N, --nodeList=N`            |                                                  Optional nodeList                                                 |                                                   Restrict to a supplied node list                                                   |
| `-N N, --nodeType=N`            |     Optional nodeType file (value:1 if unipartite, nothing means bipartite, FILE with types in any other case)     |                                                Specify the k-partiteness of the graph.                                               |
| `-i I, --id=I`                  |                                                   Key identifier                                                   |                           Specify the name of the original node identifier (here for instance it’s UniqID)                           |
| `-u U, --unilateral=U`          |                                                  Node types (1/2…)                                                 |                                             Restrict if desired to nodes of a given type.                                            |
| `-T T, --track=T`               | Track empty annotations: STRING will be written as annotation for every entry in graph whose annotation is missing | If a value is missing at a given node for a given attribute, do not ignore, but give it a descriptive name (default “No Annotation”) |
| `-E, --empty`                   |                                 If activated, does not include missing annotations                                 |                                                                Boolean                                                               |
| `-x X, --xml-config=X`          |                                           Specify XML configuration file                                           |     Supply the (compulsory) XML configuration file. NB: if missing a template will automatically be generated (see option `-X` )     |
| `-X X, --generate-xml-config=X` |                                      Generate template XML configuration file                                      |               Use all parameters to generate a template XML configuration file overriding default name (`config.xml` )               |
| `-H H, --history=H`             |                                   Use trailFile FILE history to generate XML file                                  |                       Retrieve and include all intermediate trailFiles (as obtained from the TrailFile history)                      |
| `-c C, --component=C`           |                                 Optional comma-separated embedded component files.                                 |                       Specify terminal overlapping clustering. Fills in the `<mod>` field in the XML template.                       |
| `-D, --display-all`             |                              Display all annotations by default in configuration file                              |                                                                Boolean                                                               |

The following options are deprecated, but may still be useful to
generate the XML template (the recommended way is to use the `-H` option
above):

|                       |                                                                                                                                                                                                                                                                                                   |                                                                                                     |
|-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------:|
| `-t T, --trail-old=T` | Optional comma-separated embedded old trail files to include a previous clustering. Syntax:keyForType1:keyForType2:…=TrailFile1,… If omitted, keyForType2 will not be included in the description, as in keyForType1::=trail1, means tripartite but only nodes of type1 considered at this level. | Deprecated: when used, specifies the sequence of trail files for the XML template (`<trail>` field) |
| `-k K, --keyList=K`   |                                                                Optional keyList. Syntax: key1-type1:type2,key2. This means that key1 has a relevance both for type 1 and type2, and key2 for all; default None means no keys asked.                                                               | Deprecated: activates the `<display>` field for attribute keyX for typeX nodes in the XML template. |

4.  `InducedSubgraph.py [options] in_networkFile out_subnetworkFile`

Computes a subgraph of the input graph, with respect to a subset of
nodes.

-   Options:

| Option                |                                            MESSAGE                                            |                                                                COMMENT                                                                |
|-----------------------|:---------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`          |                                Show this help message and exit                                |                                                                                                                                       |
| `-n N, --nodes=N`     |                                 Give file containing subnodes                                 |                                           Plain file with the node identifiers (one per row)                                          |
| `-N N, --Nodes=N`     |                             Give list of comma-separated subnodes                             |                                             Alternative subnode supply method: -N 0,1,2,3                                             |
| `-c C, --component=C` | Outputs subgraph corresponding to component COMP in compFile FILE (given as a pair FILE,COMP) |                                                                                                                                       |
| `-t T, --type=T`      |               specify type of subgraph on nodes (0:incident,1:induced,-1:remove)              | Type of method used to generate the subgraph: subnodes contain both ends of an edge (incident), at least one (induced), none (remove) |
| `-s S, --separator=S` |                                        Field separator                                        |                                                             Default “\\t”                                                             |

5.  `TrailHistory.py [options] trailFile`

Reconstructs the trail history since the ROOT graph, including all the
calls to `FactorGraph.py`  and the names of the
intermediate trailFiles. This is an independent utility script.  
Input: the last trailFile.

-   Options:

| Option          |                            MESSAGE                            |                                                  COMMENT                                                 |
|-----------------|:-------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------:|
| `-h, --help`    |                Show this help message and exit                |                                                                                                          |
| `-r, --reverse` | Print history in chronological order (starting from the root) | By default, the history is printed backwards. The “root” directory is the one containing the ROOT graph. |

6.  `TransferAnnotations.py [options] annotationFile trailFile outFile`

Updates the annotationFile with the new IDs specified in the trailFile.
In case several old IDs are given the same new ID, the output file will
have as many rows as in the original annotationFile.

-   Options:

| Option           |              MESSAGE             |                                                                   COMMENT                                                                   |
|------------------|:--------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`     |  show this help message and exit |                                                                                                                                             |
| `-H, --header`   | Specify if there’s a header line |                                                                   Boolean                                                                   |
| `-n N, --new=N`  |        Give name of new ID       |                                                               Default=“newID”                                                               |
| `-S, --skip-old` |        Skip old identifier       |                          Boolean (default False): if not activated, the annotation file will have one more column.                          |
| `s, --skip`      |  Skip 2 rows (new trail format)  | Boolean (default True): enable flag (switch to False) if transferring annotations through another kind of community file than a trail file. |

7.  `Cluster.py [options] edgeFile`

Wrapper for several clustering algorithms implemented in igraph:
produces a community file formatted clustering output for the graph
specified in the edgeFile.  
Ensures that the community file has the correct node identifiers (this
can be a problem since igraph automatically renumbers node IDs).

-   Options:

| Option              |              MESSAGE              |
|---------------------|:---------------------------------:|
| `-h, --help`        |  show this help message and exit  |
| `-o O, --outfile=O` |        Give name to outfile       |
| `-m M, --method=M`  | Clustering method (`-m METHOD` ): |

-   ‘fg’: `community_fastgreedy(self, weights=None)`  
    Community structure based on the greedy optimization of modularity.
-   ‘im’:
    `community_infomap(self, edge_weights=None, vertex_weights=None, trials=10)`  
    Finds the community structure of the network according to the
    *Infomap* method of Martin Rosvall and Carl T.
-   ‘le’:
    `community_leading_eigenvector(clusters=None, weights=None, arpack_options=None)`  
    Newman’s leading eigenvector method for detecting community
    structure.
-   ‘lp’:
    `community_label_propagation(weights=None, initial=None, fixed=None)`  
    Finds the community structure of the graph according to the label
    propagation method of Raghavan *et al*.
-   ‘ml’:
    `community_multilevel(self, weights=None, return_levels=False)`  
    Community structure based on the multilevel algorithm of Blondel *et
    al*.
-   ‘om’: `community_optimal_modularity(self, *args, **kwds)`  
    Calculates the optimal modularity score of the graph and the
    corresponding community structure.
-   ‘eb’:
    `community_edge_betweenness(self, clusters=None, directed=True, weights=None)`  
    Community structure based on the betweenness of the edges in the
    network.
-   ‘sg’:
    `community_spinglass(weights=None, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule='config', gamma=1, implementation='orig', lambda_=1)`  
    Finds the community structure of the graph according to the
    spinglass community detection method of Reichardt & Bornholdt.
    *Attention*: only works on connected graphs.
-   ‘wt’: `community_walktrap(self, weights=None, steps=4)`  
    Community detection algorithm of Latapy & Pons, based on random
    walks.

8.  `BiTwin.py [options] blastFile genome2sequenceFile`

Standalone program generating the twin and articulation points analysis
for the genome-gene family bipartite graph. It takes sequence data and
sequence-to-genome assignment as input.

-   Options:

| Option                    |                                           MESSAGE                                           |                                         COMMENT                                        |
|---------------------------|:-------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------:|
| `-h, --help`              |                               show this help message and exit                               |                                                                                        |
| `-s S, --separator=S`     |                               Field separator (default “\\t”)                               |                                                                                        |
| `-n N, --thr=N`           |                    Threshold(s) for sequence similarity (comma-separated)                   | `-n 30,40,50,60,70,80,90,95` will run the analysis for all these similarity thresholds |
| `-c C, --cover=C`         |                        Threshold for reciprocal sequence length cover                       |                                       default 80%                                      |
| `-I I, --input-network=I` |                   Skips `CleanBlast` step with supplied `networkFile FILE`                  |                                                                                        |
| `-f F, --fasta=F`         | Fasta file – if supplied, then the `blast-all` will be run first to generate the blastFile. |         *Attention*: the supplied `blastFile NAME` will be used for the output.        |
| `-A A, --aln=A`           |  Sequence comparison algorithm (b=BLAST/d=DIAMOND) – if `-f` not supplied, silently ignored |                                                                                        |
| `-C C, --clustering=C`    |                    Clustering type for family detection (cc or families)                    |   `cc` uses *Connected Components* as clusters; `families` uses *Louvain communities*  |
| `-o O, --outfile=O`       |                                     Give NAME to outfile                                    |                                                                                        |
| `-a A, --annotation=A`    |                            Annotation file, referenced by UniqID                            |   Used for the last step: analysis and description of components (Twin and supports)   |
| `-i I, --id=I`            |                               Key identifier (default: UniqID)                              |                                          Idem                                          |
| `-k K, --keyList=K`       |     Optional list of keys in annotFile to consider (requires option `-a` – default All)     |                                          Idem                                          |

9.  `BlastAll.py [-h] -i I [-db DB] [-evalue EVALUE] -out OUT -th TH [-fasta_spl FASTA_SPL]`

Runs a parallel BLAST on TH threads for the FASTA input file I, and
stores the output in file OUT.

**NB**: It is recommended that you run your own BLAST for large data
(you know your machine best!).

10.  `ShaveGraph.py [options] in_networkFile out_subnetworkFile`

Removes gene family nodes having degree one.

-   Options:

| Option                |             MESSAGE             | COMMENT |
|-----------------------|:-------------------------------:|:-------:|
| `-h, --help`          | show this help message and exit |         |
| `-d D, --degree=D`    |     Ceiling value for degree    |         |
| `-u U, --type=U`      |    Type of node if bipartite    |         |
| `-s S, --separator=S` |         Field separator         |         |

