# Introduction 
This is a set of python scripts that can be used to access the One Codex api.

# Getting Started
1. You will need a One Codex account at https://genomes.atcc.org/ to obtain a JWT. This is required for all scripts.
2. You need python

# Cookbook
## Examine metadata for all genomes 
You must include a page number argument
`python oc_api.py -m all_genomes -j your_JWT --page_number 12`
## Search for genomes using a product ID or search term
You must include a product ID or search term
<br>Product ID:
`python oc_api.py -m all_genomes -j your_JWT -p 35638`
<br>Search term:
`python oc_api.py -m all_genomes -j your_JWT -t pseudomonas`
<br>Return only the genome ID(s) for your search
`python oc_api.py -m all_genomes -j your_JWT -p 35638 --id_only`
## Download a specific genome's metadata
You must include a genome id, e.g., 304fd1fb9a4e48ee.
<br>Print out metadata:
`python oc_api.py -m download_metadata -j your_JWT -i 304fd1fb9a4e48ee`
## Download a specific genome assembly
You must include a genome id, e.g., 304fd1fb9a4e48ee.
<br>Print out raw results:
`python oc_api.py -m download_assembly -j your_JWT -i 304fd1fb9a4e48ee`
<br>Print out download url only:
`python oc_api.py -m download_assembly -j your_JWT -i 304fd1fb9a4e48ee --download_link_only`
<br>Print out assembly:
`python oc_api.py -m download_assembly -j your_JWT -i 304fd1fb9a4e48ee --print_out_results`
## Download a specific genome's annotations:
You must include a genome id, e.g., 304fd1fb9a4e48ee.
<br>Print out raw results:
`python oc_api.py -m download_annotations -j your_JWT -i 304fd1fb9a4e48ee`
<br>Print out download url only:
`python oc_api.py -m download_annotations -j your_JWT -i 304fd1fb9a4e48ee --download_link_only`
<br>Print out annotations:
`python oc_api.py -m download_annotations -j your_JWT -i 304fd1fb9a4e48ee --print_out_results`