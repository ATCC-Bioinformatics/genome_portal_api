# Introduction
This is a set of python scripts that can be used to access the One Codex api. All scripts were created using Python version 3.8. Scripts have been tested in Google Colab (link to notebook available at bottom of README) using Python 3.7. See the demo python notebook for detailed examples:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1feU-VVZzTFrfvRA63KK0NeKRMrAcqxMw?usp=sharing)

# Getting Started
You will need:
* a One Codex account at https://genomes.atcc.org/ to obtain a JWT. This is required for all scripts.
    * Log in or create an account on https://genomes.atcc.org 
    <p align="left">
    <img width="500" src="images/login.png">
     </p>
      
    * Hover over your username on the home page of https://genomes.atcc.org, and select “Profile” from the list that drops down
    <p align="left">  
    <img width="500" src="images/profile.png">
      </p>
    * Click on “Copy JWT” - lasts for 15 minutes before time out.
    <p align="left">
    <img width="500" src="images/copyjwt.png">
      </p>

*   Python 3.7 or higher.
# Pip install
```
python -m venv env
source env/bin/activate
git clone https://github.com/ATCC-Bioinformatics/genome_portal_api.git
pip install /path/to/genome_portal_api
```
# Functions
### search_text()
The search_text() function can be used to find assemblies and their assocaiated metadata that match a search term. The search term can either be a full- or sub-string for an organism name or an exact match of the ATCC catalog number as a character string. For the example below any of the following search terms could have been used to produce a list which contained Yersinia entercolitica: "Yersinia", "enter", "coli", "entercolitica", or "27729".
Usage:
```
To use search_product(), you must include your jwt, a product_id, and a boolean id_only flag. If the 
id_only boolean is set to True, then only the assembly id is retrieved.
E.g., search_product(jwt=YOUR_JWT,product_id=35638,id_only=False) return resulting metadata
E.g., x = search_product(jwt=YOUR_JWT,product_id=35638,id_only=True) return only the assembly id
```
Example:
```
search_text_results=search_text(jwt=jwt,text="coli",id_only=False)
```
`search_text_results` is a list of dictionary objects. The first element is:
```
{'attributes': {'asm_launch': True,
  'atcc_metadata': {'antibiotic_resistance': None,
   'antigenic_prop': 'Biotype 1 serotype 8',
   'bsl': 2,
   'catalog_number': '27729',
   'genotype': None,
   'gold': True,
   'isolation_new_web': 'Human blood Belgium November 7 1972',
   'notes': None,
   'sequencing_technology': None,
   'type_strain': False},
  'biosafety_level': 2,
  'catalog_number': '27729',
  'dna_item': '27729D-5',
  'product_url': 'https://www.atcc.org/Products/All/27729',
  'source_item': '27729'},
 'collection_name': 'bacteriology',
 'description': None,
 'id': '099e5acebc284d19',
 'name': 'ATCC® 27729™',
 'preferred_taxonomy_name': None,
 'product_id': '27729',
 'product_url': 'https://www.atcc.org/Products/All/27729D-5',
 'taxon_name': 'Yersinia enterocolitica'}
```
Specific values from each dictionary can be accessed as follows:
```
[(e['taxon_name'],e['attributes']['atcc_metadata']['catalog_number']) for e in search_text_results]
```
Output:
```
[('Yersinia enterocolitica', '27729'),
 ('Escherichia coli', 'BAA-525'),
 ('Mycolicibacterium fortuitum subsp. fortuitum', '6841'),
 ...
```
### search_product()
The search_product() function is similar to the search_text() function, except it looks for assembly metadata that matches a particular product id. The product id used must be an exact match to return correct results.
```
To use search_product(), you must include your jwt, a product_id, and a boolean id_only flag. If the 
id_only boolean is set to True, then only the assembly id is retrieved.
E.g., search_product(jwt=YOUR_JWT,product_id=35638,id_only=False) return resulting metadata
E.g., x = search_product(jwt=YOUR_JWT,product_id=35638,id_only=True) return only the assembly id
```
Example:
```
product_metadata = search_product(jwt=jwt,product_id="BAA-335", id_only=False)
product_metadata
```
`product_metadata`  holds the following dictionary:
```
[{'attributes': {'atcc_metadata': {'antibiotic_resistance': None,
    'antigenic_prop': 'Serogroup B',
    'bsl': 2,
    'catalog_number': 'BAA-335',
    'genotype': None,
    'gold': None,
    'isolation_new_web': 'Human infection',
    'notes': None,
    'sequencing_technology': None,
    'type_strain': False},
   'product_url': 'https://www.atcc.org/Products/All/BAA-335',
   'scraped_organism_name': 'Neisseria meningitidis (Albrecht and Ghon) Murray (ATCC® BAA-335™)'},
  'collection_name': 'bacteriology',
  'description': None,
  'id': '261b0e41db924d0f',
  'name': 'ATCC® BAA-335™',
  'preferred_taxonomy_name': None,
  'product_id': 'BAA-335',
  'product_url': 'https://www.atcc.org/Products/All/BAA-335',
  'taxon_name': 'Neisseria meningitidis'}]
```
### download_assembly()
The download_assembly() function uses an assembly id to either obtain the link to download an assembly, or download an assembly directly. Here, the assembly id contained in the search_product_assembly_id variable is used to retrieve the assembly download link which can be copied and pasted into any web browser: The first 200 nucleoties of each contig in the assemblies relating to the assembly ids in search_product_assembly_id variable are shown below. If neither the download_link_only or download_assembly options are set to True, the raw json result is returned.
```
To use download_assembly(), you must include your jwt, an assembly ID, a boolean download_link_only flag, and a boolean 
download_assembly flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved. 
If the download_assembly boolean is set to True, then only the assembly download link is retrieved.
E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="True",download_assembly="False") return assembly url
E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="True") return assembly dict 
E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="False") return raw json result
```
Download link example:
```
assembly_download_link=download_assembly(jwt=jwt,id=search_product_results_assembly_id,download_link_only=True,download_assembly=False)
assembly_download_link
```
`assembly_download_link` is the url to access in order to download the assembly:
```
https://s3.amazonaws.com/refgenomics-userdata-production-encrypted/temporary-files/72h/assembly_5_genome_0_taxon_0/Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822_assembly_4a3fc3892d33411f.fasta?response-content-disposition=attachment%3B%20filename%3D%22Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822.fasta%22&AWSAccessKeyId=AKIA6GPUEB7CLCIK2XEI&Expires=1648018077&Signature=biFOkbIIT2VJ0YHJtyk72ZCjwFo%3D
```
Download assembly example:
```
assembly=download_assembly(jwt=jwt,id=search_product_results_assembly_id,download_link_only=False,download_assembly=True)
for contig in assembly:
  print(contig)
  print(assembly[contig][0:200])
```
`assembly` is a dictionary where each key is the contig header and each value is the contig sequence. The output from above:
```
>4a3fc3892d33411f_1 assembly_id="4a3fc3892d33411f" genome_id="a614b8c4a4664441" atcc_catalog_number="ATCC 700822" species="Yersinia enterocolitica subsp. enterocolitica" contig_number="1" topology="circular"
GTGTCACTTTCGCTTTGGCAGCAGTGTCTTGCCCGATTGCAGGATGAGTTACCTGCCACAGAATTTAGTATGTGGATACGCCCCTTACAGGCGGAACTGAGTGACAATACTCTGGCGCTTTACGCACCTAATCGTTTTGTACTGGACTGGGTCCGTGATAAGTACTTAAACAATATCAATGGCTTACTTAATGATTTCTG
>4a3fc3892d33411f_2 assembly_id="4a3fc3892d33411f" genome_id="a614b8c4a4664441" atcc_catalog_number="ATCC 700822" species="Yersinia enterocolitica subsp. enterocolitica" contig_number="2" topology="linear"
TTCAATGAATCCATTCTGCTGCGGGTTTACCCGGTTGAATATGGCACAAAGTAATACCATTATATTCACAGTAATTCAGTAAGTTAACCGATATCAGTTCCGGACCATTATCAACTCTAATTTGCTGAGGCTGTCCACGTTCTTCTTTCAGACGTTCAAGTACGCGGATCACTCTGTTTGCTGGCAAAGAAGTATCGACT
```
### download_annotations()
Similarly to download_assembly, an assembly id is required to be able to download assembly annotations, and it is possible to download only the annotations link rather than the full annotation. Using the assembly ids from search_product_results_assembly_id the download links are retrieved. Annotations are downloaded directly as a GenBank file.
```
To use download_annotations(), you must include your jwt, an assembly ID, a boolean download_link_only flag, and a boolean 
download_annotations flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved.
If the download_annotations boolean is set to True, then only the assembly download link is retrieved.
E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="True",download_annotations="False") return annotation data url 
E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="True") return the raw genbank file
E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="False") return the raw json result
```
Download annotation link example:
```
annotations_download_link=download_annotations(jwt=jwt,id=search_product_results_assembly_id,download_link_only=True,download_annotations=False)
annotations_download_link
```
`annotations_download_link` is the url to access in order to download the annotations:
```
https://s3.amazonaws.com/refgenomics-userdata-production-encrypted/temporary-files/72h/assembly_5_genome_0_taxon_0/Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822_assembly_0518695e1d044c30.gbk?response-content-disposition=attachment%3B%20filename%3D%22Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822.gbk%22&AWSAccessKeyId=AKIA6GPUEB7CLCIK2XEI&Expires=1648018483&Signature=ZYq0cN6ONumf2iHsEQx7%2F4hsctY%3D
```
Download annotations directly example:
```
annotations=download_annotations(jwt=jwt,id=search_product_results_assembly_id,download_link_only=False,download_annotations=True)
for line in annotations.split("\n")[:35]:
  print(line)
```
Output:
```
LOCUS       1                    4533095 bp    DNA     linear   UNK 07-DEC-2021
DEFINITION  Yersinia enterocolitica subsp. enterocolitica ATCC® 700822™, contig
            1.
ACCESSION   assembly_4a3fc3892d33411f_1
VERSION     assembly_4a3fc3892d33411f_1
DBLINK      assembly: 4a3fc3892d33411f
            annotation_set: 0518695e1d044c30
            genome: a614b8c4a4664441
KEYWORDS    .
SOURCE      https://genomes.atcc.org/genomes/a614b8c4a4664441
  ORGANISM  Yersinia enterocolitica subsp. enterocolitica
            cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria;
            Enterobacterales; Yersiniaceae; Yersinia; Yersinia enterocolitica;
            Yersinia enterocolitica subsp. enterocolitica.
COMMENT     Annotated using prokka 1.14.0 from
            https://github.com/tseemann/prokka.
FEATURES             Location/Qualifiers
     source          1..4533095
                     /organism="unknown"
                     /mol_type="genomic DNA"
                     /strain="strain"
     CDS             1..1389
                     /gene="dnaA"
                     /locus_tag="HEHAGAAE_00001"
                     /inference="ab initio prediction:Prodigal:2.6"
                     /inference="similar to AA sequence:UniProtKB:P03004"
                     /codon_start=1
                     /transl_table=11
                     /product="Chromosomal replication initiator protein DnaA"
                     /db_xref="COG:COG0593"
                     /translation="MSLSLWQQCLARLQDELPATEFSMWIRPLQAELSDNTLALYAPNR
                     FVLDWVRDKYLNNINGLLNDFCGSEVPLLRFEVGSKPAVRAHSHPVTASVSAPVAPVTR
                     SAPVRPSWDSSPAQPELSYRSNVNPKHTFDNFVEGKSNQLARAAARQVADNPGGAYNPL
                     FLYGGTGLGKTHLLHAVGNGIMARKANAKVVYMHSERFVQDMVKALQNNAIEEFKRYYR
                     SVDALLIDDIQFFANKERSQEEFFHTFNALLEGNQQIILTSDRYPKEINGVEDRLKSRF
   ...
   ...
```
The annotations can be printed to a file as follows:
```
with open("annotations.gbk", "w") as f:
  for line in annotations.split("\n"):
    f.write(line+"\n")
```
### download_metadata()
In order to download an assembly's metadata using an assembly id when other options are not needed, i.e. links, GenBank files, etc, download_metadata() should be used. download_metadata() produces the detailed metadata for any given assembly id.
```
To use download_metadata(), you must include your jwt and an assembly ID.
E.g., download_metadata(jwt=YOUR_JWT,id=304fd1fb9a4e48ee) return metadata
```
The detailed metadata can be downloaded as follows:
```
assembly_metadata = download_metadata(jwt=jwt,id=search_product_results_assembly_id)
assembly_metadata
```
`assembly_metadata` is a dictionary:
```
{'attributes': {'atcc_metadata': {'antibiotic_resistance': None,
   'antigenic_prop': '3',
   'bsl': 2,
   'catalog_number': '700822',
   'drug_repository': None,
   'genotype': None,
   'gold': None,
   'isolation_new_web': 'Blood',
   'notes': None,
   'sequencing_technology': None,
   'type_strain': False},
  'product_url': 'https://www.atcc.org/Products/700822'},
 'collection_name': 'bacteriology',
 'description': None,
 'id': 'a614b8c4a4664441',
 'name': 'ATCC® 700822™',
 'preferred_taxonomy_name': None,
 'primary_assembly': {'attributes': {'contig_lengths': [4533095, 10119],
   'length': 4543214,
   'qc_statistics': {'assembly_level': 'Chromosome',
    'assembly_statistics': {'filtered': {'contig_statistics': [{'ambiguous_nucleotide_count': 0,
        'circular': True,
        'gc_content': 0.47005809496602213,
        'id': '1',
        'illumina_depth': {'max': 1154,
         'mean': 303.71365479876334,
         'median': 304,
   ...
   ...
```
### download_all_genomes() - Deprecate?
download_all_genomes() allows the user to download all genomes available on https://genomes.atcc.org without prior knowledge of any associated metadata.
```
To use download_all_genomes(), you must include your jwt, and a page number.
E.g., download_all_genomes(jwt=YOUR_JWT,page=1,output="output.txt") return page 1 of metadata
```
### download_catalogue()
download_catalogue() allows the user to download the entire catalogue available on https://genomes.atcc.org and either return a list of all assembly options or save the list to a pkl file. The complete catalogue can be returned from the function as a list by not including an output path. The complete catalogue can be saved to a .pkl file by including an output path. This is required to run the search_fuzzy() function.
```
To use download_catalogue(), you must include your jwt.
E.g., download_catalogue(jwt=YOUR_JWT,output="output.txt")
```
The entire catalogue can be downloaded as follows:
```
catalogue = download_catalogue(jwt=jwt)
catalogue[0]
```
`catalogue` is a list of dictionaries. The first element is:
```
{'attributes': {'atcc_metadata': {'antibiotic_resistance': None,
   'antigenic_prop': None,
   'bsl': 2,
   'catalog_number': 'BAA-1845',
   'drug_repository': None,
   'genotype': None,
   'gold': None,
   'isolation_new_web': 'Patient with typical disseminated gonococcal infection (DGI) symptoms',
   'notes': None,
   'sequencing_technology': 'Illumina + Oxford Nanopore',
   'type_strain': False},
  'product_url': 'https://www.atcc.org/Products/All/BAA-1845'},
 'collection_name': 'bacteriology',
 'description': None,
 'id': 'd2546e5050bc4f63',
 'name': 'ATCC® BAA-1845™',
 'preferred_taxonomy_name': None,
 'product_id': 'BAA-1845',
 'product_url': 'https://www.atcc.org/Products/All/BAA-1845',
 'taxon_name': 'Neisseria gonorrhoeae'}
```
In order to use search_fuzzy(), the catalogue must be saved to file. For example:
```
download_catalogue(jwt=jwt,output="path/to/catalogue.pkl")
```
### search_fuzzy()
search_fuzzy() allows the user to search for a term using fuzzy matching. The function searches through every value in the metadata nested dictionary and looks for a fuzzy match with the search term. To use this function, you must have downloaded the complete catalogue using download_catalogue(jwt=jwt,output="path/to/catalogue.pkl") because the catalogue path is a required argument.
```
To use search_fuzzy(), you must include a search term and the path to the catalogue
downloaded via download_catalogue().
E.g., search_fuzzy(term="coly",catalogue_path="path/to/catalogue.txt") search for the term "coly"
```
For example, searching for the term "yursinia" (a misspelling of yersinia) works as follows:
```
match_list=search_fuzzy(term="yursinia",catalogue_path="path/to/catalogue.pkl")
[e['taxon_name'] for e in match_list]
```
`match_list` is a list of dictionaries. The taxon_name for each element output from the above code:
```
['Yersinia enterocolitica',
 'Yersinia pseudotuberculosis',
 'Yersinia enterocolitica subsp. enterocolitica',
 'Yersinia pestis',
 'Yersinia pseudotuberculosis',
 'Yersinia pseudotuberculosis',
 'Yersinia pestis',
 ...
```
