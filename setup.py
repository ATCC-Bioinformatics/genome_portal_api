from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="genome_portal_api",
    version="1.1.1",
    description="Python package to access and download"
    "data from ATCC's Genome Portal",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/ATCC-Bioinformatics",
    author="Sequencing and Bioinformatics Center",
    author_email="SBC@AtccCloud.onmicrosoft.com",
    keywords="core package",
    license="https://www.atcc.org/policies/product-use-policies/data-use-agreement",
    packages=["genome_portal_api"],
    install_requires=["fuzzywuzzy>=0.18.0","python-Levenshtein>=0.12.2", "requests>=2.31.0", "argparse>=1.1", 'pandas>=2.0.3'],
    include_package_data=True,

)
