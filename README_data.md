This is the _README_ file for the pathogen-non pathogen dataset presented in the paper ["_MultiTwin_: a software suite to analyze evolution at multiple levels of organization using multipartite graphs"](https://doi.org/10.1093/gbe/evy209) by Corel _et al_.


### The contents of the directory `data`  is as follows:

| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`Seq.fasta`|The sequences from all prokaryotes in FASTA format.|| 
|`Seq.blastp` | The result of the all-against-all BLAST run on the `Seq.fasta`  file (E-value <= 1e-5).| This file is the first compulsory argument for the BiTwin.py program.|
|`GenomeToSeq.txt` | This file contains all matches between sequences and genomes. It follows the syntax `X TAB Y`  where `X`  is the identifier of a genome and `Y`  the identifier of a sequence.| It is the second compulsory argument for the `bitwin.py`  program. It is also the root graph for the bipartite analysis.|
|`complete.annot` | The annotation file for both sequences and genomes.|Fields having no match for a given row are shown with a dash ("-").|


* To run the analysis, install the _MultiTwin_ suite as indicated in the README file of the MultiTwin1.2 directory, and then

        $ cd data
        $ bitwin.py -a complete.annot -n 30,40,50,60,70,80,90,95 -C [cc or families] -b Seq.blastp -g GenomeToSeq.txt

* _Optionally_, one can run the `blast` all-against-all parallel step:

        $ bitwin.py -a complete.annot -n 30,40,50,60,70,80,90,95 -C [cc or families] -f Seq.fasta -b Seq_alt.blastp -g GenomeToSeq.txt 

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
|
File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`[CC/family].nodes` | Community file for gene families.||
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
|`graph1.art` | List of articulation points of `graph1` and the biconnected components it is contained in (comma-separated).|
|`graph1.twins` | Twin file of `graph1`. |
|`graph1.twin_comp` |Community file describing the twin support overlapping clustering of `graph1`. |
|`graph1.bic_comp` |Community file describing the biconnected component (overlapping) clustering of `graph1`. |

### DESCRIPTION FILES

| File | DESCRIPTION | COMMENT |
|--------|:-----------|:------|
|`graph1.config` |XML configuration file (generated automatically).|Requires additional files|
|`complete.annot` || 	Used by `graph1.config` to identify keys.|
|`Data/graphsXX/TwinQuotient/graph1.trail` ||Used by `graph1.config` to identify intermediate levels.|
|`Data/graphsXX/graph1.twin_comp`||Used by `graph1.config` to define modules (overlapping clusters).|
|`graph1.desc` |Output of the `description.py` program for the twin support.| Plain text format.|
|`graph1.xml_desc` | Output of the `description.py`  program for the twin support.| Parsable XML format.|

## EXAMPLE OF OUTPUT:  `Module 6`  (Twin + support) at `XX=95` 

|Module|Level 2|Level 1|Root Level|
|--------|:-----------|:------|:-----------|
|`NodeType1` Support |48, 54	(Genomes)|64897,68995 (Genomes)|Aeromonas hydrophila subsp. hydrophila ATCC 7966, Tolumonas auensis DSM 9187 (Genomes)|
|`NodeType2` Twin|15 (Twin Gene Families)|253,264,531,585,764,871 (Gene Families)|2 COG0267, 2 COG0361, 2 COG0100, 2 COG0126, 2 COG0335, 2 COG0148 (Genes)|

In `graph1.desc`, this appears under this format:

    Module 6
    Pathogen	{'1': 1, '2': 1}
    CC	{'597': 2, '3015': 2, '2158': 2, '1940': 2, '706': 2, '2155': 2}
    Species	{'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1, 'Tolumonas auensis DSM 9187': 1}
    Genome Project ID	{'PRJNA58617': 1, 'PRJNA59395': 1}
    Shorthand ID	{'Tau': 1, 'Ahy': 1}
    COGCAT	{'G': 4, 'J': 8}
    PATH	{'1': 6, '2': 6}
    COGID	{'COG0267': 2, 'COG0361': 2, 'COG0100': 2, 'COG0126': 2, 'COG0335': 2, 'COG0148': 2}
    DESCRIPTION	{'Enolase': 2, '3-phosphoglycerate kinase': 2, 'Ribosomal protein S11': 2, 'Ribosomal protein L19': 2, 'Translation initiation factor 1 (IF-1)': 2, 'Ribosomal protein L33': 2}
    SPECIES	{'59395': 6, '58617': 6}
    =========================================== level 2
    ++++++++++++++++++++++++++++++++++++++++ 3 groups
    NodeType2 15
    {'COGID': {'COG0267': 2, 'COG0361': 2, 'COG0100': 2, 'COG0126': 2, 'COG0335': 2, 'COG0148': 2}, 'CC': {'597': 2, '3015': 2, '2158': 2, '1940': 2, '706': 2, '2155': 2}, 'COGCAT': {'G': 4, 'J': 8}, 'PATH': {'1': 6, '2': 6}, 'SPECIES': {'59395': 6, '58617': 6}, 'DESCRIPTION': {'Enolase': 2, '3-phosphoglycerate kinase': 2, 'Ribosomal protein S11': 2, 'Ribosomal protein L19': 2, 'Translation initiation factor 1 (IF-1)': 2, 'Ribosomal protein L33': 2}}
    ---------------------------------------
    NodeType1 48
    {'Genome Project ID': {'PRJNA58617': 1}, 'Pathogen': {'1': 1}, 'Shorthand ID': {'Ahy': 1}, 'Species': {'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1}}
    ---------------------------------------
    NodeType1 54
    {'Genome Project ID': {'PRJNA59395': 1}, 'Pathogen': {'2': 1}, 'Shorthand ID': {'Tau': 1}, 'Species': {'Tolumonas auensis DSM 9187': 1}}
    ---------------------------------------
    =========================================== level 1
    ++++++++++++++++++++++++++++++++++++++++ 8 groups
    NodeType2 871
    {'COGID': {'COG0335': 2}, 'CC': {'3015': 2}, 'COGCAT': {'J': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'Ribosomal protein L19': 2}}
    ---------------------------------------
    NodeType2 253
    {'COGID': {'COG0361': 2}, 'CC': {'2155': 2}, 'COGCAT': {'J': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'Translation initiation factor 1 (IF-1)': 2}}
    ---------------------------------------
    NodeType2 531
    {'COGID': {'COG0126': 2}, 'CC': {'706': 2}, 'COGCAT': {'G': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'3-phosphoglycerate kinase': 2}}
    ---------------------------------------
    NodeType2 585
    {'COGID': {'COG0148': 2}, 'CC': {'597': 2}, 'COGCAT': {'G': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'Enolase': 2}}
    ---------------------------------------
    NodeType2 764
    {'COGID': {'COG0100': 2}, 'CC': {'2158': 2}, 'COGCAT': {'J': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'Ribosomal protein S11': 2}}
    ---------------------------------------
    NodeType2 264
    {'COGID': {'COG0267': 2}, 'CC': {'1940': 2}, 'COGCAT': {'J': 2}, 'PATH': {'1': 1, '2': 1}, 'SPECIES': {'59395': 1, '58617': 1}, 'DESCRIPTION': {'Ribosomal protein L33': 2}}
    ---------------------------------------
    NodeType1 68995
    {'Genome Project ID': {'PRJNA59395': 1}, 'Pathogen': {'2': 1}, 'Shorthand ID': {'Tau': 1}, 'Species': {'Tolumonas auensis DSM 9187': 1}}
    ---------------------------------------
    NodeType1 64897
    {'Genome Project ID': {'PRJNA58617': 1}, 'Pathogen': {'1': 1}, 'Shorthand ID': {'Ahy': 1}, 'Species': {'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1}}
    ---------------------------------------
    #############################################

In `graph1.xml_desc`, the same module is described as follows:

    <mod name="Module" id="6">
    <content>
	    <attr name="Pathogen">
		    {'1': 1, '2': 1}
	    </attr>
	    <attr name="CC">
		    {'597': 2, '3015': 2, '2158': 2, '1940': 2, '706': 2, '2155': 2}
	    </attr>
	    <attr name="Species">
		    {'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1, 'Tolumonas auensis DSM 9187': 1}
	    </attr>
	    <attr name="Genome Project ID">
		    {'PRJNA58617': 1, 'PRJNA59395': 1}
	    </attr>
	    <attr name="Shorthand ID">
		    {'Tau': 1, 'Ahy': 1}
	    </attr>
	    <attr name="COGCAT">
	            {'G': 4, 'J': 8}
	    </attr>
	    <attr name="PATH">
		    {'1': 6, '2': 6}
	    </attr>
	    <attr name="COGID">
		{'COG0267': 2, 'COG0361': 2, 'COG0100': 2, 'COG0126': 2, 'COG0335': 2, 'COG0148': 2}
	    </attr>
	    <attr name="DESCRIPTION">
		    {'Enolase': 2, '3-phosphoglycerate kinase': 2, 'Ribosomal protein S11': 2, 'Ribosomal protein L19': 2, 'Translation initiation factor 1 (IF-1)': 2, 'Ribosomal protein L33': 2}
	    </attr>
	    <attr name="SPECIES">
		    {'59395': 6, '58617': 6}
	    </attr>
    </content>
    <trail level="2">
    <key name="NodeType2" type="2" id="15">
	    <attr name="COGID">
		    {'COG0267': 2, 'COG0361': 2, 'COG0100': 2, 'COG0126': 2, 'COG0335': 2, 'COG0148': 2}
 	    </attr>
	    <attr name="CC">
		    {'597': 2, '3015': 2, '2158': 2, '1940': 2, '706': 2, '2155': 2}
	    </attr>
	    <attr name="COGCAT">
		    {'G': 4, 'J': 8}
	    </attr>
	    <attr name="PATH">
		    {'1': 6, '2': 6}
  	    </attr>
	    <attr name="SPECIES">
		    {'59395': 6, '58617': 6}
	    </attr>
	    <attr name="DESCRIPTION">
		    {'Enolase': 2, '3-phosphoglycerate kinase': 2, 'Ribosomal protein S11': 2, 'Ribosomal protein L19': 2, 'Translation initiation factor 1 (IF-1)': 2, 'Ribosomal protein L33': 2}
	    </attr>
    </key>
    <key name="NodeType1" type="1" id="48">
	    <attr name="Genome Project ID">
		    {'PRJNA58617': 1}
	    </attr>
	    <attr name="Pathogen">
		    {'1': 1}
	    </attr>
	    <attr name="Shorthand ID">
		    {'Ahy': 1}
	    </attr>
		<attr name="Species">
		{'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1}
	</attr>
	</key>
	<key name="NodeType1" type="1" id="54">
		<attr name="Genome Project ID">
			{'PRJNA59395': 1}
		</attr>
		<attr name="Pathogen">
			{'2': 1}
		</attr>
		<attr name="Shorthand ID">
			{'Tau': 1}
		</attr>
		<attr name="Species">
			{'Tolumonas auensis DSM 9187': 1}
		</attr>
	</key>
	</trail>
	<trail level="1">
	<key name="NodeType2" type="2" id="871">
		<attr name="COGID">
			{'COG0335': 2}
		</attr>
		<attr name="CC">
			{'3015': 2}
		</attr>
		<attr name="COGCAT">
			{'J': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'Ribosomal protein L19': 2}
		</attr>
	</key>
	<key name="NodeType2" type="2" id="253">
		<attr name="COGID">
			{'COG0361': 2}
		</attr>
		<attr name="CC">
			{'2155': 2}
		</attr>
		<attr name="COGCAT">
			{'J': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'Translation initiation factor 1 (IF-1)': 2}
		</attr>
	</key>
	<key name="NodeType2" type="2" id="531">
		<attr name="COGID">
			{'COG0126': 2}
		</attr>
		<attr name="CC">
			{'706': 2}
		</attr>
		<attr name="COGCAT">
			{'G': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'3-phosphoglycerate kinase': 2}
		</attr>
	</key>
	<key name="NodeType2" type="2" id="585">
		<attr name="COGID">
			{'COG0148': 2}
		</attr>
		<attr name="CC">
			{'597': 2}
		</attr>
		<attr name="COGCAT">
			{'G': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'Enolase': 2}
		</attr>
	</key>
	<key name="NodeType2" type="2" id="764">
		<attr name="COGID">
			{'COG0100': 2}
		</attr>
		<attr name="CC">
			{'2158': 2}
		</attr>
		<attr name="COGCAT">
			{'J': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'Ribosomal protein S11': 2}
		</attr>
	</key>
	<key name="NodeType2" type="2" id="264">
		<attr name="COGID">
			{'COG0267': 2}
		</attr>
		<attr name="CC">
			{'1940': 2}
		</attr>
		<attr name="COGCAT">
			{'J': 2}
		</attr>
		<attr name="PATH">
			{'1': 1, '2': 1}
		</attr>
		<attr name="SPECIES">
			{'59395': 1, '58617': 1}
		</attr>
		<attr name="DESCRIPTION">
			{'Ribosomal protein L33': 2}
		</attr>
	</key>
	<key name="NodeType1" type="1" id="68995">
		<attr name="Genome Project ID">
			{'PRJNA59395': 1}
		</attr>
		<attr name="Pathogen">
			{'2': 1}
		</attr>
		<attr name="Shorthand ID">
			{'Tau': 1}
		</attr>
		<attr name="Species">
			{'Tolumonas auensis DSM 9187': 1}
		</attr>
	</key>
	<key name="NodeType1" type="1" id="64897">
		<attr name="Genome Project ID">
			{'PRJNA58617': 1}
		</attr>
		<attr name="Pathogen">
			{'1': 1}
		</attr>
		<attr name="Shorthand ID">
			{'Ahy': 1}
		</attr>
		<attr name="Species">
			{'Aeromonas hydrophila subsp. hydrophila ATCC 7966': 1}
		</attr>
	</key>
	</trail>
	</mod>
 
