<a href="https://genomes.atcc.org/"><img src="https://github.com/ATCC-Bioinformatics/genome_portal_api/blob/dev/images/Genome Portal_728x90.jpg" alt="Clickable-Awesome-Portal-portal" /></a>

# Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Installation](#installation)
4. [Setup](#Setup)
    - [Setting an API key](#setting_api_key)
4. [Tips and FAQ](#FAQ)
4. [Functions](#functions)  
   1. [search_product](#search_product)
      - [Return results as JSON](#search_product_json)
      - [Return results as a table](#search_product_table)
   2. [search_text](#search_text)
      - [Return results as JSON](#search_text_json)
      - [Return results as a table](#search_text_table)
   3. [download_assembly](#download_assembly)
      - [Download genome to a fasta file](#download_assembly_fasta_file)
      - [Get genome as a dict()](#download_assembly_as_a_dictionary)
   4. [download_annotations](#download_annotations)
      - [Download annotations to a GenBank file](#download_annotations_to_file)
      - [Get annotations as raw output](#download_annotations_raw_ouput)
   5. [download_metadata](#download_metadata)
      - [Download metadata](#download_all_genomes_to_list)
   6. [download_all_genomes](#download_all_genomes)
      - [download all genome metadata to a list](#download_all_genomes_to_list)
      - [Convert list to GenomeID Indexing](#convert_to_genomeid)
   8. [deep_search](#deep_search)
      - [Fuzzy search with incorrect spelling](#deep_search_fuzzy)
      - [Search for a biosafety level in table output](#deep_search_fuzzy_contig)
   9. [tabulate](#tabulate)  
          - 
5. [Cookbook](#cookbook)
   1. [Download all the data for all *E. coli* assemblies](#ex1)
   2. [Download all the data for product 700822](#ex2)
   3. [Download all data for fuzzy search results](#ex3)

# Introduction <a name="introduction"></a>
This is a set of python scripts that can be used to access the ATCC Genome Portal through the One Codex REST-API. This API provides extensively more data than can be seen on the ATCC Genome Portal GUI. [While One Codex documentation](https://docs.onecodex.com/en/articles/5812163-atcc-genome-portal-api-guide) exists to detail the exact endpoints, this repo serves as prebuilt and formatted wrappers to navigate the REST API.

All scripts were created using Python version 3.9. Scripts have been tested in Google Colab using Python 3.9. See the demo python notebook for detailed walkthroughs: \
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
pip install /path/to/downloaded/genome_portal_api_folder
```
### Python virtual environmnet
```
python -m venv env
source env/bin/activate
git clone https://github.com/ATCC-Bioinformatics/genome_portal_api.git
pip install /path/to/downloaded/genome_portal_api_folder
```
# Setup <a name="Setup"></a>
Activate your evironment, load in the packages / functions, and get started!
```
conda activate genome_portal_api
python 

# Below is ran from within a python session
>>> from genome_portal_api import * #Loads up all functions of the API
```
## Setting a global api key <a name="setting_api_key"></a>
**If you have the `global_api_key` variable set in your environment, you do not need to provide an `api_key` argument to any function.** If this is your first time using the API, we advise to set and export your API key under the global variable `ATCC_GENOME_PORTAL_API_KEY` in your .bashrc file. To verify your API key is set, call the function `get_global_apikey()`.

Otherwise, we recommend setting your api_key globally on script startup. This can be done a few ways below:
```
Best Option:
(.bashrc file) EXPORT ATCC_GENOME_PORTAL_API_KEY="yourapikeygoeshere"
>>> set_global_api()
2024-07-29 14:20:08,021 - INFO - API key has been found: "yourapikeygoeshere" 

Option 1 - "Manual override or set"
>>> set_global_api(api_key="testing")
2024-07-29 14:24:13,860 - INFO - API key is now set: 'testing'. Please export this api_key under the variable 'ATCC_GENOME_PORTAL_API_KEY'!

Option 2 - "Set on the fly; Quickstart"
>>> search_product(product_id='TSD-364') #Most functions will envoke the call
2024-07-29 19:27:12,996 - INFO - API key has been found: 'testing'
{'ATCC TSD-364': '4a3251f108a044c3'}

Option 3 - "Not in os.eviron"
>>> set_global_api()
Please enter the API key: 'testing'
2024-07-29 14:24:13,860 - INFO - API key is now set: 'testing. Please export this api_key under the variable 'ATCC_GENOME_PORTAL_API_KEY'!

Option 4 - "Test your group membership API keys"
>>> search_product(product_id='TSD-364',api_key='badapikey')
2024-07-29 19:40:57,305 - CRITICAL - API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe.

```

#  Tips & FAQ <a name="FAQ"></a>  
<details>  
<summary>Click to Expand</summary>  

### -- Do I need to provide an API key to each function call??? 
Absolutely not! The recommended way is to set your API key in the global variable `ATCC_GENOME_PORTAL_API_KEY`. This can be written into and explicitly exported from your `.bashrc` file. At anytime, you can also overwrite your API Key from within a function by providing it as an argument, making it avalailable for all functions. Please look above to section "Setting a global api key" to learn how to set an API key in more detail.  
```
set_global_api(api_key='yourapikey')
```

### -- Which output is best???
Simply put, whichever is best for you! **For most functions, there is a choice of output.**  
I will breakdown the output here:

* #### table:

Personally this is our favorite output mode. In this mode, a pandas dataframe is returned as the output of the function. Each row is a unique different genome/assembly, and the JSON metadata is meaningfully auto-formatted and named in a human-readable way! We are continually improving the captured and reported metadata, so keep checking back for more updates!  

* #### json:

This is like legendary mode...There is much more data behind each genome, but reporting on it for most use-cases is challenging for brevity. We are working on a wiki to explain each metadata field in the JSON, but feel free to raise an issue if you need help!
* #### id:  

Bread and butter! One of the most-used cases in the past API behavior, this output is strictly a list of IDs, so that each list entry is the ATCC catalog number followed by the genomeID. ex( ['ATCC 10536:996d977f03724ce6', ...])

</details>  <br />

# Functions <a name="functions"></a>
## search_product() <a name="search_product"></a>
**The `search_product()` function is intended to give an exact match to an ATCC Catalog number / product ID.**  
The product id used in this function must be an **exact** match to return results. Expected output of this function is a single item list, signifying the matched genome for that catalog number.  
This function mimics the GUI ability of using the "Search for a genome" bar on the ATCC Genome Portal set to the "Catalog Number" filter.

<details markdown="1">
<summary>Usage</summary>

```
search_product() is intended for EXACT matching of ATCC product numbers.
This mimics the function of using the search bar on the ATCC Genome Portal set to CATALOG NUMBER 
      
--------- USAGE ---------
Required arguments:
    product_id = <str>
          An ATCC product_id (ex. "BAA-2889")  

Optional arguments:
  output = <str> 
        The API response output format [(id) | json | table]
  api_key = <str>
        Your Genome Portal APIKey [default looks for global_api_key]       

EXAMPLES:
  > search_product(product_id='35638') Return resulting Genome ID for ATCC 35638
  > search_product(product_id='35638', api_key='apikey') Same as above, but this time with a new apikey
  > search_product(product_id='35638', output='json') Return resulting JSON metadata for ATCC 35638
  > search_product(product_id='35638', output='table') Return resulting JSON metadata for ATCC 35638 in a informative table
```

<details>
<summary>Advanced</summary>

### Outputing product metadata as JSON format <a name="search_product_json"></a>
Example:
```
product_metadata = search_product(product_id="BAA-335",output="json")
product_metadata
```
`product_metadata`  holds the following dictionary:
```
["attributes": {
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
  "other_metadata": {
    "catalog_details": {
      "ATCC_catalog_number": "ATCC BAA-335",
      "ATCC_lot_number": "70055783"
    },
    "genome_provider": {
      "annotatated_by": "ATCC",
      "annotations_date": "04/12/2024 05:10:20",
      "annotations_software": "PGAP",
      "asssembled_by": "One Codex",
      "asssembler_software": "Illumina + Oxford Nanopore Unicycler Hybrid Assembly",
      "asssembly_date": "12/08/22 00:14:05"
    },
  },
  "collection_name": "bacteriology",
  "created_at": "2020-02-26T18:58:47.303264+00:00",
  "description": null,
  "id": "261b0e41db924d0f",
  "name": "ATCC BAA-335",
  'preferred_taxonomy_name': None,
  'product_id': 'BAA-335',
  'product_url': 'https://www.atcc.org/Products/All/BAA-335',
  'taxon_name': 'Neisseria meningitidis'}}]

... "Intentionally shortened for cleanliness"
```
### Outputing product metadata as table <a name="search_product_table"></a>
Example:

```
search_product_table = search_product(product_id="BAA-335",output="table")
```
`search_product_table` is a human-readable dataframe. Each result is populated as a single row, and the relevant JSON metadata is automatically pulled and formatted under each column!

```
  atcc_product_id                 name            taxid     genome_id        assembly_id        collection    isolation_new_web  biosafety_level   notes
0     BAA-335             Neisseria meningitidis   487  261b0e41db924d0f  62a2a65ba33541af  ATCC Bacteriology   Infection               2          None

```

</details></details>



## search_text() <a name="search_text"></a>
**The `search_text()` function can be used to find assemblies and/or associated metadata for genomes that match a search term.**  
This function mimics default behavior of the "Search for a genome" bar on the ATCC Genome Portal. The search term can either be a full- or sub-string of an organism name, or an exact match of the ATCC catalog number as a character string.   
**The default output of this function is a list of ids formatted like ['ATCC CatalogNo:GenomeID', ... ]**.

**To test out what search terms might help, first try using the "Search for a genome" bar on the [ATCC Genome Portal](https://genomes.atcc.org/).**

<details markdown="1">
<summary>Usage</summary>


```
search_text() is intended for exact string matching or substring matching on taxonomic names. This will also capture partial matching of ATCC product numbers. 
This mimics the function of using the search bar default on the ATCC Genome Portal, but DOESNOT FULLY SUPPORT FUZZY MATCHING

--------- USAGE ---------
Required arguments:
  text = <str>
        A free text field to search by (ex. "Salmonella enterica")\n            

Optional arguments:
  output = <str>
        The API response format "output" [(id) | json | table]
  api_key = <str>
        Your Genome Portal APIKey [Globally set "global_api_key" or entered"api_key"]      

EXAMPLES:
  > search_text(text='coli') return resulting Genome IDs that match that string
  > search_text(text='coli',output="table") return resulting metadata in TABULAR output for genomes that contain that text string
  > metadata = search_text(api_key='YOUR_API_KEY',text='coli',output="table") Same as above, but with a manually entered API Key to overwrite set
  > search_text(text='coli', output="json") return resulting metadata in table-form for genomes that contain that text string
```

<details>
<summary>Advanced</summary>
For the example below, any of the following search terms could have been used to produce a list which contained Escherichia coli: "Escherichia", "Esch", "coli", "richia", or "35401".

### Outputing search results metadat as JSON format <a name="search_text_json"></a>
Example:

```
search_text_results=search_text(text="coli",output="table")
```
`search_text_results` is a human-readable dataframe. Each search result is populated as a new row, and the relevant JSON metadata is automatically pulled and formatted under each column!

```
  atcc_product_id                                           name   taxid  ...                                  isolation_new_web biosafety_level notes
0             35401                               Escherichia coli     562  ...                                              Feces               2  None
1            700928                               Escherichia coli     562  ...  Blood and urine from woman with acute pyelonep...               2  None
2             27729  Yersinia enterocolitica subsp. enterocolitica  150052  ...                   Blood; isolated November 7, 1972               2  None
3              8739                               Escherichia coli     562  ...                                              Feces               1  None
4             23715  Yersinia enterocolitica subsp. enterocolitica  150052  ...     Blood, petechiae, from anterior chamber of eye               2  None
..              ...                                            ...     ...  ...                                                ...             ...   ...
296           49920                      Mycobacterium confluentis   28047  ...                           Sputum from healthy male               2  None
297        BAA-3232                               Escherichia coli     562  ...                                               None               1  None
298        BAA-3237                               Escherichia coli     562  ...                                  Red clover sprout               2  None
299           23014                           Mycobacterium vaccae    1810  ...                                             Cattle               2  None
300           51798                             Campylobacter coli     195  ...  Terminal ileum of pig with proliferative enter...               2  None
```

### Outputing search results metadata as a table <a name="search_text_table"></a>
Example:
```
search_text_results=search_text(text="coli",output="json")
```
`search_text_results` is a list of dictionary objects. The first element `search_text_results[0]` is:
```
{"attributes": {
  "atcc_metadata": {
      "amr_intermediate": [],
      "amr_resistant": [],
      "amr_susceptible": [],
      "antibiotic_resistance": null,
      "antigenic_prop": null,
      "bsl": 2,
      "catalog_number": "35401",
      "drug_repository": null,
      "genotype": null,
      "gold": true,
      "isolation_new_web": "Feces",
      "notes": null,
      "other_metadata": {
        "catalog_details": {
          "ATCC_catalog_number": "ATCC 35401",
          "ATCC_lot_number": "57972906"
        },
        "genome_provider": {
          "annotatated_by": "ATCC",
          "annotations_date": "04/08/2024 13:35:34",
          "annotations_software": "PGAP",
          "asssembled_by": "One Codex",
          "asssembler_software": "Illumina + Oxford Nanopore Unicycler Hybrid Assembly",
          "asssembly_date": "06/17/19 18:38:25"
        },
        "genome_stats": {
          "filtered_contig_count": 6,
          "filtered_contig_length": 5393109,
          "number_of_n_bases": 0
        },
        "illumina_metadata": {
          "barcoding_kit": "Nextera XT Index Kit (96 Indexes 384 Samples)",
          "basecaller_model": "MiSeq Reporter Software",
          "basecaller_version": "2.6.2.3",
          "library_kit": "Nextera XT",
          "sequencer": "Illumina MiSeq"
        },
        "ont_metadata": {
          "barcoding_kit": "EXP-NBD103",
          "basecaller_model": "albacore",
          "basecaller_version": "2.3.4",
          "flowcell_type": "FLO-MIN106D",
          "library_kit": "SQK-LSK109",
          "sequencer": "Oxford Nanopore MinION"}
          }
    "id": "07905137c2314f3f",
    "visibility": "public"
  },
  "product_id": "35401",
  "product_url": "https://www.atcc.org/Products/All/35401",
  "taxon_id": "562",
  "taxon_name": "Escherichia coli"
}}

... "Shortened for cleanliness"

```
Specific values from each dictionary can be accessed as follows:
```
[(e['taxon_name'],e['attributes']['atcc_metadata']['catalog_number']) for e in search_text_results]
```
or

**DEFAULT MODE ID output**:
```
>>> search_text_results=search_text(text="coli") 
>>> 
```

Output:
```
['ATCC 35401:50cf24c55cc943c6', 'ATCC 700928:bad734779799489e', 'ATCC 27729:099e5acebc284d19', 'ATCC 8739:b9d91f150db449de', 'ATCC 23715:7df0c95fcc1f4b9a', 'ATCC 10536:996d977f03724ce6', 'ATCC 13706:c8c61b38f71249fe', 'ATCC 35218:92c302c2e2f34245', 'ATCC BAA-1061:82f4cdb84df547e8', 'ATCC BAA-2775:14440a65caf249d2', 'ATCC BAA-2776:8fbfddd1b7d54dea', 'ATCC BAA-2777:ca654a1656c9442e', 'ATCC BAA-2779:2dff3bccaa724f0b', 'ATCC BAA-2781:5c691565033045d5', 'ATCC 35638:0e56bc78536746d0', 'ATCC BAA-2774:d13a73ffd124484e', 'ATCC BAA-1429:a374dd646c7f42b2', 'ATCC BAA-1431:0a8241dfa0aa49b9', 'ATCC BAA-2523:0553bec8639740aa', ... ]
```
</details>
</details>



## download_assembly() <a name="download_assembly"></a>
**The download_assembly() function is the only function that can query and download the fasta assembly of an item on the ATCC Genome Portal.**  
This function takes an genome id as input to either download an assembly directly to a filepath, or store an assembly as a dictionary.

<details markdown="1">
<summary>Usage</summary>

```
  download_assembly() is function to download the fasta assemblies on the ATCC Genome Portal. The genomes files can be downloaded, or output directly to stdout.
  
  --------- USAGE ---------
  Required arguments:
    id = <str>
          An ATCC Genome ID (https://genomes.atcc.org/genome<genomeid>)          
  
  Optional arguments:
    output = <str>
          The API response format "output" [ (dict) | fasta ]
    download_dir = [Path <str>]
          A directory to download the fasta file toThe fasta file will be named automatically.
    api_key = <str> 
          Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] 
  
  EXAMPLES:
    > download_assembly(id='assemblyid', output='fasta', download_dir="/directory/for/download/") downloads an assembly file to provided path
    > download_assembly(id='assemblyid', output='dict') return a dictionary othe assembly. Key=Header : Value=Seq.
```

<details>
<summary>Advanced</summary>

### Download fasta file example: <a name="download_assembly_fasta_file"></a>
```
download_assembly(id='8df308b788704bed',output='fasta',download_dir="/path/to/folder")
```
This will download the fasta file directly to the folder provided for the "download_assembly_path" argument

### Download assembly as a dictionary example: <a name="download_assembly_as_a_dictionary"></a>
```
assembly=download_assembly(id='8df308b788704bed',output="dict")
for contig in assembly:
  print(contig)
  print(assembly[contig][0:200])
```
`assembly` is a dictionary where each key is the contig header and each value is the contig sequence. The output from above (200 bases extended from each contig):
```
>128666ac42774942_1 assembly_id="128666ac42774942" genome_id="8df308b788704bed" atcc_catalog_number="ATCC BAA-2481" species="Liberibacter crescens" contig_number="1" topology="circular"
TTTTTCCTTCTGCTCATGTCTATTTTATGGAAAATAAAGGTCGTGATATAAAGCCTTTTTTGACTTTGCTTGAATCTGGGAAACTCGATCAGTATGATTATATTTGCAAGATTCATGGCAAGGAGTCGAGACATCAAAAGCGTTCTCCGATTGAAGGAACCTTATGGAGACGTTGGTTATTTTATGATCTTCTTGGAGCA
```

</details></details>

## download_annotations() <a name="download_annotations"></a>
**`download_annotations()` is the only function that can query and download the annotations of an item on the ATCC Genome Portal via GenBank format.**  
Similar to `download_assembly()`, an assembly id is required for the `download_annotations()`, which can be used to obtain the annotations to stdOUT or save as a file directly. The annotations are in .gbk filetype.

<details markdown="1">
<summary>Usage</summary>

```
  download_annotations() is a function to download the fasta assemblies on the ATCC Genome Portal. 
  The annotation files can be downloaded, or output directly to stdout.
  
  -------- USAGE ---------
  Required arguments:
    id = <str>
          An ATCC Genome ID (https://genomes.atcc.org/genomes/<genomeid>)          
  
  Optional arguments:
    output = <str> 
          The API response format "output" [ (dict) | gbk ]
    download_dir = [Path <str>] 
          A directory to download the GenBank files to. The file will be named automatically.
    api_key = <str> 
          Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \      
  
  EXAMPLES:
    > download_annotations(id='genomeid', output='gbk', download_dir='/directory/for/download/') downloads a GenBank file to provided path
    > download_annotations(id='genomeid', output='dict') return the raw genbank file
```

<details>
<summary>Advanced</summary>

### Download annotations to a GenBank file example:  <a name="download_annotations_to_file"></a>
```
>>> download_annotations(id='8df308b788704bed', output="gbk", download_dir="/path/to/folder")

% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 3537k  100 3537k    0     0  5733k      0 --:--:-- --:--:-- --:--:-- 5724k
SUCCESS! File: /path/to/folder/Liberibacter_crescens_ATCC_BAA_2481.gbk now exists!

```
The above will directly download a GenBank file to your provided path.

### Download annotations output directly example:  <a name="download_annotations_raw_ouput"></a>
```
annotations=download_annotations(id='8df308b788704bed',output='dict')
for line in annotations.split("\n"):
  print(line)
```
The output from the above code block prints each link of the .gbk file.
```
LOCUS       assembly_128666ac42774942_1 1513871 bp    DNA     circular BCT 30-APR-2024
DEFINITION  Liberibacter crescens ATCC® BAA-2481™, contig 1.
ACCESSION   assembly_128666ac42774942_1
VERSION     assembly_128666ac42774942_1
DBLINK      assembly: 128666ac42774942
            annotation_set: a000cf31c34f4e43
            genome: 8df308b788704bed
KEYWORDS    .
SOURCE      https://genomes.atcc.org/genomes/8df308b788704bed
  ORGANISM  Liberibacter crescens
            cellular organisms; Bacteria; Pseudomonadota; Alphaproteobacteria;
            Hyphomicrobiales; Rhizobiaceae; Liberibacter; Liberibacter crescens.
COMMENT     ##Genome-Annotation-Data-START##
            Annotation Provider :: ATCC Sequencing & Bioinformatics Center
            Annotation Date                   :: 04/29/2024 16:44:51
            Annotation Pipeline :: NCBI Prokaryotic Genome Annotation Pipeline
            (PGAP)
            Annotation Method :: Best-placed reference protein set; GeneMarkS-2+
            Annotation Software revision      :: 2022-12-13.build6494
            ATCC Item Catalog                 :: ATCC BAA-2481
            ATCC Item Lot Number              :: 70048410
            ATCC Item Name                    :: Liberibacter crescens
            ATCC Collection                   :: Bacteriology
            Features Annotated                :: Gene; CDS; rRNA; tRNA; ncRNA
            Genes (total)                     :: 1,386
            CDSs (total)                      :: 1,327
            Genes (coding)                    :: 1,305
            CDSs (with protein)               :: 1,305
            Genes (RNA)                       :: 59
            rRNAs                             :: 3, 3, 3 (5S, 16S, 23S)
            complete rRNAs                    :: 3, 3, 3 (5S, 16S, 23S)
            tRNAs                             :: 46
            ncRNAs                            :: 4
            Pseudo Genes (total)              :: 22
            CDSs (without protein)            :: 22
            Pseudo Genes (ambiguous residues) :: 0 of 22
            Pseudo Genes (frameshifted)       :: 3 of 22
            Pseudo Genes (incomplete)         :: 19 of 22
            Pseudo Genes (internal stop)      :: 3 of 22
            Pseudo Genes (multiple problems)  :: 2 of 22
            ##Genome-Annotation-Data-END##
            The annotation was added by the assembly submitters using the NCBI
            Prokaryotic Genome Annotation Pipeline (PGAP). Information about
            stand-alone PGAP can be found here: https://github.com/ncbi/pgap/
FEATURES             Location/Qualifiers
     source          1..1513871
                     /organism="Liberibacter crescens"
                     /mol_type="genomic DNA"
                     /strain="BAA-2481"
                     /db_xref="taxon:1273132"
     gene            join(1513283..1513871,1..587)
                     /locus_tag="pgap_annot_000001"
     CDS             join(1513283..1513871,1..587)
                     /locus_tag="pgap_annot_000001"
                     /inference="COORDINATES: ab initio prediction:GeneMarkS-2+"
                     /note="Derived by automated computational analysis using
                     gene prediction method: GeneMarkS-2+."
                     /codon_start=1
                     /transl_table=11
                     /product="hypothetical protein"
                     /protein_id="extdb:pgap_annot_000001"
   ...
   ...
   ... "Intentionally Shortened for Readability"
```

</details></details>

## download_metadata() <a name="download_metadata"></a>
**`download_metadata()` is a function to download the full metadata of a genome on the portal.**  
This function be used to obtain the detailed metadata including qc statistics, contig length(s), etc. for a specific genome id.

<details markdown="1">
<summary>Usage</summary>

```
download_metadata() is a function intended to download the JSON metadata behind each assembly on the portal.
The metadata can be output as a dictionary, or as an informative table with the correct fields already formatted.\n
      
--------- USAGE ---------
Required arguments:
  id = <str>
        An ATCC Genome ID (https://genomes.atcc.org/genomes/<genomeid>) \n     
      
Optional arguments:
  output = <str>
        The API response format "output" [ (dict) | table ]
  api_key = <str>
        Your Genome Portal APIKey [(global_api_key) | overwrite if provided ]
```
<details>
<summary>Advanced</summary>

### Download metadata example <a name="download_metadata_as_dict"></a>
The detailed metadata can be downloaded as follows:
```
>>> assembly_metadata = download_metadata(id='8df308b788704bed')
>>> assembly_metadata
```
`assembly_metadata` is a dictionary:
```
{"attributes": {
    "atcc_metadata": {
      "amr_intermediate": [],
      "amr_resistant": [],
      "amr_susceptible": [],
      "antigenic_prop": null,
      "bsl": 1,
      "catalog_number": "BAA-2481",
      "genotype": null,
      "gold": true,
      "isolation_new_web": "Cultivated mountain papaya (Babaco)",
      "notes": null,
      "other_metadata": {
        "catalog_details": {
          "ATCC_catalog_number": "ATCC BAA-2481",
          "ATCC_lot_number": "70048410"
        },
        "genome_provider": {
          "annotatated_by": "ATCC",
          "annotations_date": "04/29/2024 16:44:51",
          "annotations_software": "PGAP",
          "asssembled_by": "One Codex",
          "asssembler_software": "Illumina + Oxford Nanopore Unicycler Hybrid Assembly",
          "asssembly_date": "08/12/23 12:35:01"
        },
        "genome_stats": {
          "filtered_contig_count": 1,
          "filtered_contig_length": 1513871,
          "number_of_n_bases": 0
        },
        "illumina_metadata": {
          "barcoding_kit": "IDTIlmnDNARNAUDISetATagmentation",
          "basecaller_model": "NextSeq 1000/2000 Control Software",
          "basecaller_version": "1.5.0.42699",
          "library_kit": "IlluminaDNAPrep",
          "sequencer": "Illumina NextSeq"
        },
        "ont_metadata": {
          "barcoding_kit": "EXP-NBD196",
          "basecaller_model": "HAC",
          "basecaller_version": "6.4.6+ae70e8f",
          "flowcell_type": "FLO-MIN106",
          "library_kit": "SQK-LSK109",
          "sequencer": "Oxford Nanopore GridION X5"
   ...
   "Intentionally Shortened For Example"
   ...
```
</details></details>

## download_all_genomes() <a name="download_all_genomes"></a>
**`download_all_genomes()` is a function that allows the user to download all genomic JSON metadata available on https://genomes.atcc.org**.  
**If you are using functions like `deep_search()`, this is not needed to run manually.**  

This can be ran without prior knowledge of any associated metadata.  

**This function defaults to storing all genomes to the variable `global_genome_metadata` as well as piping to stdOUT for variable storage**

<details markdown="1">
<summary>Usage</summary>

```
  download_all_genomes() is a function intended to download the JSON metadata for ALL ATCC genomes currently available on the ATCC Genome Portal.
  This function will store the results as the variable "global_genome_metadata", and will also report to stdOUT.

  --------- USAGE ---------
  Required arguments: NONE
      
  Optional arguments:
    api_key = <str>
          Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \n

  EXAMPLES:
    > download_all_genomes() downloads all genomes as a list of JSON dictionaries to the variable "global_genome_metadata".
    > secondary_var=download_all_genomes() downloads all genomes as a list of JSON dictionaries to the variable "global_genome_metadata" AND "secondary_var".
```

<details>
<summary>Advanced</summary>

### Download all genome entries as list example: <a name="download_all_genomes_to_list"></a>
Running the below code will generate a list of every genome's metadata. Because the output was assigned to a variable, it will store as the assigned variable here `genomes` as well as `global_genome_metadata` by default.
```
genomes=download_all_genomes()
```
This will output a stored variable `genomes`. This object is a list of dictionaries representing all genomes available in the portal. This will also print a message about the collection:

> Fetched 4,750 genomes  
> genomes visibility='public': 4,750

This list can then be leveraged into `download_assembly` or `download_annotations` in order to download each item to file. Each genome's ID can be found in the "id" keys of each dictionary:

```
>>> genomes[0]['id']
'21846cfe916b4f18'
```
### Change the index to "genomeID": <a name="convert_to_genomeid"></a>
Alternatively, you can create a secondary list of these genomes, now indexed by genomeid:
```
>>> genomes_named=convert_to_genomeid(list=genomes)
>>> genomes_named['21846cfe916b4f18']['id']
  '21846cfe916b4f18'

```

</details></details>



## deep_search() <a name="deep_search"></a>
`deep_search()` allows the user to search for a term in a list of genome JSON metadata. The function searches through every key and value in the metadata nested dictionary. By default, it runs in 'text' mode, where the term is searched within the entire JSON as a string. 'json' mode enables full text matching as either a key or dict value. 

This function also supports fuzzy matching with the search term. By adding `fuzzy=value` to the command, the 'value' becomes the fuzzy token ratio value.

To use this function, you must have downloaded all genomic metadata using `download_all_genomes()` or must assign your personal list to the variable `global_genome_metadata`.

<details markdown="1">
<summary>Usage</summary>

```
deep_search() is intended for deep searching of ATCC JSON metadata behind each genome.
THIS FUNCTION SUPPORTS EXACT KEY|VALUE|STRING MATCHING, WITH "text" METHOD CAPTURE SUBSTRINGS.
There is currently no similar function on the ATCC Genome Portal.
This function will search through the JSON metadata of all available genomes for matching strings orv alues.

--------- USAGE ---------
Required arguments:
  text = <str>
        any text field caputured within the JSON of the portal.
  -- a list of genomes (Globally set variable "global_genome_metadata")      

Optional arguments:
  fuzz_on = <str>
        If provided with a value, enables fuzzy matching  [(75) | value 0-100]
  output = <str>
        The API response format "output" [(id) | json | table]
  mode = <str>
        Choice to search based on a dictionary structure or just raw text [(text)json]
  api_key = <str>
        Your Genome Portal APIKey [Globally set "global_api_key"orentered"api_key"]
  STORE global_genome_metadata
        A list of genomes can be set as "global_genome_metadata"variable. Not needed as an argument (Globally setvariable"global_genome_metadata")

EXAMPLES:
  > deep_search(text="PGAP") will return a list of genomeIDs that had "PGAP" somewhere in the JSON
  > deep_search(text="Lake", output="id") return resulting assembly IDs that contain "Lake"inthemetadata
  > deep_search(text="Lake", output="id", fuzz_on='75') Same as above, but with a fuzzy score to lake
  > deep_search(mode='json',text="Lake", output="table") Same as above, but with a manually entered API Key and output as an informational table.
  > deep_search(api_key="<apikey>",text="Lake",output="table",fuzzy='75') Same as above, but now fuzzy match to '75'
```
<details>
<summary>Advanced</summary>

### Fuzzy search for an incorrect spelling! <a name="deep_search_fuzzy"></a>
For example, searching for the term "yursinia" (a misspelling of yersinia) works as follows:
```
match_list=deep_search(text="yursinia",fuzz_on='50',output='json')
[e['taxon_name'] for e in match_list]
```
`match_list` is a list of dictionaries. The taxon_name for each element output from the above code:
```
['Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia pestis', 'Yersinia ruckeri', 'Yersinia pestis', 'Human rhinovirus 35', 'Phytobacter ursingii', 'Yersinia rohdei', 'Yersinia aldovae', 'Yersinia rohdei', 'Yersinia rohdei', 'Yersinia rohdei', 'Yersinia aldovae', 'Yersinia ruckeri', 'Bovine respiratory syncytial virus', 'Yersinia aldovae', 'Yersinia aldovae', 'Yersinia rohdei', 'Phytobacter ursingii', 'Yersinia sp.', ... ]
```

### Fuzzy search for a BSL level! <a name="deep_search_fuzzy_contig"></a>
Example:
```
>>> search_results = deep_search(text="'bsl': 2",output='table')
```
Which returns a tabular output of all genomes that have this metadata!:

```
>>> search_results
     atcc_product_id                               name  taxid  ...                                  isolation_new_web biosafety_level notes
0             700824                Helicobacter pylori    210  ...                      Patient with a duodenal ulcer               2  None
1             700294             Streptococcus pyogenes   1314  ...                                     Infected wound               2  None
2              19606            Acinetobacter baumannii    470  ...                                              Urine               2  None
3           BAA-1605            Acinetobacter baumannii    470  ...  Sputum of military personnel returning from Af...               2  None
4              49882                Bartonella henselae  38323  ...                         Blood of HIV-positive male               2  None
...              ...                                ...    ...  ...                                                ...             ...   ...
2623          VR-240                  Human echovirus 6  12062  ...                     Child with aseptic meningitis.               2  None
2624           VR-47                 Human echovirus 17  47505  ...                    Rectal swab from healthy child.               2  None
2625          VR-583  Human Coxsackievirus A 24 variant  12089  ...                Isolated from infant with diarrhea.               2  None
2626          VR-645           Adeno-associated virus 1  85106  ...         Pool of RhMk TC infected with SV-15 virus.               2  None
2627          VR-692                 Human echovirus 30  41846  ...                                               None               2  None

[2628 rows x 44 columns]
```

</details></details>

## tabulate() <a name="tabulate"></a>
**`tabulate()` is a function that is intended to reformat your list of genome metadata into a table.**  

This function allows the user to input a genome metadata list, and return a formatted dataframe that has pre-converted the JSON values into important columns.
<details markdown="1">
<summary>Usage</summary>

```
tabulate() is a helper function used to convert a list of JSON-formatted metadata into a dataframe.
This function then calls on "format_qc()" to pull relevant metadata fields as dedicated columns. 

--------- USAGE ---------
Required arguments:
  genome_list = [list]
        This is not a kwarg, and is just the object of the function to be called. You must pass a list of genomic metadata.
```
<details>
<summary>Advanced</summary>

### Convert any list of genomes to a table <a name="tabulate_example"></a>
Example:
```
>>> global_genome_metadata_table = tabulate(global_genome_metadata) # Covert the global list of all genomes into a table
```
By providing a list of genomes, `tabulate()` will then convert the inputed listed to stdOUT. Redirecting to `global_genome_metadata_table` provides the following output.

```
>>> global_genome_metadata_table
     atcc_product_id                               name    taxid  ...                                  isolation_new_web biosafety_level notes
0             700824                Helicobacter pylori      210  ...                      Patient with a duodenal ulcer             2.0  None
1               4357          Lactobacillus acidophilus     1579  ...                                               None             1.0  None
2             700294             Streptococcus pyogenes     1314  ...                                     Infected wound             2.0  None
3             700610               Streptococcus mutans     1309  ...                           Child with active caries             1.0  None
4              19606            Acinetobacter baumannii      470  ...                                              Urine             2.0  None
...              ...                                ...      ...  ...                                                ...             ...   ...
4885          VR-583  Human Coxsackievirus A 24 variant    12089  ...                Isolated from infant with diarrhea.             2.0  None
4886          VR-645           Adeno-associated virus 1    85106  ...         Pool of RhMk TC infected with SV-15 virus.             2.0  None
4887          VR-692                 Human echovirus 30    41846  ...                                               None             2.0  None
4888           VR-74        Japanese encephalitis virus    11072  ...  Spinal fluid from a fatally infected 6-year-ol...             3.0  None
4889         TSD-366           Methanoglobus nevadensis  1872626  ...  Hot springs by Gerlach, Nevada (N40° 39.684′ W...             1.0  None

[4890 rows x 44 columns]
```

# Cookbook <a name="cookbook"></a>

<details>
<summary>Click to view cookbook</summary>

## Download all the data for all *E. coli* assemblies <a name="ex1"></a>
First, we search for all Escherichia coli using `search_text()`. Then we iterate through the results list, create a dictionary entry for each assembly, and then download and store the assembly, annotations, and metadata. The first 3 assemblies are downloaded below.
```
search_text_results=search_text(text="Escherichia coli",output='json')
e_coli_data = {}
# Download assembly, annotations, and metadata for first 5 
for e in search_text_results[:3]:
  id = e['id']
  e_coli_data[id] = {}
  e_coli_data[id]["assembly"] = download_assembly(id=e['id'],output='dict')
  e_coli_data[id]["annotations"] = download_annotations(id=e['id'],output='dict')
  e_coli_data[id]["metadata"] = download_metadata(id=e['id'])
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
>>> for id in e_coli_data.keys():
...   print("First 150 nts of each contig")
...   for contig in e_coli_data[id]["assembly"].keys():
...     print(contig)
...     print(e_coli_data[id]["assembly"][contig][0:150])
...   print("\nFirst 10 lines of the annotation data:")
...   for line in e_coli_data[id]["annotations"].split("\n")[:10]:
...     print(line)
...   print("\nSome example metadata:")
...   print("contig_lengths:",e_coli_data[id]["metadata"]["primary_assembly"]["attributes"]["contig_lengths"])
...   print("checkm_results:",e_coli_data[id]["metadata"]["primary_assembly"]["attributes"]["qc_statistics"]["checkm_results"])
...   break
... 
First 150 nts of each contig
>07905137c2314f3f_1 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="1" topology="circular"
GTGTCACTTTCGCTTTGGCAGCAGTGTCTTGCCCGATTGCAGGATGAGTTACCAGCCACAGAATTCAGTATGTGGATACGCCCATTGCAGGCGGAACTGAGCGATAACACGCTGGCCCTGTACGCGCCAAACCGTTTTGTCCTCGATTGG
>07905137c2314f3f_2 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="2" topology="circular"
GTGACTGATCTTCAACAAACGTATTACCGCCAGGTAAAGAACCCGAATCCGGTGTTTACACCCCGTGAAGGTGCCGGAACGCTGAAGTTCTGCGAAAAACTGATGGAAAAGGCGGTGGGCTTCACTTCTCGTTTTGATTTCGCCATTCAT
>07905137c2314f3f_3 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="3" topology="circular"
GTGACTGATCTTCAACAAACGTATTACCGCCAGGTAAAGAACCCGAATCCGGTGTTTACACCCCGTAAAGGTGCCGGAACGCTGAAGTTCTGCGAAAAACTGATGGAAAAGGCGGTGGGCTTCACTTCCCGTTTTGATTTCGCCATTCAT
>07905137c2314f3f_4 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="4" topology="circular"
GTGACTGATCTTCAACAAACGTATTACCGCCAGGTAAAGAACCCGAATCCGGTGTTTACACCCCGTAAAGGTGCCGGAACGCTGAAGTTCTGCGAAAAACTGATGGAAAAGGCGGTGGGCTTCACTTCCCGTTTTGATTTCGCCATTCAT
>07905137c2314f3f_5 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="5" topology="circular"
TTCCTCAGGGATGAAAAAGGTAATATACATTGAACCTTTTGATAAAAGCTTAGCTTTAGATTTACATGACGATGCAATAACCACCACAGAAGACCCGTCGAGAGTTATTTTCTCGAAATTTGAGGGTGTTGCACCAAGAAGATACAATAA
>07905137c2314f3f_6 assembly_id="07905137c2314f3f" genome_id="50cf24c55cc943c6" atcc_catalog_number="ATCC 35401" species="Escherichia coli" contig_number="6" topology="circular"
ATCTATGCTGAGCGGGAAGGTAATGGGTTGCTTGTGAGAGTAGATCTGAGAACGTGCTATCTGAATCCAGGTCAAGCTGAAATGTTTAATATAGCTATTGGATATACGCGTTCAGTTCACGGGAATCATCTATAAGCTGTCTACAAAAAG

First 10 lines of the annotation data:
LOCUS       assembly_07905137c2314f3f_1 5152467 bp    DNA     circular BCT 17-APR-2024
DEFINITION  Escherichia coli ATCC® 35401™, contig 1.
ACCESSION   assembly_07905137c2314f3f_1
VERSION     assembly_07905137c2314f3f_1
DBLINK      assembly: 07905137c2314f3f
            annotation_set: 7966cc374f2a4a3a
            genome: 50cf24c55cc943c6
KEYWORDS    .
SOURCE      https://genomes.atcc.org/genomes/50cf24c55cc943c6
  ORGANISM  Escherichia coli

Some example metadata:
contig_lengths: [5152467.0, 94797.0, 67898.0, 66609.0, 5800.0, 5538.0]
checkm_results: {'completeness': 99.96693121693121, 'contamination': 0.4836309523809524}
```
## Download all the data for products with BSL 2 designations, with the most antibiotic resistance <a name="ex_bsl"></a>

First, we will have to set up a good string to search on for deep_search()

```
## This search works because we explicitly quote the key and value for "bsl".
bsl_hits=deep_search(text="'bsl': 2", output='table')

## Now we have a table called "bsl_hits".
## Lets sort some ABX columns and pull the top 5
bsl_hits = bsl_hits.sort_values(by='amr_resistant')[0:5]

```
Output:

```
>>> bsl_hits_sorted = bsl_hits.sort_values(by='amr_resistant')[0:5]
    atcc_product_id                    name taxid         genome_id       assembly_id         collection  ...  antigenic_prop  drug_repository  genotype  isolation_new_web biosafety_level notes
768        BAA-2114  Pseudomonas aeruginosa   287  a86969582da540ab  09ad0c9c1cc1487e  ATCC Bacteriology  ...            None              NaN      None      Sputum sample               2  None
108        BAA-2790   Klebsiella pneumoniae   573  e995244fd8584d55  0f8527a3328b4cf6  ATCC Bacteriology  ...            None              NaN      None              Wound               2  None
269        BAA-2783   Klebsiella pneumoniae   573  bdb0cfd03b5a4757  1f13c918db214992  ATCC Bacteriology  ...            None              NaN      None        Large colon               2  None
276        BAA-2808            Serratia sp.   616  c2d57b369fcd41b0  ed513ca825f9484e  ATCC Bacteriology  ...            None              NaN      None              Urine               2  None
271        BAA-2791       Proteus mirabilis   584  8ff2f99c4c264aed  ed57a07c1158434c  ATCC Bacteriology  ...            None              NaN      None              Urine               2  None

[5 rows x 44 columns]
```
Now, lets download these genbanks and annotations for each of the top 5 most ABX resistant BSL-2 items:

```
for i, row in bsl_hits_sorted.iterrows():
  download_assembly(id=row['genome_id'], output='fasta',download_dir='/home/jpetrone_atcc.org')
  download_annotations(id=row['genome_id'], output='gbk',download_dir='/home/jpetrone_atcc.org')
```
Output:

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   388    0   388    0     0   4172      0 --:--:-- --:--:-- --:--:--  4217
SUCCESS! File: /test/download_dir/Pseudomonas_aeruginosa_ATCC_BAA_2114.fasta now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14.2M  100 14.2M    0     0  47.7M      0 --:--:-- --:--:-- --:--:-- 47.8M
SUCCESS! File: /test/download_dir/Pseudomonas_aeruginosa_ATCC_BAA_2114.gbk now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   387    0   387    0     0   5528      0 --:--:-- --:--:-- --:--:--  5528
SUCCESS! File: /test/download_dir/Klebsiella_pneumoniae_ATCC_BAA_2790.fasta now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 13.5M  100 13.5M    0     0  45.9M      0 --:--:-- --:--:-- --:--:-- 46.1M
SUCCESS! File: /test/download_dir/Klebsiella_pneumoniae_ATCC_BAA_2790.gbk now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   387    0   387    0     0   5229      0 --:--:-- --:--:-- --:--:--  5301
SUCCESS! File: /test/download_dir/Klebsiella_pneumoniae_ATCC_BAA_2783.fasta now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14.0M  100 14.0M    0     0  55.1M      0 --:--:-- --:--:-- --:--:-- 55.1M
SUCCESS! File: /test/download_dir/Klebsiella_pneumoniae_ATCC_BAA_2783.gbk now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   377    0   377    0     0   4333      0 --:--:-- --:--:-- --:--:--  4333
SUCCESS! File: /test/download_dir/Serratia_sp_ATCC_BAA_2808.fasta now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 13.2M  100 13.2M    0     0  38.4M      0 --:--:-- --:--:-- --:--:-- 38.4M
SUCCESS! File: /test/download_dir/Serratia_sp_ATCC_BAA_2808.gbk now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   383    0   383    0     0   5471      0 --:--:-- --:--:-- --:--:--  5471
SUCCESS! File: /test/download_dir/Proteus_mirabilis_ATCC_BAA_2791.fasta now exists!
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 10.0M  100 10.0M    0     0  51.1M      0 --:--:-- --:--:-- --:--:-- 51.4M
SUCCESS! File: /test/download_dir/Proteus_mirabilis_ATCC_BAA_2791.gbk now exists!
```

## Download all the data for product 700822, in the new table format <a name="ex2"></a>
First, we use `search_product` to download the assembly metadata from which we pull out the assembly id. Then, we download the assembly, annotations, and metadata.
```
>>> search_products_results=search_product(product_id="700822",output='table')
>>> id = search_products_results.loc[0,'genome_id']
>>> assembly=download_assembly(id=id,output='dict')
>>> annotations=download_annotations(id=id,output='dict')
>>> metadata=download_metadata(id=id)
```
```
print("First 150 nts of each contig")
for contig in assembly.keys():
  print(contig)
  print(assembly[contig][0:150])
print("First 10 lines of the annotation data:")
for line in annotations.split("\n")[:10]:
  print(line)

print('Some example metadata:')
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
First, we use `deep_search` to download the assembly metadata for all items that fuzzy match "yersinia." Then, we pull out the assembly id for each and download the assembly, annotations, and metadata.
```
match_list=deep_search(text="yersinia",fuzz_on='50',output='json')
yersinia_data = {}
for e in match_list[:3]:
  id = e['id']
  yersinia_data[id] = {}
  yersinia_data[id]["assembly"] = download_assembly(id=id,output='dict')
  yersinia_data[id]["annotations"] = download_annotations(id=id,output='dict')
  yersinia_data[id]["metadata"] = download_metadata(id=id)
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