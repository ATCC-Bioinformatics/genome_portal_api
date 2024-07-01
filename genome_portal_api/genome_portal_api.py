import os
import argparse
from argparse import RawTextHelpFormatter
import json
import time
import pickle as pkl
from fuzzywuzzy import fuzz
import logging
import requests
import glob
from typing import Any, Dict, Generator, List, Optional
from collections import Counter
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)


logger.addHandler(stream_handler)

class emptyResultsError(Exception):
  def __init__(self, message):
    self.message = message


def set_global_api(apikey=None): #! Intended to 
  """
    Sets the global API key variable by checking environment variables and function input.
    :param api_key: User-provided API key (optional)
  """
  global global_api_key
  ## Check to see if set as enviornment variable
  if "ATCC_GENOME_PORTAL_API_KEY" in os.environ:
    global_api_key = os.environ["ATCC_GENOME_PORTAL_API_KEY"]
    logger.info(f"API key has been found: {global_api_key}")
    return
  ## Check to see if was provided as input to this function
  if apikey:
    global_api_key = apikey
    logger.info(f"API key is now set: {global_api_key}. Please export this api_key under the variable 'ATCC_GENOME_PORTAL_API_KEY'!")
    return
  # If still no API key, prompt the user to input one
  while True:
    user_input = input("Please enter the API key: ")
    if user_input:
      global_api_key = user_input
      logger.info(f"Using user-provided API key: {global_api_key}")
      break
    else:
      print("API key cannot be empty. Please try again.")




def load_all_metadata(genome_list=None):
  """
    Stores a global variable for the JSONs of all metadata
  """
  global global_genome_metadata
  ## Check to see if set as enviornment variable
  if not global_genome_metadata:
    global_genome_metadata=download_all_genomes()
    logger.info(f"All genome have been stored under the variable 'global_genome_metadata' ")
  else:
    logger.info(f"All genome have been already been stored under the variable 'global_genome_metadata' ")
    logger.info(f"If this is an error or you want to requery the genome, please run download_all_genomes()")



def json_search(nested_dict, term): #! Intended to iteratively search JSON key:value schema in genome metadata
  def recursive_search(d, term):
    try:
      for key, value in d.items():
        if key == term or value == term:
          return True
        elif isinstance(value, dict):
          # Recursively search nested dictionaries
          if recursive_search(value, term):
            return True
      return False
    except AttributeError:
      return False  
  return recursive_search(nested_dict, term)
    
    



def search_product(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
    if global_api_key:
      if str(apikey) != str(global_api_key):
        apikey = global_api_key 
  else:
      apikey = global_api_key if global_api_key else set_global_api()
  id_only = kwargs['id_only'] if 'id_only' in kwargs else True
  if 'product_id' in kwargs:
    product_id = kwargs['product_id']
  else:
    print("""
      search_product() is intended for EXACT matching of ATCC product numbers. 
      This mimics the function of using the search bar on the ATCC Genome Portal set to CATALOG NUMBER

      USAGE:
      Required:
      -- (product_id="<product_id">) an ATCC product_id
      -- your api_key (Globally set variable "global_api_key" or entered "api_key")
      
      Options:
      -- boolean id_only flag
      ---- DEFAULT: 'id_only' boolean is set to True; set it to 'False' to return metadata tpo.
      
      E.g., search_product(product_id='35638') return resulting Genome ID for ATCC 35638
      E.g., search_product(product_id='35638',id_only=False) return resulting metadata for ATCC 35638
      E.g., x = search_product(api_key=YOUR_API_KEY,product_id='35638',id_only=False) Same as above, but with a manually entered API Key
    """)
    return

  message="Your search returned zero results. This function uses exact string matching on ATCC catalog numbers. \
  Check your spelling and try again. If you continue to have issues, try search_fuzzy() to determine whether or not the genome is available from https://genomes.atcc.org."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
  cmd += " -d \'{" + "\"product_id\"" + ": \"" + product_id + "\"}\' https://genomes.atcc.org/api/genomes/search"
  cmd += " 2> /dev/null"
  result_stage = os.popen(cmd)
  result = result_stage.read()
  result_stage.close()
  try:
    if id_only == True or id_only == "True":
        data = json.loads(result)
        if data == []:
          raise emptyResultsError(message)
        else:
          return data[0]['id']
    else:
        data = json.loads(result)
        if data == []:
          raise emptyResultsError(message)
        else:
          return data
  except emptyResultsError as ere:
    logger.warning(ere)





def search_text(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
    if global_api_key:
      if str(apikey) != str(global_api_key):
        apikey = global_api_key 
  else:
      apikey = global_api_key if global_api_key else set_global_api()
  
  id_only = kwargs['id_only'] if 'id_only' in kwargs else True
  if 'text' in kwargs:
    text = kwargs['text']
  else:
    print("""
      search_text() is intended for exact string matching or substring matching on taxonomic names. This will also capture partial matching of ATCC product numbers. 
      This mimics the function of using the search bar default on the ATCC Genome Portal, but DOES NOT FULLY SUPPORT FUZZY MATCHING

      USAGE:
      Required:
      -- (text="<text>") a free text field to search 
      -- your api_key (Globally set variable "global_api_key" or entered "api_key")
      
      Options:
      -- boolean id_only flag
      ---- DEFAULT: 'id_only' boolean is set to True; set it to 'False' to return metadata tpo.
      
      E.g., search_text(text='coli') return resulting Genome IDs that match that string
      E.g., search_text(text='coli',id_only=False) return resulting metadata for genomes that contain that text string
      E.g., metadata = search_text(api_key=YOUR_API_KEY,text='coli',id_only=False) Same as above, but with a manually entered API Key
    """)
    return  

  message="Your search returned zero results. This function uses exact string matching or substrings on taxonomic names, or exact string matching on ATCC catalog numbers. \
  Check your spelling and try again. If you continue to have issues, try search_fuzzy() to determine whether or not the genome is available from https://genomes.atcc.org."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
  cmd += " -d \'{" + "\"text\"" + ": \"" + text + "\"}\' https://genomes.atcc.org/api/genomes/search"
  cmd += " 2> /dev/null"
  result_stage = os.popen(cmd)
  result = result_stage.read()
  result_stage.close()
  try:
    if id_only == True or id_only == "True":
        data = json.loads(result)
        if data == []:
          raise emptyResultsError(message)
        else:
          ids = [e['id'] for e in data]
          return ids
    else:
        data = json.loads(result)
        if data == []:
          raise emptyResultsError(message)
        else:
          return data
  except emptyResultsError as ere:
    logger.warning(ere)





def deep_search(**kwargs):
  
  # API entry O.o.O kwargs['api_key'] > global_api_key
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
    if global_api_key:
      if str(apikey) != str(global_api_key):
        apikey = global_api_key 
  else:
      apikey = global_api_key if global_api_key else set_global_api()
  
  # Method to search. Defaults to JSON format of typical KEY:VALUE
  if "method" in kwargs:
    method=kwargs['method'].lower()
  else:
    method="json"
  
  # Store ID only as true
  id_only = kwargs['id_only'] if 'id_only' in kwargs else True
  
  # If global genome list is empty, repull all JSONs
  genome_list = global_genome_metadata if global_genome_metadata else load_all_metadata()
  
  if 'text' in kwargs:
    text = kwargs['text']
  else:
    print("""
      deep_search() is intended for deep searching of ATCC JSON metadata behind each genome.
      THIS FUNCTION SUPPORTS EXACT KEY|VALUE|STRING MATCHING, WITH "text" METHOD CAPTURE SUBSTRINGS.
      There is currently no similar function on the ATCC Genome Portal.
      This function will search through the JSON metadata of all available genomes for matching strings or values.

      USAGE:
      Required:
      -- (text="<text">) any text field caputured within the JSON of the portal.
      -- your api_key (Globally set variable "global_api_key" or entered "api_key")
      -- a list of genomes (Globally set variable "global_genome_metadata")
      
      Options:
      -- The method you want to search (DEFAULT: set to "json" [ json | text ])
      -- boolean id_only flag (DEFAULT: set to True)
      ---- Set it to 'False' to return full metadata too.
      
      E.g., search_results = deep_search(text="PGAP") will return a list of genomeIDs that had "PGAP" somewhere in the JSON
      E.g., deep_search(text='Lake') return resulting assembly IDs that contain "Lake" in the metadata
      E.g., search_results = deep_search(api_key=YOUR_API_KEY,text="Lake",id_only=False) Same as above, but with a manually entered API Key and full metadata output.
    """)
    return

  message="Your search returned zero results. This function uses exact string matching on the JSON metadata for each genome. \
  Check your spelling and try again. If you continue to have issues, try downloading an assembly metadata file to ensure the search term is present."

  try:  
    items_to_return = []
    
    for item in genome_list:
      if method == "json":
        gotcha=json_search(item, text)
      else:
        gotcha=text in str(item)
      if gotcha:
        if id_only in ['False', False] :
          items_to_return.append(item)
        else:
          items_to_return.append(item['id'])
    if items_to_return:
      return items_to_return
    else:
      emptyResultsError(message)
  except emptyResultsError as ere:
    logger.warning(ere)



def download_assembly(**kwargs):
  if not "download_assembly" or "download_link" in kwargs:
    logger.warning("One download argument must be provided!")
    return
  if "api_key" and "id" in kwargs:
    api_key = kwargs['api_key']
    id = kwargs['id']
    download_assembly_file = kwargs['download_assembly_file'] if 'download_assembly_file' in kwargs else False
    download_assembly_path = kwargs["download_assembly_path"] if 'download_assembly_path' in kwargs else False
    download_link_only = kwargs['download_link_only'] if 'download_link_only' in kwargs else False
    download_assembly_dict = kwargs['download_assembly_dict'] if 'download_assembly_dict' in kwargs else False
    if download_link_only == download_assembly_file and download_link_only in [True,"True"]:
        logger.warning("download_link_only and download_assembly cannot both be True")
        return
    if not download_assembly_path and download_assembly_file in [True,"True"]:
        logger.warning("download_path MUST be provided when selecting download_assembly")
        return
  else:
    print("""
      To use download_assembly(), you must include:
      - api_key=<Your api_key>
      - id=<GenomeID>
      One or more of the flags below should be present:
      - Boolean 'download_link_only' flag     (returns temporary assembly url) 
      - Boolean 'download_assembly_dict' flag (returns assembly file dictionary; [key]=header,[value]=sequence)
      - Boolean 'download_assembly_file' flag (download assembly fasta file to provided path "below")
         - 'download_assembly_path'           (Needed for 'download_assembly_file'; quoted str path to download assembly) \n
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_assembly_file=True,download_assembly_path="/directory/for/download/") downloads an assembly file to provided path
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only=True) return assembly url
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_assembly_dict=True) return assembly dict 
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only=False,download_assembly=False) return raw json result
    """)
    return

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
  cmd += " 2> /dev/null"
  try:
    grab = os.popen(cmd)
    result = grab.read()
    data = json.loads(result)
    grab.close()
    assembly_stage=None
    print(grab)
    if "membership" in result:
      logger.critical("REST API access to the ATCC Genome Portal is only available to supporting member!")
      return result
    print(result)
    if download_link_only == True or download_link_only == "True":
      return data['url']
    elif download_assembly_file == True or download_assembly_file == "True" or download_assembly_dict == True or download_assembly_dict == "True":
      while not assembly_stage:
        assembly_stage = os.popen(f"curl \"{data['url']}\"")
        if not assembly_stage:
          time.sleep(2.5) # Allow 2 seconds per tmp URL generation
      assembly = assembly_stage.read()
      assembly_obj = {}
      for line in assembly.split("\n"):
        if ">" in line:
          header = line.strip()
          assembly_obj[header] = ""
        else:
          assembly_obj[header] += line.strip()
      assembly_stage.close()
      if download_assembly_dict == True or download_assembly_dict =='True':
        return assembly_obj
      elif download_assembly_file == True or download_assembly_file == 'True':
        output_file_path = os.path.join(download_assembly_path, data['save_as_filename'])
        if not os.path.isfile(output_file_path) or os.path.getsize(output_file_path) < 500:
          try:
            with open(output_file_path, 'w') as f: 
              for key, value in assembly_obj.items():
                print(key, file=f)
                print(value, file=f)
              print(f"SUCCESS! File: {output_file_path} now exists!")
          except emptyResultsError as ere:
            logger.warning(ere)
        if os.path.isfile(output_file_path) or os.path.getsize(output_file_path) > 500:
                try:
                    with open(output_file_path, 'r') as f: 
                        for line in f:
                            if line.startswith(">"):
                                filtered=line[line.find('assembly_id='):][13:29]
                                if filtered in str(assembly_obj):
                                    logger.info("This file already exists, and the assembly version is the same...re-downloading!")
                                else:
                                    logger.info("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
                                    incoming_id = assembly[assembly.find('assembly_id='):][13:29]
                                    output_file_path = f'{output_file_path.strip(".fasta")}_{incoming_id}.fasta'
                        with open(output_file_path, 'w') as f: 
                            for key, value in assembly_obj.items():
                                print(key, file=f)
                                print(value, file=f)
                        print(f"SUCCESS! File: {output_file_path} now exists!")
                except Exception as e:
                  print(e)
                  print("Whoops, we encountered a file link bug. Please try again!")
      else:
        return assembly_obj
    else:
      print("You may have forgotten or mispelled a download argument!")
      return data
  except emptyResultsError as ere:
    logger.warning(ere)

def download_annotations(**kwargs):
  if not "download_assembly" or "download_link" in kwargs:
    logger.warning("One download argument must be provided!")
    return
  if "api_key" and "id" in kwargs:
    api_key = kwargs['api_key']
    id = kwargs['id']
    download_annotations_file = kwargs['download_annotations_file'] if 'download_annotations_file' in kwargs else False
    download_annotations_path = kwargs["download_annotations_path"] if 'download_annotations_path' in kwargs else False
    download_link_only = kwargs['download_link_only'] if 'download_link_only' in kwargs else False
    download_annotations_dict = kwargs['download_annotations_dict'] if 'download_annotations_dict' in kwargs else False
    if download_link_only == download_annotations_file and download_annotations_file in [True,"True"]:
        logger.warning("download_link_only and download_assembly cannot both be True")
        return
    if not download_annotations_path and download_annotations_file in [True,"True"]:
        logger.warning("download_path MUST be provided when selecting download_assembly")
        return
  else:
    print("""
      To use download_annotations(), you must include:
      - api_key=<Your api_key>
      - id=<GenomeID>
      One or more of the flags below should be present:
      - Boolean 'download_link_only' flag        (returns temporary annotations url) 
      - Boolean 'download_annotations_dict' flag (returns GenBank raw string)
      - Boolean 'download_annotations_file' flag (downloads GenBank file to provided path "below")
         - 'download_annotations_path'           (Needed for 'download_annotations_file'; quoted str path to download GenBanks) \n

      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="True") return annotation data url 
      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_annotations_dict="True") return the raw genbank file
      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_annotations_file="True",download_annotations_path="/directory/for/download") return the raw json result
    """)
    return

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
  cmd += " 2> /dev/null"
  try:
    grab = os.popen(cmd)
    result = grab.read()
    data = json.loads(result)
    grab.close()
    annotations_stage=None
    if "membership" in result:
      logger.critical("REST API access to the ATCC Genome Portal is only available to supporting member!")
      return result
    print(result)
    if download_link_only == True or download_link_only == "True":
      return data['url']
    elif download_annotations_file == True or download_annotations_file == "True" or download_annotations_dict == True or download_annotations_dict == "True":
      while not annotations_stage:
        annotations_stage = os.popen(f"curl \"{data['url']}\"")
        if not annotations_stage:
          time.sleep(2.5)
      annotations = annotations_stage.read()
      annotations_stage.close()
      if download_annotations_dict == True or download_annotations_dict =='True':
        return annotations
      elif download_annotations_file == True or download_annotations_file == 'True':
        output_file_path = os.path.join(download_annotations_path, data['save_as_filename'])
        if not os.path.isfile(output_file_path) or os.path.getsize(output_file_path) < 500:
          try:
            with open(output_file_path, 'w') as f: 
              f.write(annotations)
            print(f"SUCCESS! File: {output_file_path} now exists!")
          except emptyResultsError as ere:
            logger.warning(ere)
          if os.path.isfile(output_file_path) or os.path.getsize(output_file_path) > 500:
            try:
                with open(output_file_path, 'r') as f: 
                    for line in f:
                        if line.startswith(">"):
                            filtered=line[line.find('assembly_id='):][13:29]
                            if filtered in str(assembly_obj):
                                logger.info("This file already exists, and the assembly version is the same...re-downloading!")
                            else:
                                logger.info("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
                                incoming_id = assembly[assembly.find('assembly_id='):][13:29]
                                output_file_path = f'{output_file_path.strip(".fasta")}_{incoming_id}.fasta'
                    with open(output_file_path, 'w') as f: 
                        for key, value in assembly_obj.items():
                            print(key, file=f)
                            print(value, file=f)
                    print(f"SUCCESS! File: {output_file_path} now exists!")
            except:
              print("Whoops, we encountered a file link bug. Please try again!")
      else:
        return annotations
    else:
      print("You may have forgotten or mispelled a download argument!")
      return data
  except emptyResultsError as ere:
    logger.warning(ere)

def download_metadata(**kwargs):
  if set(kwargs.keys()) == set(["api_key","id"]):
    api_key = kwargs['api_key']
    id = kwargs['id']
  else:
    print("""
      To use download_metadata(), you must include your api_key and an assembly ID.
      E.g., download_metadata(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee) return metadata
    """)
    return 

  message="Your search returned an error. This function uses exact string matching to the hexidecimal string used for assembly identification. \
  The hexidecimal assembly id can be obtained using search_text(), search_product(), or search_fuzzy(). Check your spelling and try again."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}"
  cmd += " 2> /dev/null"
  try:
    result_stage = os.popen(cmd)
    result = result_stage.read()
    result_stage.close()
    if "Not found." in result:
      raise emptyResultsError(message)
    else:
      data = json.loads(result)
      return data
  except emptyResultsError as ere:
    logger.warning(ere)


def iter_paginated_endpoint(url: str, api_key) -> Generator:
    """Fetch all items from a paginated API endpoint"""
    page = 1
    total = 0
    while True:
        resp = requests.get(
            url,
            auth=(api_key, ""),
            params={"page": page},
        )
        if not resp.status_code == 200:
            raise Exception(f"something went wrong {resp.status_code}: {resp.text}")
        pagination_info = json.loads(resp.headers["X-Pagination"])
        page = pagination_info.get("next_page")
        rows = resp.json()
        for row in rows:
            total += 1
            yield row
        if page is None or len(rows) == 0:
            break

def get_genomes(api_key) -> Generator:
    """Fetch list of Genomes using ATCC Genome Management API"""
    return iter_paginated_endpoint("https://genomes.atcc.org/api/genomes", api_key)

def convert_to_genomeid(**kwargs):
  try:
    if "genome_list" in kwargs:
      genomes = kwargs['genome_list']
      final_format = {g["id"]: g for g in genomes}
      print("SUCCESS! Your list can been reformatted")
      return final_format
    else:
      print("""
        The purpose of this function is to format a list of genomic metadata to it's genomeID linked on the portal
        To use convert_to_genomeid(), please provide a list that you would like converted to genomeIDs.

        E.g., formated_genome_list = convert_to_genomeid(genomes=download_all_genomes(api_key=<api_key>)) 
        ------ returns each genomeID as the list index
        For example, a list of genomes provided by `download_all_genomes` named: genome_list;
        -- genome_list[1] may have an ID of "48a898bec49c4b13"...
        -- running this function will output a new list of genomes, where that genome is now indexed as "genome_list['48a898bec49c4b13']"
      """)
  except:
    print("Whoops! Something went wrong. Please double check your arguments and make sure you are passing a list of genomic metadata!")


def download_all_genomes(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
    if global_api_key:
      if str(apikey) != str(global_api_key):
        apikey = global_api_key 
  else:
    apikey = global_api_key if global_api_key else set_global_api()

  if not apikey:
    print("""
      To use download_all_genomes(), you must include your api_key, and a page number.
      E.g., download_all_genomes(api_key=YOUR_API_KEY) returns all metadata
    """)
    return 
  message="Your search returned zero results. Double check that the page you are searching for exists, and try again."
  message2="Your search returned an error. Double check that the page you are searching for exists, and try again."
  
  genomes=list(get_genomes(apikey))
  print(f"Fetched {len(genomes):,} genomes")
  for visibility, count in Counter(
    [g["primary_assembly"]["visibility"] for g in genomes]
      ).items():
          print(f"genomes {visibility=}: {count:,}")

  if "errors" in genomes:
    raise emptyResultsError(message2)
  else:
    global global_genome_metadata
    data = genomes
    global_genome_metadata = data
    if data == [] or genomes == []:
      raise emptyResultsError(message)
    else:
      return data

def download_catalogue(**kwargs):
  if "api_key" in kwargs.keys(): 
    api_key = kwargs['api_key']
    if "output" in kwargs.keys():
      output = kwargs['output']
    else:
      output = False
  else:
    print("""
      To use download_catalogue(), you must include your api_key. The output argument is optional and
      should be used to save the resulting data to a .pkl file. This is required to use the 
      search_fuzzy() function.
      E.g., download_catalogue(api_key=YOUR_API_KEY) # returns the complete list of assembly objects
      E.g., download_catalogue(api_key=YOUR_API_KEY,output="output.txt") # write the list of available genomes to file
    """)
    return

  try:
    page=1
    all_data = []
    empty_result=False
    while empty_result == False:
      cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
      cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
      cmd += " 2> /dev/null"
      result_stage = os.popen(cmd)
      result = result_stage.read()
      data = json.loads(result)
      result_stage.close()
      if data == []:
        if output is False:
          return all_data
        else:
          with open(output, 'wb') as file:
            pkl.dump(all_data, file)
        message = 'End of catalogue data at {0}'.format(page)
        raise emptyResultsError(message)
      else:
        all_data += data
        page+=1

  except emptyResultsError as ere:
    logger.info(ere)

def returnflatlist(newlist, nesteddict):
  for key, value in nesteddict.items():
      # If the value is of the dictionary type, then print
      # all of the values within the nested dictionary.
      if isinstance(value, dict):
          returnflatlist(newlist, value)
      else:
          newlist.append(value)
  return newlist

def search_fuzzy(**kwargs):
  fuzz_value = 75
  if set(kwargs.keys()) == set(["term","catalogue_path"]):
    term = kwargs['term']
    catalogue_path = kwargs['catalogue_path']
  else:
    print("""
      To use search_fuzzy(), you must include a search term and the path to the catalogue
      downloaded via download_catalogue().
      E.g., search_fuzzy(term="coly",catalogue_path="catalogue.txt") search for the term "coly"
    """)
    return 
  catalogue = pkl.load(open(catalogue_path,"rb"))
    ##### In progress
  items_to_return = []
  for item in catalogue:
    fuzzy_match = False
    search_list = []
    returnflatlist(search_list,item)
    for value in search_list:
      if value is not None:
        value = str(value).lower()
        if len(str(value)) > len(term):
          for i in range(len(value)-len(term)):
            if fuzz.ratio(value[i:i+len(term)],term) > fuzz_value:
              fuzzy_match = True
        elif fuzz.ratio(value,term) > fuzz_value:
          fuzzy_match = True
    if fuzzy_match == True:
      items_to_return.append(item)
  return items_to_return 
