# Introduction
This is a set of python scripts that can be used to access the One Codex api. All scripts were created using Python version 3.8. Scripts have been tested in Google Colab (link to notebook available at bottom of README) using Python 3.7. See the demo python notebook for detailed examples.
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
