# Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Setup](#Setup)
4. [Functions](#functions)
   1. [search_text](#search_text)
   2. [search_product](#search_product)
   3. [download_assembly](#download_assembly)
      - [Download genome to a fasta file](#download_assembly_fasta_file)
      - [Get genome as a dict()](#download_assembly_as_a_dictionary)
      - [Get link to download genome url](#store_link_to_assembly_url)
   4. [download_annotations](#download_annotations)
      - [Download annotations to a GenBank file](#download_annotations_to_file)
      - [Get annotations as raw output](#download_annotations_raw_ouput)
      - [Get url to download annotations file](#get_link_to_annotations_file)
   5. [download_metadata](#download_metadata)
      - [Download metadata](#download_all_genomes_to_list)
   6. [download_all_genomes](#download_all_genomes)
      - [Download all genomes to a list](#download_all_genomes_to_list)
   7. [download_catalogue](#download_catalogue)
   8. [search_fuzzy](#search_fuzzy)
5. [Cookbook](#cookbook)
   1. [Download all the data for all *E. coli* assemblies](#ex1)
   2. [Download all the data for product 700822](#ex2)
   3. [Download all data for fuzzy search results](#ex3)

# Introduction <a name="introduction"></a>
This is a set of python scripts that can be used to access the One Codex api. All scripts were created using Python version 3.9. Scripts have been tested in Google Colab using Python 3.9. See the demo python notebook for detailed examples:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11hBTFeM4SzHKxPvfiIlwGQHW0YZelfgY?usp=sharing)

# Getting Started <a name="getting-started"></a>
You will need:
1. An ATCC Genome Portal Suporting Membership
    * As of May 1, 2024, a supporting membership is required to access the REST API
    * To purchase a suporting membership, learn more [here](https://www.atcc.org/applications/reference-quality-data/discover-the-atcc-genome-portal)
2. a One Codex account at https://genomes.atcc.org/ to obtain an API Key. This is required for all scripts.
    * Log in or create an account on https://genomes.atcc.org       
    * Proceed to https://genomes.atcc.org/profile 
    * Click on “Copy API Key”

3.   Python 3.9 or higher.
        * Scripts were tested on python 3.9, but use of earlier requirements (v3.7+) should not prohibit usage of the API and functionality.
# Pip install <a name="installation"></a>
### Conda environment
```
conda create -n "genome_portal_api"
conda activate genome_portal_api
git clone https://github.com/ATCC-Bioinformatics/genome_portal_api.git
pip install /path/to/downloaded/genome_portal_api
```
### Python virtual environmnet
```
python -m venv env
source env/bin/activate
git clone https://github.com/ATCC-Bioinformatics/genome_portal_api.git
pip install /path/to/downloaded/genome_portal_api
```
# Setup <a name="Setup"></a>
Activate your evironment, load in the packages / functions, and get started!
```
conda activate genome_portal_api
python 

# Below is ran from within a python session
from genome_portal_api import * #Loads up all functions of the API
```

# Functions <a name="functions"></a>
## search_text() <a name="search_text"></a>
The `search_text()` function can be used to find assemblies and their associated metadata that match a search term. The search term can either be a full- or sub-string of an organism name or an exact match of the ATCC catalog number as a character string. For the example below any of the following search terms could have been used to produce a list which contained Yersinia entercolitica: "Yersinia", "enter", "coli", "entercolitica", or "27729".

**To test out what search terms might help, first try using the "Search for a genome" bar on the [ATCC Genome Portal](https://genomes.atcc.org/).**

Usage:
```
To use search_text(), you must include your api key, a search string and a boolean id_only flag. If the id_only boolean is set 
to True, then only the assembly id is retrieved.

E.g., search_text(api_key=YOUR_API_KEY,text="coli",id_only="False") return resulting metadata
E.g., x = search_text(api_key=YOUR_API_KEY,text="asp",id_only="True") return list of assembly ids
```

<details>
<summary>Advanced</summary>

Example:
```
search_text_results=search_text(api_key=api_key,text="coli",id_only=False)
```
`search_text_results` is a list of dictionary objects. The first element is:
```
{"attributes": {
        "atcc_metadata": {
            "amr_intermediate": [],
            "amr_resistant": [],
            "amr_susceptible": [],
            "antibiotic_resistance": null,
            "antigenic_prop": "Biotype 1",
            "bsl": 2,
            "catalog_number": "27729",
            "drug_repository": null,
            "genotype": null,
            "gold": true,
            "isolation_new_web": "Blood; isolated November 7, 1972",
            "notes": null,
            "preferred_taxonomy_name": null,
            "product_url": "https://www.atcc.org/Products/All/27729D-5",
            "sequencing_technology": null,
            "tag_names": [
                "MSA Component"
            ],
            "tax_id": "630",
            "type_strain": false
        }
      },
  "collection_name": "bacteriology",
  "created_at": "2019-05-14T17:08:28.498440+00:00",
  "description": null,
  "id": "099e5acebc284d19",
  "name": "ATCC 27729",
  "product_id": "27729",
  "product_url": "https://www.atcc.org/Products/All/27729D-5",
  "taxon_id": "630",
  "taxon_name": "Yersinia enterocolitica"
}
... "Shortened for cleanliness"

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
</details>

## search_product() <a name="search_product"></a>
The `search_product()` function is similar to the search_text() function, except it looks for assemblies that match a particular product id. The product id used must be an **exact** match to return correct results.
```
To use search_product(), you must include your api_key, a product_id, and a boolean id_only flag. If the 
id_only boolean is set to True, then only the assembly id is retrieved.
E.g., search_product(api_key=YOUR_API_KEY,product_id=35638,id_only=False) return resulting metadata
E.g., x = search_product(api_key=YOUR_API_KEY,product_id=35638,id_only=True) return only the assembly id
```

<details>
<summary>Advanced</summary>

Example:
```
product_metadata = search_product(api_key=api_key,product_id="BAA-335", id_only=False)
product_metadata
```
`product_metadata`  holds the following dictionary:
```
[{"attributes": {
    "atcc_metadata": {
    "amr_intermediate": [],
    "amr_resistant": [],
    "amr_susceptible": [],
    "antibiotic_resistance": null,
    "antigenic_prop": null,
    "bsl": 2,
    "catalog_number": "BAA-335",
    "drug_repository": null,
    "genotype": null,
    "gold": null,
    "isolation_new_web": "Infection",
    "notes": null,
    "preferred_taxonomy_name": null,
    "product_url": "https://www.atcc.org/products/baa-335",
    "sequencing_technology": null,
    "tag_names": ["MSA Component"],
    "tax_id": "487",
    "type_strain": false
      }
    },
  "collection_name": "bacteriology",
  "created_at": "2020-02-26T18:58:47.303264+00:00",
  "description": null,
  "id": "261b0e41db924d0f",
  "name": "ATCC BAA-335",
  'preferred_taxonomy_name': None,
  'product_id': 'BAA-335',
  'product_url': 'https://www.atcc.org/Products/All/BAA-335',
  'taxon_name': 'Neisseria meningitidis'}]

... "Intentionally shortened for cleanliness"
```
</details>

## download_assembly() <a name="download_assembly"></a>
The download_assembly() function uses an genome id to either obtain the link to download an assembly or download an assembly directly.
```
  To use download_assembly(), you must include:
  - api_key=<Your api_key>
  - id=<GenomeID>
  One or more of the flags below should be present:
    - Boolean 'download_link_only' flag     (returns temporary assembly url) 
    - Boolean 'download_assembly_dict' flag (returns assembly file dictionary; [key]=header,[value]=sequence)
    - Boolean 'download_assembly_file' flag (download assembly fasta file to provided path "below")
      - 'download_assembly_path'  (Needed for 'download_assembly_file'; quoted str path to folder) 
  E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_assembly_file=True,download_assembly_path="/directory/for/download/") downloads an assembly file to provided path  
  E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only=True) return assembly url
  E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_assembly_dict=True) return assembly dict 
  E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_assembly_dict=True) return raw json result
```

<details>
<summary>Advanced</summary>

### Download fasta file example: <a name="download_assembly_fasta_file"></a>
```
download_assembly(api_key=api_key,id=genome_id,download_assembly_file=True,download_assembly_path="/path/to/folder")
```
This will download the fasta file directly to the folder provided for the "download_assembly_path" argument

### Download assembly as a dictionary example: <a name="download_assembly_as_a_dictionary"></a>
```
assembly=download_assembly(api_key=api_key,id=genome_id,download_assembly_dict=True)
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
The output from the above code block prints each link of the .gbk file.
### Download link example: <a name="store_link_to_assembly_url"></a>
```
assembly_download_link=download_assembly(api_key=api_key,id=genome_id,download_link_only=True)
assembly_download_link
```
`assembly_download_link` is the url to access in order to download the assembly:
```
https://s3.amazonaws.com/refgenomics-userdata-production-encrypted/temporary-files/72h/assembly_5_genome_0_taxon_0/Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822_assembly_4a3fc3892d33411f.fasta?response-content-disposition=attachment%3B%20filename%3D%22Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822.fasta%22&AWSAccessKeyId=AKIA6GPUEB7CLCIK2XEI&Expires=1648018077&Signature=biFOkbIIT2VJ0YHJtyk72ZCjwFo%3D
```
</details>  

## download_annotations() <a name="download_annotations"></a>
Similar to `download_assembly()`, an assembly id is required for the `download_annotations()`, which can be used to either obtain the download link or to download the annotations directly. The annotations are in .gbk format.
```
  To use download_annotations(), you must include:
    - api_key=<Your api_key>
    - id=<GenomeID>
  One or more of the flags below should be present:
    - Boolean 'download_link_only' flag        (returns temporary annotations url) 
    - Boolean 'download_annotations_dict' flag (returns GenBank raw string)
    - Boolean 'download_annotations_file' flag (downloads GenBank file to provided path "below")
      - 'download_annotations_path'           (Needed for 'download_annotations_file'; quoted str path to download GenBanks)\n
  E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="True") return annotation data url 
  E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_annotations_dict="True") return the raw genbank file
  E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_annotations_file="True",download_annotations_path="/directory/for/download") Download the GenBank file to provided path.
```
<details>
<summary>Advanced</summary>

### Download annotations to a GenBank file example:  <a name="download_annotations_to_file"></a>
```
download_annotations(api_key=api_key,id=genome_id,download_annotations_file=True,download_annotations_path="/path/to/folder")
```
The above will directly download a GenBank file to your provided path.

### Download annotations output directly example:  <a name="download_annotations_raw_ouput"></a>
```
annotations=download_annotations(api_key=api_key,id=genome_id,download_annotations_dict=True)
for line in annotations.split("\n"):
  print(line)
```
The output from the above code block prints each link of the .gbk file.
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
### Get annotation link example:  <a name="get_link_to_annotations_file"></a>
```
annotations_download_link=download_annotations(api_key=api_key,id=genome_id,download_link_only=True)
annotations_download_link
```
`annotations_download_link` is the url to access in order to download the annotations:
```
https://s3.amazonaws.com/refgenomics-userdata-production-encrypted/temporary-files/72h/assembly_5_genome_0_taxon_0/Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822_assembly_0518695e1d044c30.gbk?response-content-disposition=attachment%3B%20filename%3D%22Yersinia_enterocolitica_subsp_enterocolitica_ATCC_700822.gbk%22&AWSAccessKeyId=AKIA6GPUEB7CLCIK2XEI&Expires=1648018483&Signature=ZYq0cN6ONumf2iHsEQx7%2F4hsctY%3D
```
</details>

## download_metadata() <a name="download_metadata"></a>
`download_metadata()` should be used to obtain the detailed metadata including qc statistics, contig length(s), etc. for any given assembly id.
```
To use download_metadata(), you must include your api_key and an assembly ID.
E.g., download_metadata(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee) return metadata
```
<details>
<summary>Advanced</summary>

### Download metadata example <a name="download_metadata_as_dict"></a>
The detailed metadata can be downloaded as follows:
```
assembly_metadata = download_metadata(api_key=api_key,id=genome_id)
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
</details>

## download_all_genomes() <a name="download_all_genomes"></a>
download_all_genomes() allows the user to download all genomes available on https://genomes.atcc.org without prior knowledge of any associated metadata.
```
  To use download_all_genomes(), you must include your api_key, and a page number.
  
  E.g., download_all_genomes(api_key=YOUR_API_KEY) returns all metadata
```

<details>
<summary>Advanced</summary>

### Download all genome entries as list example: <a name="download_all_genomes_to_list"></a>
Running the below code will generate a list of every genome's metadata
```
genomes=download_all_genomes(api_key='YOUR_API_KEY')
```
This will output a stored variable `genomes`. This object is a list of dictionaries representing all genomes available in the portal. This will also print a message about the collection:

> Fetched 4,500 genomes  
> genomes visibility='public': 4,500

This list can then be leveraged into `download_assembly` or `download_annotations` in order to download each item to file. Each genome's ID can be found in the "id" keys of each dictionary:
```
genomes[0]['id']
> '21846cfe916b4f18'
```
</details>

### download_catalogue() <a name="download_catalogue"></a>
`download_catalogue()` allows the user to download the entire catalogue available on https://genomes.atcc.org and either return a list of all assembly metadata or save the list to a pkl file. The complete catalogue can be returned from the function as a list by not including an output path. The complete catalogue can be saved to a .pkl file by including an output path. **Saving to file is required to run the search_fuzzy() function**.
```
To use download_catalogue(), you must include your api_key.
E.g., download_catalogue(api_key=YOUR_API_KEY,output="output.txt")
```
<details>
<summary>Advanced</summary>

The entire catalogue can be downloaded as follows:
```
catalogue = download_catalogue(api_key=api_key)
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
download_catalogue(api_key=api_key,output="path/to/catalogue.pkl")
```

</details>

### search_fuzzy() <a name="search_fuzzy"></a>
`search_fuzzy()` allows the user to search for a term using fuzzy matching. The function searches through every value in the metadata nested dictionary and looks for a fuzzy match with the search term. To use this function, you must have downloaded the complete catalogue using download_catalogue(api_key=api_key,output="path/to/catalogue.pkl") because the catalogue path is a required argument.
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
# Cookbook <a name="cookbook"></a>

<details>
<summary>Click to view cookbook</summary>

## Download all the data for all *E. coli* assemblies <a name="ex1"></a>
First, we search for Escherichia coli using `search_text()`. Then we iterate through the results list, create a dictionary entry for each assembly, and then download and store the assembly, annotations, and metadata. The first 3 assemblies are downloaded below.
```
search_text_results=search_text(api_key=api_key,text="Escherichia coli",id_only=False)
e_coli_data = {}
# Download assembly, annotations, and metadata for first 5 
for e in search_text_results[:3]:
  id = e['id']
  e_coli_data[id] = {}
  e_coli_data[id]["assembly"] = download_assembly(api_key=api_key,id=e['id'],download_link_only=False,download_assembly=True)
  e_coli_data[id]["annotations"] = download_annotations(api_key=api_key,id=e['id'],download_link_only=False,download_annotations=True)
  e_coli_data[id]["metadata"] = download_metadata(api_key=api_key,id=e['id'])
 ```
 ```
 for id in e_coli_data.keys():
  print("First 150 nts of each contig")
  for contig in e_coli_data[id]["assembly"].keys():
    print(contig)
    print(e_coli_data[id]["assembly"][contig][0:150])
  print("\nFirst 10 lines of the annotation data:")
  for line in e_coli_data[id]["annotations"].split("\n")[:10]:
    print(line)
  print("\nSome example metadata:")
  print("contig_lengths:",e_coli_data[id]["metadata"]["primary_assembly"]["attributes"]["contig_lengths"])
  print("checkm_results:",e_coli_data[id]["metadata"]["primary_assembly"]["attributes"]["qc_statistics"]["checkm_results"])
  break
```
Output:
```
First 150 nts of each contig
>8ee16eff570c4cef_1 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="1" topology="linear"
TTGGCGCATTAAAACCTGGCGCACGCCTGATTACTAAAAATCTGGCGGAGCAATTAGGTATGAGTATTACACCTGTGCGTGAAGCATTATTACGTCTGGTTTCGGTGAATGCGCTTTCTGTCGCACCTGCACAAGCATTTACAGTTCCGG
>8ee16eff570c4cef_2 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="2" topology="linear"
TACTAAGCTGATGTTTCAGGTCGTTCTCAACCTGCAGAGTCAAACTGACATGTTTCATTTTTCCCGTTCCAGGCATTTTAATTCCTTCGCGTGTTTTCTGTCCAACCCTGCCTGCATGGCAGAAGGAATTCACCTGGTGTATTAAAGTGA
>8ee16eff570c4cef_3 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="3" topology="linear"
TCGGCAAAGGAGCCATGGATTCTAGCAACTAACTTACCTGTTGAAATTCGAACACCCAAACAACTTGTTAATATCTATTCGAAGCGAATGCAGATTGAAGAAACCTTCCGAGACTTGAAAAGTCCTGCCTACGGACTAGGCCTACGCCAT
>8ee16eff570c4cef_4 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="4" topology="linear"
CGCTGAGTAGATTTTAGGTGACGGGTGGTGACAATGAGTCCGTGTCGAGCGCTGATTTTTTCGGCCTTTAGAGCGAGATTTATACAATAGAATTTGGCATGAGATTGGATTGCTTTTAGTCAGCCTCTTATAGCCTAAAGTCTTTGAGTG
>8ee16eff570c4cef_5 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="5" topology="linear"
TTACTTGACTGTAAAACTCTCACTCTTACCGAACTTGGCCGTAACCTGCCAACCAAAGCGAGAACAAAACATAACATCAAACGAATCGACCGATTGTTAGGTAATCGTCACCTCCACAAAGAGCGACTCGCTGTATACCGTTGGCATGCT
>8ee16eff570c4cef_6 assembly_id="8ee16eff570c4cef" genome_id="aa07e8781d624001" atcc_catalog_number="ATCC BAA-525" species="Escherichia coli" contig_number="6" topology="linear"
GAGAGTCGTGTAAAATATCGAGTTCGCACATTTTGTTGTCTGATTATTGATTTTTGGCGAAACCATTTGATCATATGACAAGATGTGTATCTACCTTAACTTAATGATTTTGATAAAAATCATTAGGGGATTCATCAG

First 10 lines of the annotation data:
LOCUS       1                    4631769 bp    DNA     linear   UNK 12-AUG-2021
DEFINITION  Escherichia coli ATCC® BAA-525™, contig 1.
ACCESSION   assembly_8ee16eff570c4cef_1
VERSION     assembly_8ee16eff570c4cef_1
DBLINK      assembly: 8ee16eff570c4cef
            annotation_set: bda19b71c6d7400c
            genome: aa07e8781d624001
KEYWORDS    .
SOURCE      https://genomes.atcc.org/genomes/aa07e8781d624001
  ORGANISM  Escherichia coli

Some example metadata:
contig_lengths: [4631769, 31262, 445, 413, 206, 138]
checkm_results: {'completeness': 99.96693121693121, 'contamination': 0.03720238095238095}
```
## Download all the data for product 700822 <a name="ex2"></a>
First, we use `search_product` to download the assembly metadata from which we pull out the assembly id. Then, we download the assembly, annotations, and metadata.
```
search_products_results=search_product(api_key=api_key,product_id="700822",id_only=False)
id = search_products_results[0]['id']
assembly=download_assembly(api_key=api_key,id=id,download_link_only=False,download_assembly=True)
annotations=download_annotations(api_key=api_key,id=id,download_link_only=False,download_annotations=True)
metadata=download_metadata(api_key=api_key,id=id)
```
```
print("First 150 nts of each contig")
for contig in assembly.keys():
  print(contig)
  print(assembly[contig][0:150])
print("\nFirst 10 lines of the annotation data:")
for line in annotations.split("\n")[:10]:
  print(line)
print("\nSome example metadata:")
print("Filtered contig N50 value:",metadata["primary_assembly"]["attributes"]["qc_statistics"]["assembly_statistics"]["filtered"]["n50"])
print("Filtered contig GC content:",metadata["primary_assembly"]["attributes"]["qc_statistics"]["assembly_statistics"]["filtered"]["gc_content"])
print("Illumina data:",metadata["primary_assembly"]["attributes"]["qc_statistics"]["sequencing_statistics"]["illumina"]["depth"])
print("ONT data:",metadata["primary_assembly"]["attributes"]["qc_statistics"]["sequencing_statistics"]["ont"]["reads"])
```
Output:
```
First 150 nts of each contig
>4a3fc3892d33411f_1 assembly_id="4a3fc3892d33411f" genome_id="a614b8c4a4664441" atcc_catalog_number="ATCC 700822" species="Yersinia enterocolitica subsp. enterocolitica" contig_number="1" topology="circular"
GTGTCACTTTCGCTTTGGCAGCAGTGTCTTGCCCGATTGCAGGATGAGTTACCTGCCACAGAATTTAGTATGTGGATACGCCCCTTACAGGCGGAACTGAGTGACAATACTCTGGCGCTTTACGCACCTAATCGTTTTGTACTGGACTGG
>4a3fc3892d33411f_2 assembly_id="4a3fc3892d33411f" genome_id="a614b8c4a4664441" atcc_catalog_number="ATCC 700822" species="Yersinia enterocolitica subsp. enterocolitica" contig_number="2" topology="linear"
TTCAATGAATCCATTCTGCTGCGGGTTTACCCGGTTGAATATGGCACAAAGTAATACCATTATATTCACAGTAATTCAGTAAGTTAACCGATATCAGTTCCGGACCATTATCAACTCTAATTTGCTGAGGCTGTCCACGTTCTTCTTTCA

First 10 lines of the annotation data:
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

Some example metadata:
Filtered contig N50 value: 4533095
Filtered contig GC content: 0.46992943761839084
Illumina data: {'max': 1154, 'mean': 303.12891886668774, 'median': 304.0, 'min': 12, 'stdev': 43.0585172469467}
ONT data: {'N50': 30777, 'ambiguous_bases': 0, 'median_quality': 25, 'median_quantized_percent_gc': 40, 'median_read_length': 9478, 'position_specific_quality_scores': {}, 'quantized_percent_gc_histogram': {'20': 49, '30': 2514, '40': 66891, '50': 8085, '60': 12}, 'total_bases': 1255401398, 'total_gc_bases': 589992714, 'total_reads': 77551}
```
## Download all data for fuzzy search results <a name="ex3"></a>
First, we use `search_fuzzy` to download the assembly metadata for all items that fuzzy match "yersinia." Then, we pull out the assembly id for each and download the assembly, annotations, and metadata.
```
match_list=search_fuzzy(term="yersinia",catalogue_path="catalogue.pkl")
yersinia_data = {}
for e in match_list[:3]:
  id = e['id']
  yersinia_data[id] = {}
  yersinia_data[id]["assembly"] = download_assembly(api_key=api_key,id=e['id'],download_link_only=False,download_assembly=True)
  yersinia_data[id]["annotations"] = download_annotations(api_key=api_key,id=e['id'],download_link_only=False,download_annotations=True)
  yersinia_data[id]["metadata"] = download_metadata(api_key=api_key,id=e['id'])
```
```
for id in yersinia_data.keys():
  print("First 150 nts of each contig")
  for contig in yersinia_data[id]["assembly"].keys():
    print(contig)
    print(yersinia_data[id]["assembly"][contig][0:150])
  print("\nFirst 10 lines of the annotation data:")
  for line in yersinia_data[id]["annotations"].split("\n")[:10]:
    print(line)
  print("\nSome example metadata:")
  print("taxon:",yersinia_data[id]["metadata"]["taxon"])
  break
```
Output:
```
First 150 nts of each contig
>02048bb2e6674f9c_1 assembly_id="02048bb2e6674f9c" genome_id="099e5acebc284d19" atcc_catalog_number="ATCC 27729" species="Yersinia enterocolitica" contig_number="1" topology="circular"
GTGTCACTTTCGCTTTGGCAGCAGTGTCTTGCCCGATTGCAGGATGAGTTACCTGCCACAGAATTTAGTATGTGGATACGCCCCTTACAGGCGGAACTGAGTGACAATACTCTGGCGCTTTACGCACCTAATCGTTTTGTACTGGACTGG
>02048bb2e6674f9c_2 assembly_id="02048bb2e6674f9c" genome_id="099e5acebc284d19" atcc_catalog_number="ATCC 27729" species="Yersinia enterocolitica" contig_number="2" topology="circular"
GTGGATAAGCAGAAATTCTCTAATTTTTCTAAAGATCATTCTTGGGAAGATATTGATTTTGAAGCACTAGAACGAGCTTCAATCGAATATTTTCAAGAACAGACTTCTTTCGATACATCCAAAACTGAAAAGAAAAGAACGCTTCGGAAA

First 10 lines of the annotation data:
LOCUS       1                    4551126 bp    DNA     linear   UNK 19-SEP-2019
DEFINITION  Yersinia enterocolitica ATCC® 27729™, contig 1.
ACCESSION   assembly_02048bb2e6674f9c_1
VERSION     assembly_02048bb2e6674f9c_1
DBLINK      assembly: 02048bb2e6674f9c
            annotation_set: 4d8f7c47c7c44494
            genome: 099e5acebc284d19
KEYWORDS    .
SOURCE      https://genomes.atcc.org/genomes/099e5acebc284d19
  ORGANISM  Yersinia enterocolitica

Some example metadata:
taxon: {'name': 'Yersinia enterocolitica', 'parents': [{'name': 'Yersinia', 'rank': 'genus', 'tax_id': 629}, {'name': 'Yersiniaceae', 'rank': 'family', 'tax_id': 1903411}, {'name': 'Enterobacterales', 'rank': 'order', 'tax_id': 91347}, {'name': 'Gammaproteobacteria', 'rank': 'class', 'tax_id': 1236}, {'name': 'Proteobacteria', 'rank': 'phylum', 'tax_id': 1224}, {'name': 'Bacteria', 'rank': 'superkingdom', 'tax_id': 2}, {'name': 'cellular organisms', 'rank': 'no rank', 'tax_id': 131567}], 'rank': 'species', 'tax_id': 630}
```
</details>