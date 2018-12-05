_MultiTwin_ package for the analysis of multipartite graphs.

_Authors_: Eduardo Corel & Jananan S. Pathmanathan -- 2014-2018.

CONTENTS:
=========
# _Download methods_

* From this repository: download or clone the zipped archive `MultiTwin-master.zip` into an `INSTALL_DIR`. The `MULTITWIN_DIR` will be `MultiTwin-master`

      $ cd INSTALL_DIR
      $ unzip MultiTwin-master.zip
      $ cd MultiTwin-master	

# _Contents of `MULTITWIN_DIR`_

      $ ls
      install.sh                           Installer script
      INSTALL.md                           Install instructions
      README.md                            this file
      BlastProg/                           program sources in C++
      data/                                test data 
      python-scripts/                      python scripts
    
   `$ ls python-scripts/`

|||
|:---|:---:|
|`bitwin.py`| Runs a complete bipartite graph analysis|
|`blast_all.py`| will make a blast all-against-all|
|`cluster.py`| Cluster algorithm wrapper. Outputs a community file|
|`description.py`|Outputs description files based on an annotation file for a trail history hierarchy of graphs|
|`detect_twins.py`|Computes twin classes of nodes in graph|
|`factorgraph.py`| Factors a graph as communities|
|`bt_launcher.py`|Graphical startup utility for `bitwin.py`| 
|`fg_launcher.py`|Graphical startup utility for `factorgraph.py`|       
|`dt_launcher.py`|Graphical startup utility for `detect_twins.py`|       
|`ds_launcher.py`|Graphical startup utility for `description.py`|       
|`simplify_graph.py`|Removes degree one nodes from graph| 
|`subgraph.py`|Computes subgraph|
|`trailhistory.py`|Recalls commands from `ROOT` graph to current graph|
|`transfer_annotations.py`|Renames attributes according to `trailFile`|
|`utils.py`|Library of functions|
|`xmlform.py`| Graphical utility for XML config file editing|

> Except for `bt_launcher.py, fg_launcher.py, dt_launcher.py, ds_launcher.py, utils.py, xmlform.py`, all files should be executable (if not, change the status with `$ chmod +x *.py`)

`$ ls BlastProg/` 

|||
|---|:---:|
| `cleanBlast/` | `C++` sources for `cleanblast` |
| `cleanblast` | executable |
|  `familyDetector/` | `C++` sources for `familydetector`|
|  `familydetector`  | executable |
| `makefile`  | compiling indications |

> `cleanblast` and `familydetector` should be executable (same remark as above)

    $ ls data/
    genome2seq.txt
    seq.annot
    seq.blastp

> This is a toy example to test the installation.
# _Graphical mode_
 `detect_twins.py`, `factorgraph.py`, `bitwin.py` and `description.py` have a graphical interface mode, invoked on the command line as `program_name.py -G`. Any argument that is passed according to the syntax detailed below will appear in the corresponding field of the graphical interface, where it can also be modified.
 > See the detailed description of the executables below for more explanations.

FORMATS:
=========

A graph is specified by one compulsory and several optional files

- edge file (compulsory)
- node type file (optional: for multipartite graphs, _i.e._ tripartite or higher)
- trail file (optional)

The edge file describes the graph by its edges in a standard way:

    Node1 TAB Node2

> This format is most convenient for storing large graph files, although its main drawback is the unability to store singletons.
> Nodes can be any string (with or without whitespace, although they should definitely avoid TAB characters)

_UNIPARTITE GRAPHS_: no further specification needed. 

_BIPARTITE GRAPHS_: Bipartite graphs are graphs containing two sets of nodes (conventionally called "white" nodes and "black" nodes), such that every edge connects only nodes of different sets.

For bipartite graphs, our code implicitly considers all nodes appearing in the same column to be of the same colour:

    Node1 TAB Node2
    Node3 TAB Node4
    Node1 TAB Node4
    (..)
`Node1` and `Node3` are then, say, white, and `Node2` and `Node4`, black.

NOTE: Any inconsistency in the input file will NOT be caught! If a node appears in both columns, then the graph is not bipartite, but this should be specified (usually by a `-k 1` option).

_MULTIPARTITE GRAPHS_: *k*-partite graphs are graphs whose set of nodes *V*, is partitioned in *k* subsets *V_1,...,V_k* such that an edge only connects nodes from different subsets. 

They must be described with an additional node type file:

    Node1 TAB nodeType1
    Node2 TAB nodeType1
    Node3 TAB nodeType2
    Node4 TAB nodeType2
    Node5 TAB nodeType3
    (...)
 
Details of EXECUTABLE SCRIPTS:
============

1.  `detect_twins.py [options] edgeFile`  
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

> Nodes that form a singleton (*i.e.* whose set of neighbours is unique) are
> not given a twin identifier: the output file can therefore have less
> lines than the number of nodes.

* Options:

| Option                          |                                                    MESSAGE                                                    |                                                                                                                  COMMENT                                                                                                                 |
|---------------------------------|:-------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`  |    show this help message and exit   | |
| `-i, --input_edge_file I`|Input graph edge file| |
| `-o O, --output_twin_file=O`             |                                              Give name to outfile                                             |                                                                 Code gives output the default name: `edgeFile.twins` . Use this option to override with your own choice.                                                                 |
| `-c C, --twin_component_file=C`                | Output comp file for twin and support (_i.e._ both twin nodes and nodes in support receive the same component ID) |                       Output a file where twin nodes and their support are identified by the same integer. ATTENTION: One node will usually have SEVERAL identifiers (all the twin supports that contain this node).                      |
| `-n N, --partiteness=N`          |    Input node type file : Original\_nodeName -\> type of node (in _k_-partite) – Syntax : 1/2 or nodeTypeFile   |                                                           PARTITENESS OPTION: Default is 2. If 1, consider the graph as unipartite; otherwise, you must specify a nodeType file|                                                          | `-u U, --restrict_to_node_types=U`          |        Only detect twins from one side (1/2/3…) depending on the `typeFile` supplied (comma-separated).       | All twins are computed by default: use this option to restrict to nodes of chosen types (`-u 1` for twins for type1 nodes only). Twins are nodes having exactly the same set of neighbours: they are identified by an arbitrary integer. |
| `-m THR, --minimum_support=THR` |                               Minimal threshold for the size of the twin support                              |                                                                           Do not consider as twins nodes whose number of neighbours (degree) is lower than THR.                                                                          |
| `-M M, --minimum_twin_size=M`        |                                   Minimal threshold for the size of the twin                                  |                                                                                              Exclude twin sets composed of less than M nodes                                                                                             |
|`-l L, --log L`|         Specify log file| |
| `-G, --graphical`    |   Launch graphical interface| All values specified on the command line will be included in the interface.|
| `-t T, --twin-support=T`        |         Output twinSupport file (format: ID nbTwinNodes nbSupportNodes SupportNodesIDs (tab-separated)        |                                                                                       Twin support = common set of neighbours. Formatting option 1                                                                                       |
| `-T T, --Twin-Support=T`        |  Output twinSupport file (another format: ID TwinNodesIDs (comma-separated) SupportNodesIDs (comma-separated) |                                                                                                    Alternative format for twin support                                                                                                   |
| `-s S, --separator=S`           |                                                Field separator                                                |                                                                                             Use another separator than TAB (not recommended)                                                                                             |
| `-d, --debug`                   |                                                     Debug                                                     |                                                                                                               Not relevant.                                                                                                              |

2.  `factorgraph.py [options] -i inNetworkFile -o outNetworkFile -T outTrailingFile`

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

A community file simply specifies the community id of the nodes in the
graph, according to the syntax

`Node1 TAB identifier1`  
`Node2 TAB identifier1`  
`Node3 TAB identifier2`  
`Node4 TAB identifier2`  
(…)

A community file and a trail file follow the same syntax, except for a two-line header in the trail file that recalls the process leading to the current graph.

> The trail file is of central importance: it links the original
> `node ID` to the current `node ID` it has been mapped to, starting from the root
> graph.

| ROOT GRAPH                      | (community file 1) | GRAPH\_1                          | (community file 2) | GRAPH\_2                          | …   | GRAPH\_k                          |
|:--------------------------------|:-------------------|:--------------------------------|:-------------------|:--------------------------------|:----|:----------------------------------|
| `edgeFile`: UniqID                | UniqID TAB newID1                   | `edgeFile`: newID1                |  newID1 TAB newID2                  | `edgeFile`: newID2                |     | `edgeFile`: newID\_k                | 
| (`nodeType`: UniqID TAB nodeType) |                    | (`nodeType`: newID1 TAB nodeType) |                    | (`nodeType`: newID2 TAB nodeType) |     | (`nodeType`: newID\_k TAB nodeType) |
|                                 |                    | `trailFile`: UniqID TAB newID1    |                    | `trailFile`: UniqID TAB newID2    |     | `trailFile`: UniqID TAB newID\_k    |

> *Note*: It is possible to change the `ROOT` graph at any step. If one supplies no `trailFile` to `factorgraph.py` , then it is implicitly assumed that the `edgeFile` provided is the (new) `ROOT` graph (and its node identifiers the reference ones).

-   Options:

| Option                  | MESSAGE                                                                                         | COMMENT                                                                                                                                                                                                                                                                |
|:------------------------|:------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h, --help`            | show this help message and exit                                                                 |                                                                                                                                                                                                                                                                        |
| `-i, --input_edge_file INPUT_EDGE_FILE` | Input graph edge file|
| `-o, --output_edge_file OUTPUT_EDGE_FILE` |                         Output graph edge file |
| `-T, --output_trail_file OUTPUT_TRAIL_FILE` | Output trailing file|
| `-d D, --output_directory=D`   | Subdirectory where results will be saved                                                        | Create subdirectory and store output files |
| `-c C, --community_file=C`   | Input community cluster file for the graph factoring                                            | Pass the community file where the first column are current graph node identifiers and the second are the community identifiers.                                                                                                                                        |
| `-f F, --community_file-fasta F` |Input community cluster file in FASTA format for the graph factoring |
| `-C, --keep_community_IDs`    | Keep the identifiers from the community file – requires `-c` option, otherwise silently ignored | By default, all communities are renumbered from 0. Use this option to override and keep original community identifiers. *Attention*: the renumbering for singleton nodes (*i.e.* not belonging to any non trivial community) will start after the largest available label. |
| `-t T, --input_trail_file=T`    | Input trail file : Original\_nodeName -\> current\_nodeName                                  | *VERY IMPORTANT*: the trail file attaches to the `ROOT` node Ids the value of its current super-node: passing the `trailFile` allow to keep a consistent renumbering of the nodes                                                                                        |
| `-n N, --input_node_type_file=N`  | Input node type file : Original\_nodeName -\> type of node (in _k_-partite)                       | *MULTIPARTITE GRAPH*: supply the `nodeType` file with the node types.                                                                                                                                                                                                      |
| `-N N, --output_node_type_file=N` | Output node type file : New\_nodeName -\> type of node (in _k_-partite)                           | *MULTIPARTITE GRAPH*: update the `nodeType` file with the new node identifiers.                                                                                                                                                                                            |
| `-w, --use_weights`          | Use weights (BOOLEAN)                                                                           | When creating the super-nodes, endow them with a weight (currently the number of nodes).                                                                                                                                                                               |
| `-s S, --separator=S`   | Field separator                                                                                 | Specify new separator character (not recommended).                                                                                                                                                                                                                     |
|`-G, --graphical`| Launch graphical interface| All values specified on the command line will be included in the interface.|
|`-l L, --log L`|         Specify log file| |

3.  `description.py [options] edgeFile annotFile`

> This script produces a complete summary of the contents of the graph
> contained in the `edgeFile`, in terms of the attributes contained in an
> annotation file `annotFile`.

The `annotFile` is a flat TAB-separated file with columns containing the
attributes of the nodes in the graph.  It has the following syntax:

| |  | |  | | | |||
|:--------------------------|:-------|:----|:-----------|:----|:-----------|:----|:----|:-------------|
| COMPULSORY header line    | UniqID | TAB | Attribute1 | TAB | Attribute2 | TAB | …   | Attribute\_n |
| OPTIONAL attribute lines: | Node1  | TAB | Value1     | TAB | Value2     | TAB |     | Value\_n     |

The expected output of this script is the content in all attributes of
all nodes in the graph.
This script was conceived to be as flexible as possible: it has
therefore a lot of parameterizing options!  
Basically, it works as a two-step procedure:

1. Construct an XML configuration file `CONFIG_FILE` specifying
   -   what are the components (usually elements of a *terminal* clustering)
   -   what nodes are considered (which *node types*)
   -   which attributes are assigned (list of attributes)
   -   what levels of clustering should be included (*trail files*)
2. Run the script with this configuration file produces description output files, either
   -   a plain text file (readable but difficult to parse)
   -   an XML output file (parsable but more difficult to read).

> The configuration file is generated as a template (named `config.xml`
> by default) when the code is run without one. It is complete (*i.e*
> contains all attributes, for all node types and for all levels) when
> called as follows:

    $ description.py -c COMP_FILE -H TRAIL_FILE [-X CONFIG_FILE] EDGE_FILE ANNOT_FILE

In the `CONFIG_FILE`, the following elements will be generated:

-   corresponding to the `COMP_FILE`

        * one <mod> element comprising
        * one <filename> field (COMP_FILE)
        * one <name> field ("Module" by default)
        * as many <key> elements as node types, containing each
	           - one <type> attribute (the node type, say 1)
               - one <display> attribute (boolean `True/False`)
	           - one <name> field ("NodeType1" by default)

-   corresponding to the `TRAIL_FILE`

         * as many <trail> elements as levels from the root graph 
           (see the output of $ trailhistory.py TRAIL_FILE) each comprising
                - one <rank> field (the index in the trail file sequence)
                - one <name> field (the trailFile name)
                - as many <key> elements as node types (same as before)

-  corresponding to the  `ANNOT_FILE`

         *  as many <attr> elements as column names in the ANNOT_FILE header comprising each
               - one <name> field (the column name)
               - as many <node> elements as node types comprising
                       * one <type> attribute (the node type)
                       * one <display> attribute (True/False)

>The configuration file can be manually or graphically (`-G` option) edited to restrict to some elements, according to the following rules:

-   if no `COMP_FILE` is given, every node of the current graph will
    form one component.
-   trail files can be skipped, but take care to adapt the `<rank>`
    field accordingly (as consecutive integers starting from 1). 
   Alternatively, one can set all the `display`attributes to `False`.
-   the `<display>` field should be set to `<display="True">` when the corresponding
    key/attribute should be taken into account.
-   the `<name>` field of the `<mod>` element can be set at will to
    describe the components, depending on their nature (*e.g.*
    **Connected component**, **Twin component**…)
-   the `<name>` field of the `<key>` element can also be chosen to
    describe the nature of the node types (*e.g.* **Genome** for
    *NodeType1*, and **Twin** or **Gene Family** for *NodeType2* in the
    `bitwin.py` example).

When passed to the script along with an `edgeFile` and an `annotFile`, 
the code
-   parses all components in the terminal clustering of the current
    graph (`-c COMP_FILE` ; if none is given, then we parse each node of
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

_NB_: The complete description files can be **VERY** verbose. 

-   Options:

| Option                          |                                                       MESSAGE                                                      |                                                                COMMENT                                                               |
|---------------------------------|:------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`                    |                                           show this help message and exit                                          |                                                                                                                                      |
| `-i I, --input_edge_file I` |Final edge file of graph |
| `-a- A, --annotation_file A` |Annotation file (relative to ROOT graph)|
| `-k K, --keyList K` |     Optional keyList|
| `-x X, --configuration_file_use X` |Specify XML configuration file and run | Supply the (compulsory) XML configuration file. *NB*: if missing a template will automatically be generated (see option `-X` ) |
| `-K, --update_xml_config` |Launch graphic interface with specified XML configure file (as indicated by `-x` option) -- boolean |Only with the `-x` option -- silently ignored otherwise.|
|`-X X, --configuration_file_generate X` |Generate template XML configuration file ||Use all parameters to generate a template XML configuration file.|
| `-t T, --use_trail_file_unique_level T` |Specify trail file |
| `-H H, --use_trail_file_follow_history H`| Use trailFile FILE history to generate XML file |Retrieve and include all intermediate trailFiles (as obtained from the TrailFile history)|
| `-c C, --component_file C`|Specify component file. If absent, every node of the graph is a component.|Terminal (usually overlapping) clustering. Fills in the `<mod>` field in the XML template.| 
| `-N N, --partiteness N` | Optional nodeType file (value:1 if unipartite, nothing means bipartite, FILE with types in any other case)| Specify the k-partiteness of the graph.|
|  `-o O, --output_plain_file O` |Give name to outfile (default `edgeFile.desc`)|
| `-O O, --output_xml_file O`| Generate XML parsable output description file (no
 default value) |
| `-I I, --unique_node_identifier I` |Key identifier (default 'UniqID')| Specify the name of the original node identifier|
| `-T T, --track T` | Track empty annotations: STRING will be written as annotation for every entry in graph whose annotation is missing (default 'No Annotation')| | If a value is missing at a given node for a given attribute, do not ignore, but give it a descriptive name.| 
| `-E, --empty` |If activated, does not include missing annotations -- boolean|
| `-A, --restrict_annotation` | Restrict annotation file (speedup expected) -- boolean. Activated by default in graphical mode.| If the annotation file has many columns that are not used, construct first a temporary restricted file.            |
| `-G, --graphical`|Launch graphical interface |
| `-l L, --log L`| Specify log file | 
| `-s S, --separator S`|  Field separator (default '\t')|                    Modify default separator (as always, not recommended, default = `“\t”`) 
| `-n N, --nodeList N`|    Optional nodeList|  Restrict to a supplied node list                                                   |
| `-u U, --unilateral U`|  Node types (1/2...)|
| `-D, --display-all`| Display all annotations by default in config file --
 boolean|

4.  `subgraph.py [options] in_networkFile out_subnetworkFile`

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

5.  `trailhistory.py [options] trailFile`

Reconstructs the trail history since the `ROOT` graph, including all the
calls to `factorgraph.py`  and the names of the
intermediate `trailFiles`. This is an independent utility script.  
Input: the last `trailFile`.

-   Options:

| Option          |                            MESSAGE                            |                                                  COMMENT                                                 |
|-----------------|:-------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------------:|
| `-h, --help`    |                Show this help message and exit                |                                                                                                          |
| `-r, --reverse` | Print history in chronological order (starting from the root) | By default, the history is printed backwards. The “root” directory is the one containing the ROOT graph. |

6.  `transfer_annotations.py [options] annotationFile trailFile outFile`

Updates the `annotationFile` with the new `IDs` specified in the `trailFile`.
In case several old IDs are given the same new ID, the output file will
have as many rows as in the original `annotationFile`.

-   Options:

| Option           |              MESSAGE             |                                                                   COMMENT                                                                   |
|------------------|:--------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------:|
| `-h, --help`     |  show this help message and exit |                                                                                                                                             |
| `-H, --header`   | Specify if there’s a header line |                                                                   Boolean                                                                   |
| `-n N, --new=N`  |        Give name of new ID       |                                                               Default=“newID”                                                               |
| `-S, --skip-old` |        Skip old identifier       |                          Boolean (default False): if not activated, the annotation file will have one more column.                          |
| `s, --skip`      |  Skip 2 rows (new trail format)  | Boolean (default True): enable flag (switch to False) if transferring annotations through another kind of community file than a trail file. |

7.  `cluster.py [options] edgeFile`

Wrapper for several clustering algorithms implemented in `igraph`:
produces a community file formatted clustering output for the graph
specified in the `edgeFile`.  
Ensures that the community file has the correct node identifiers (this
can be a problem since `igraph` automatically renumbers node IDs).

-   Options:

| Option              |              MESSAGE              |
|---------------------|:---------------------------------:|
| `-h, --help`        |  show this help message and exit  |
| `-o O, --outfile=O` |        Give name to outfile       |
| `-w, --weight` |    Use edge weights for `method` (boolean)|
| `-m M, --method=M`  | Clustering method (`-m METHOD` ): |

-   `fg: community_fastgreedy(self, weights=None)`  
    Community structure based on the greedy optimization of modularity.
-   `im: community_infomap(self, edge_weights=None, vertex_weights=None, trials=10)`  
    Finds the community structure of the network according to the
    *Infomap* method of Martin Rosvall and Carl T.
-   `le: community_leading_eigenvector(clusters=None, weights=None, arpack_options=None)`  
    Newman’s leading eigenvector method for detecting community
    structure.
-   `lp: community_label_propagation(weights=None, initial=None, fixed=None)`  
    Finds the community structure of the graph according to the label
    propagation method of Raghavan *et al*.
-   `ml: community_multilevel(self, weights=None, return_levels=False)`  
    Community structure based on the multilevel algorithm of Blondel *et
    al*.
-   `om: community_optimal_modularity(self, *args, **kwds)`  
    Calculates the optimal modularity score of the graph and the
    corresponding community structure.
-   `eb: community_edge_betweenness(self, clusters=None, directed=True, weights=None)`  
   Community structure based on the betweenness of the edges in the
    network.
-   `sg: community_spinglass(weights=None, spins=25, parupdate=False, start_temp=1, stop_temp=0.01, cool_fact=0.99, update_rule='config', gamma=1, implementation='orig', lambda_=1)`  
    Finds the community structure of the graph according to the
    spinglass community detection method of Reichardt & Bornholdt.
    *Attention*: only works on connected graphs.
-   `wt: community_walktrap(self, weights=None, steps=4)`  
    Community detection algorithm of Latapy & Pons, based on random
    walks.

8.  `bitwin.py [options] -b blastFile -g genome2sequenceFile`

Standalone program generating the twin and articulation points analysis
for the genome-gene family bipartite graph. It takes sequence data and
sequence-to-genome assignment as input.

-   Options:

| Option                    |                                           MESSAGE                                           |                                         COMMENT                                        |
|----------------------------|:-------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------:|
| `-h, --help`              |                               show this help message and exit                               |                                                                                        |
|  `-b, --blast/diamond_output_file` | Output of `BLAST` or `diamond` program | Required argument|
|  `-g, --genome_to_gene_file`| Supply `GENOME2SEQUENCE`|Required argument|
| `-a A, --annotation_file=A`    |                            Annotation file, referenced by `UniqID`                            |   Used for the last step: analysis and description of components (Twin and supports)   |
| `-k K, --annotation_keys=K`       |     Optional list of keys in annotFile to consider (requires option `-a` – default All)     |                                          Idem                                          |
| `-n N, --indentity_threshold=N`           |                    Threshold(s) for sequence similarity (comma-separated)                   | `-n 30,40,50,60,70,80,90,95` will run the analysis for all these similarity thresholds |
| `-c C, --mutual_cover=C`         |                        Threshold for reciprocal sequence length cover                       |                                       default 80%                                      |
| `-C C, --clustering_method=C`    |                    Clustering type for family detection (cc or families)                    |   `cc` uses *Connected Components* as clusters; `families` uses *Louvain communities*  |
| `-I I, --input_network=I` |              |     Skips `cleanblast` step and uses supplied `networkFile FILE` instead                  |
| `-f F, --fasta=F`         | Fasta file – if supplied, then the `blast-all` will be run first to generate the blastFile. |         *Attention*: the supplied `blastFile NAME` will be used for the output.        |
| `-A A, --similarity_search_software=A`           |  Sequence comparison algorithm (`b=BLAST/d=DIAMOND`) – if `-f` not supplied, silently ignored |                                                                                        |
| `-i I, --unique_node_identifier=I`            |                               Key identifier (default: `UniqID`)                              |                                          |
|`-G, --graphical`| Launch graphical interface| All values specified on the command line will be included in the interface.|
| `-K, --graphic_interface_for_Description`|  Launch graphical configuration interface for Description module | Can be modified on the graphical interface of `bitwin.py`|
|  `-D D, --output_dir D`|  Store all output under `DIR`||
|  `-l L, --log L` |Specify log file | Default `stderr`|
| `-s S, --separator=S`     |                               Field separator (default `“\t”`)                               |  Do not modify                                                                                       |

9.  `blast_all.py [-h] -i I [-db DB] [-evalue EVALUE] -out OUT -th TH [-fasta_spl FASTA_SPL]`

Runs a parallel `BLAST` on `TH` threads for the `FASTA` input file `I`, and
stores the output in file `OUT`.

**NB**: It is recommended that you run your own `BLAST` for large data
(you know your machine best!). Also consider using `diamond`.

10.  `simplify_graph.py [options] in_networkFile out_subnetworkFile`

Removes gene family nodes having bounded degree (default by 1).

-   Options:

| Option                |             MESSAGE             | COMMENT |
|-----------------------|:-------------------------------:|:-------:|
| `-h, --help`          | show this help message and exit |         |
| `-d D, --degree=D`    |     Ceiling value for degree    |default=1|
| `-u U, --type=U`      |    Type of node if *k*-partite  |         |
| `-s S, --separator=S` |         Field separator         |         |
	
