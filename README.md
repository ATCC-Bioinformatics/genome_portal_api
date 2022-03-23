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
### search_product()
The search_product() function is similar to the search_text() function, except it looks for assembly metadata that matches a particular product id. The product id used must be an exact match to return correct results.
### download_assembly()
The download_assembly() function uses an assembly id to either obtain the link to download an assembly, or download an assembly directly. Here, the assembly id contained in the search_product_assembly_id variable is used to retrieve the assembly download link which can be copied and pasted into any web browser: The first 200 nucleoties of each contig in the assemblies relating to the assembly ids in search_product_assembly_id variable are shown below. If neither the download_link_only or download_assembly options are set to True, the raw json result is returned.
### download_annotations()
Similarly to download_assembly, an assembly id is required to be able to download assembly annotations, and it is possible to download only the annotations link rather than the full annotation. Using the assembly ids from search_product_results_assembly_id the download links are retrieved. Annotations are downloaded directly as a GenBank file.
### download_metadata()
In order to download an assembly's metadata using an assembly id when other options are not needed, i.e. links, GenBank files, etc, download_metadata() should be used. download_metadata() produces the detailed metadata for any given assembly id.
### download_all_genomes()
download_all_genomes() allows the user to download all genomes available on https://genomes.atcc.org without prior knowledge of any associated metadata.
### download_catalogue()
download_catalogue() allows the user to download the entire catalogue available on https://genomes.atcc.org and either return a list of all assembly options or save the list to a pkl file. The complete catalogue can be returned from the function as a list by not including an output path. The complete catalogue can be saved to a .pkl file by including an output path. This is required to run the search_fuzzy() function.
### search_fuzzy()
search_fuzzy() allows the user to search for a term using fuzzy matching. To use this function, you must have downloaded the complete catalogue using download_catalogue(jwt=jwt,output="path/to/catalogue.pkl") because the catalogue path is a required argument.
