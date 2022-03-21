# Introduction
This is a set of python scripts that can be used to access the One Codex api.
# Getting Started
*   You will need a One Codex account at https://genomes.atcc.org/ to obtain a JWT. This is required for all scripts.
    * Log in or create an account on https://genomes.atcc.org
    ![<img align="left" width="500" src="images/login.png"/>](images/login.png)

    * Hover over your username on the home page of https://genomes.atcc.org, and select “Profile” from the list that drops down

    <!-- <img align="left" width="500" src="images/profile.png"> -->
    ![<img align="left" width="500" src="images/profile.png"/>](images/profile.png)

    * Click on “Copy JWT” - lasts for 15 minutes before time out.

    <!-- <img align="left" width="500" src="images/copyjwt.png"> -->
    ![<img align="left" width="500" src="images/copyjwt.png"/>](images/copyjwt.png)


*   You need python
## Pip install
```
python -m venv env
source env/bin/activate
git clone https://github.com/ATCC-Bioinformatics/genome_portal_api.git
pip install /path/to/genome_portal_api
```
See the demo python notebook for detailed examples.
