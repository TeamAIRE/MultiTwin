This is the _README_ file for the pathogen-non pathogen dataset presented in the paper "_MultiTwin_: a software suite to analyse multipartite graphs" by Corel _et al_.

### The contents of the directory `data`  is as follows:

| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`Seq.fasta`|The sequences from all prokaryotes in FASTA format.|| 
|`Seq.blastp` | The result of the all-against-all BLAST run on the `Seq.fasta`  file (E-value <= 1e-5).| This file is the first compulsory argument for the BiTwin.py program.|
|`GenomeToSeq.txt` | This file contains all matches between sequences and genomes. It follows the syntax `X TAB Y`  where `X`  is the identifier of a genome and `Y`  the identifier of a sequence.| It is the second compulsory argument for the `BiTwin.py`  program. It is also the root graph for the bipartite analysis.|
|`complete.annot` | The annotation file for both sequences and genomes.|Fields having no match for a given row are shown with a dash ("-").|


* To run the analysis, install the _MultiTwin_ suite as indicated in the README file of the MultiTwin1.1 directory, and then

        $ cd data
        $ BiTwin.py -a complete.annot -n 30,40,50,60,70,80,90,95 -C [cc or families] Seq.blastp GenomeToSeq.txt

* _Optionally_, one can run the `blast` all-against-all parallel step:

        $ BiTwin.py -a complete.annot -n 30,40,50,60,70,80,90,95 -C [cc or families] -f Seq.fasta Seq_alt.blastp GenomeToSeq.txt 

_NB_: use a different name for the `blast`  output (here `Seq_alt.blastp`) to avoid overwriting the supplied output file.

### OUTPUT FILES:
> The previous commands produce the following hierarchy of directories and files.

- in `current_dir` 

| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`Seq.blastp.cleanNetwork` |Sequence-similarity graph obtained by keeping the best reciprocal hit (>=30% ID) with reciprocal minimum coverage of 80%. | Sequence IDs are renumbered.|
|`Seq.blastp.cleanNetwork.genes` | List of new sequence IDs| Internal use only.|
|`Seq.blastp.cleanNetwork.dico` | Correspondence between initial IDs and sequence ids.|Internal use only.|

- in `graphsXX/`  (for `XX=30,40,50,60,70,80,90,95`):
| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`[CC/family].nodes` | Community file for gene families.||
|`[CC/family].edges` |Fasta-formatted list of edges for each gene family.|Includes singletons _i.e._ families without edges.|
|`[CC/family].info` |Graph statistics for the gene families.||
|`graph.edges` | The bipartite graph obtained by factoring the `GenomeToSeq.txt`  ROOT graph by the gene family file.|The weight in the third column is _log_(nb of original edges).|
|`graph.trail` | The corresponding trail file.||
|`graph0.edges` |The bipartite graph obtained by removing all degree one gene families.||
|`graph0.twins` |The community file describing the twin mapping.||
|`graph0.twin_comp` | The community file describing the twin+support overlapping clustering.||

- in `graphsXX/TwinQuotient/` :
| File | DESCRIPTION |
|--------|:-----------|
|`graph1.edges` |The bipartite graph obtained by factoring `graph0.edges`  by the `graph0.twins`  file.|
|`graph1.trail` |The corresponding trail file.|
|`graph1.art` | List of articulation points of `graph1` |
|`graph1.twins` | Twin file of `graph1` |
|`graph1.twin_comp` |Community file describing the twin support overlapping clustering of `graph1` |

### DESCRIPTION FILES
| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`graph1.config` |XML configuration file (generated automatically).|Requires additional files|
|`complete.annot` || 	Used by `graph1.config` to identify keys.|
|`Data/graphsXX/TwinQuotient/graph1.trail` ||Used by `graph1.config` to identify intermediate levels.|
|`Data/graphsXX/graph1.twin_comp`||Used by `graph1.config` to define modules (overlapping clusters).|
|`graph1.desc` |Output of the `Description.py` program for the twin support.| Plain text format.|
|`graph1.xml_desc` | Output of the `Description.py`  program for the twin support.| Parsable XML format.|

## EXAMPLE OF OUTPUT:  `Module 6`  (Twin + support) at `XX=95` 

|Module|Level 2|Level 1|Root Level|
|--------|:-----------|:------|:-----------|:------|
|`NodeType1` Support |43, 51	(Genomes)|76088,14444 (Genomes)|Escherichia coli BW2952, Capnocytophaga gingivalis ATCC 33624 (Genomes)|
|`NodeType2` Twin|0 (Twin Gene Families)| 1046,1656,1657 (Gene Families)| 2 COG1974, 2 NA, 2 NA (Genes)|

In `graph1.desc`, this appears under this format:

    Module 6
    =========================================== level 2
    ++++++++++++++++++++++++++++++++++++++++ 3 groups
    NodeType2 0
    {'COGID': {'NA': 4, 'COG1974': 2}, 'DESCRIPTION': {'NA': 4, 'SOS-response transcriptional repressors (RecA-mediated autopeptidases)': 2}, 'CC': {'12578': 2, '12577': 2, '4430': 2}, 'COGCAT': {'NA': 4, 'KT': 2}, 'PATH': {'1': 3, '2': 3}, 'SPECIES': {'59391': 3, '55451': 3}}
     ---------------------------------------
     NodeType1 43
     {'Shorthand ID': {'Eco': 1}, 'Pathogen': {'2': 1}, 'Genome Project ID': {'PRJNA59391': 1}, 'Species': {'Escherichia coli BW2952': 1}}
     ---------------------------------------
     NodeType1 51
     {'Shorthand ID': {'Cgi': 1}, 'Pathogen': {'1': 1}, 'Genome Project ID': {'PRJNA55451': 1}, 'Species': {'Capnocytophaga gingivalis ATCC 33624': 1}}
     ---------------------------------------
     =========================================== level 1
     ++++++++++++++++++++++++++++++++++++++++ 5 groups
     NodeType2 1046
     {'COGID': {'COG1974': 2}, 'DESCRIPTION': {'SOS-response transcriptional repressors (RecA-mediated autopeptidases)': 2}, 'CC': {'4430': 2}, 'COGCAT': {'KT': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59391': 1, '55451': 1}}
     ---------------------------------------
     NodeType2 1657
     {'COGID': {'NA': 2}, 'DESCRIPTION': {'NA': 2}, 'CC': {'12577': 2}, 'COGCAT': {'NA': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59391': 1, '55451': 1}}
     ---------------------------------------
     NodeType2 1656
     {'COGID': {'NA': 2}, 'DESCRIPTION': {'NA': 2}, 'CC': {'12578': 2}, 'COGCAT': {'NA': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59391': 1, '55451': 1}}
     ---------------------------------------
     NodeType1 76088
     {'Shorthand ID': {'Eco': 1}, 'Pathogen': {'2': 1}, 'Genome Project ID': {'PRJNA59391': 1}, 'Species': {'Escherichia coli BW2952': 1}}
     ---------------------------------------
     NodeType1 14444
     {'Shorthand ID': {'Cgi': 1}, 'Pathogen': {'1': 1}, 'Genome Project ID': {'PRJNA55451': 1}, 'Species': {'Capnocytophaga gingivalis ATCC 33624': 1}}
    ---------------------------------------
    #############################################

In `graph1.xml_desc`, the same module is described as follows:

    <mod "name"=Module "id"=6>
    <content>
	<attr "name"=COGID>
		{'NA': 4, 'COG1974': 2}
	</attr>
	<attr "name"=DESCRIPTION>
		{'NA': 4, 'SOS-response transcriptional repressors (RecA-mediated autopeptidases)': 2}
	</attr>
	<attr "name"=Genome Project ID>
		{'PRJNA59391': 1, 'PRJNA55451': 1}
	</attr>
	<attr "name"=CC>
		{'12578': 2, '12577': 2, '4430': 2}
	</attr>
	<attr "name"=COGCAT>
		{'NA': 4, 'KT': 2}
	</attr>
	<attr "name"=Species>
		{'Escherichia coli BW2952': 1, 'Capnocytophaga gingivalis ATCC 33624': 1}
	</attr>
	<attr "name"=PATH>
		{'1': 3, '2': 3}
	</attr>
	<attr "name"=Shorthand ID>
		{'Eco': 1, 'Cgi': 1}
	</attr>
	<attr "name"=SPECIES>
		{'59391': 3, '55451': 3}
	</attr>
	<attr "name"=Pathogen>
		{'1': 1, '2': 1}
	</attr>
    </content>
    <trail "level"=2>
    <key "name"=NodeType2 "type"=2 "id"=0>
	<attr "name"=COGID>
		{'NA': 4, 'COG1974': 2}
	</attr>
	<attr "name"=DESCRIPTION>
		{'NA': 4, 'SOS-response transcriptional repressors (RecA-mediated autopeptidases)': 2}
	</attr>
	<attr "name"=CC>
		{'12578': 2, '12577': 2, '4430': 2}
	</attr>
	<attr "name"=COGCAT>
		{'NA': 4, 'KT': 2}
	</attr>
	<attr "name"=PATH>
		{'1': 3, '2': 3}
	</attr>
	<attr "name"=SPECIES>
		{'59391': 3, '55451': 3}
	</attr>
    </key>
    <key "name"=NodeType1 "type"=1 "id"=43>
	<attr "name"=Shorthand ID>
		{'Eco': 1}
	</attr>
	<attr "name"=Pathogen>
		{'2': 1}
	</attr>
	<attr "name"=Genome Project ID>
		{'PRJNA59391': 1}
	</attr>
	<attr "name"=Species>
		{'Escherichia coli BW2952': 1}
	</attr>
    </key>
    <key "name"=NodeType1 "type"=1 "id"=51>
	<attr "name"=Shorthand ID>
		{'Cgi': 1}
	</attr>
	<attr "name"=Pathogen>
		{'1': 1}
	</attr>
	<attr "name"=Genome Project ID>
		{'PRJNA55451': 1}
	</attr>
	<attr "name"=Species>
		{'Capnocytophaga gingivalis ATCC 33624': 1}
	</attr>
    </key>
    </trail>
    <trail "level"=1>
    <key "name"=NodeType2 "type"=2 "id"=1046>
	<attr "name"=COGID>
		{'COG1974': 2}
	</attr>
	<attr "name"=DESCRIPTION>
		{'SOS-response transcriptional repressors (RecA-mediated autopeptidases)': 2}
	</attr>
	<attr "name"=CC>
		{'4430': 2}
	</attr>
	<attr "name"=COGCAT>
		{'KT': 2}
	</attr>
	<attr "name"=PATH>
		{'1': 1, '2': 1}
	</attr>
	<attr "name"=SPECIES>
		{'59391': 1, '55451': 1}
	</attr>
    </key>
    <key "name"=NodeType2 "type"=2 "id"=1657>
	<attr "name"=COGID>
		{'NA': 2}
	</attr>
	<attr "name"=DESCRIPTION>
		{'NA': 2}
	</attr>
	<attr "name"=CC>
		{'12577': 2}
	</attr>
	<attr "name"=COGCAT>
		{'NA': 2}
	</attr>
	<attr "name"=PATH>
		{'1': 1, '2': 1}
	</attr>
	<attr "name"=SPECIES>
		{'59391': 1, '55451': 1}
	</attr>
    </key>
    <key "name"=NodeType2 "type"=2 "id"=1656>
	<attr "name"=COGID>
		{'NA': 2}
	</attr>
	<attr "name"=DESCRIPTION>
		{'NA': 2}
	</attr>
	<attr "name"=CC>
		{'12578': 2}
	</attr>
	<attr "name"=COGCAT>
		{'NA': 2}
	</attr>
	<attr "name"=PATH>
		{'1': 1, '2': 1}
	</attr>
	<attr "name"=SPECIES>
		{'59391': 1, '55451': 1}
	</attr>
    </key>
    <key "name"=NodeType1 "type"=1 "id"=76088>
	<attr "name"=Shorthand ID>
		{'Eco': 1}
	</attr>
	<attr "name"=Pathogen>
		{'2': 1}
	</attr>
	<attr "name"=Genome Project ID>
		{'PRJNA59391': 1}
	</attr>
	<attr "name"=Species>
		{'Escherichia coli BW2952': 1}
	</attr>
    </key>
    <key "name"=NodeType1 "type"=1 "id"=14444>
	<attr "name"=Shorthand ID>
		{'Cgi': 1}
	</attr>
	<attr "name"=Pathogen>
		{'1': 1}
	</attr>
	<attr "name"=Genome Project ID>
		{'PRJNA55451': 1}
	</attr>
	<attr "name"=Species>
		{'Capnocytophaga gingivalis ATCC 33624': 1}
	</attr>
    </key>
    </trail>
    </mod>

