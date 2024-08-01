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
from dateutil.parser import parse
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


global global_genome_metadata
global global_api_key


class emptyResultsError(Exception):
  def __init__(self, message):
    self.message = message

def get_global_metadata():
  try:
    if global_genome_metadata:
      return global_genome_metadata
    else:
      load_all_metadata()
  except NameError:
    load_all_metadata()

def get_global_apikey():
  global global_api_key
  try:
    return global_api_key
  except NameError: 
    set_global_api()
    return global_api_key

def set_global_api(**kwargs): #! Intended to 
  """
    set_global_api() is a function used to set an API key global variable "global_api_key".
    Running this command can overwrite an existing "global_api_key" variable, or set it for the first time. \n
    
    --------- USAGE ---------
    Optional arguments:
    \t api_key = <str> \n \t\t An inputed API key to set and/or overwrite the variable "global_api_key".

  """
  global global_api_key
  ## Check to see if was provided as input to this function
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
    global_api_key = apikey
    logger.info(f"API key is now set: {global_api_key}. Please export this api_key under the variable 'ATCC_GENOME_PORTAL_API_KEY'!")
    return
  ## Check to see if set as enviornment variable
  if "ATCC_GENOME_PORTAL_API_KEY" in os.environ and not "api_key" in kwargs:
    global_api_key = os.environ["ATCC_GENOME_PORTAL_API_KEY"]
    logger.info(f"API key has been found: {global_api_key}")
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




def load_all_metadata():
  """
    load_all_metadata() is a helper function used to load the JSON metadata for all available genomes as the variable "global_genome_metadata". 
    This function will be called automatically in deep_search() and download_all_genomes(), but can be ran independently.\n    
  """
  global global_genome_metadata
  ## Check to see if set as enviornment variable
  try:
    if global_genome_metadata:
      logger.info(f"All genomes have been stored under the variable 'global_genome_metadata'")
      logger.info(f"You may need to run `global_genome_metadata=get_global_metadata()` to access this list")
      logger.info(f"If this is an error or you want to requery the genomes, please run download_all_genomes()")
      return
    else:
      global_genome_metadata=download_all_genomes()
  except NameError:
    global_genome_metadata=download_all_genomes()
    if global_genome_metadata:
      logger.info(f"All genomes have been stored under the variable 'global_genome_metadata' ")
      logger.info(f"You may need to run `global_genome_metadata=get_global_metadata()` to access this list")
    return


def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                    yield key + "." + subkey, subvalue
            else:
                yield key, value
    return dict(items())


def tabulate(api_out):
  """
    tabulate() is a helper function used to convert a list of JSON-formatted metadata into a dataframe.
    This function then calls on "format_qc()" to pull relevant metadata fields as dedicated columns. 
  """
  api_out=list(map(flatten_dict, api_out))
  df=pd.DataFrame.from_records(api_out)
  new_df=format_qc(df)
  return new_df


def json_search(nested_dict, term, fuzz_value, fuzz_on): #! Intended to iteratively search JSON key:value schema in genome metadata
  def recursive_search(d, term,fuzz_value, fuzz_on):
    if fuzz_on:
      try:
        for key, value in d.items():
          if fuzz.ratio(value,term) >= fuzz_value or fuzz.ratio(key,term) >= fuzz_value:
            return True
          elif isinstance(value, dict):
            # Recursively search nested dictionaries
            if recursive_search(value, term, fuzz_value, fuzz_on):
              return True
        return False
      except:
        return False  
    else:
      try:
        for key, value in d.items():
          if key == term or value == term:
            return True
          elif isinstance(value, dict):
            # Recursively search nested dictionaries
            if recursive_search(value, term, 0, False):
              return True
        return False
      except AttributeError:
        return False  
  return recursive_search(nested_dict, term,fuzz_value, fuzz_on)
    

def search_product(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key 
    except NameError:
      apikey = get_global_apikey()
  output = kwargs['output'].lower() if "output" in kwargs else 'id'
  if 'product_id' in kwargs:
    product_id = kwargs['product_id']
  else:
    print("""
      search_product() is intended for EXACT matching of ATCC product numbers. 
      This mimics the function of using the search bar on the ATCC Genome Portal set to CATALOG NUMBER \n
      
      --------- USAGE ---------
      Required arguments:
      \t product_id = <str> \n \t\t An ATCC product_id (ex. "BAA-2889")\n
  
      Optional arguments:
      \t output = <str> \n \t\t The API response output format [(id) | json | table]
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [default looks for global_api_key] \n
      
      EXAMPLES:
      \t search_product(product_id='35638') Return resulting Genome ID for ATCC 35638
      \t search_product(product_id='35638', api_key='apikey') Same as above, but this time with a new apikey
      \t search_product(product_id='35638', output=json) Return resulting JSON metadata for ATCC 35638
      \t search_product(product_id='35638', output=table) Return resulting JSON metadata for ATCC 35638 in a informative table
    """)
    return

  message="Your search returned zero results. This function uses exact string matching on ATCC catalog numbers. Check your spelling and try again. \
           If you continue to have issues, try deep_search() to determine whether or not the genome is available from https://genomes.atcc.org."
  
  membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."

  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"

  try:
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
    cmd += " -d \'{" + "\"product_id\"" + ": \"" + product_id + "\"}\'" 
    cmd += f" https://genomes.atcc.org/api/genomes/search"
    cmd += " 2> /dev/null"
    result_stage = os.popen(cmd)
    result = result_stage.read()
    result_stage.close()
    if "API access" in result:
      logger.critical(membership_message)
      return
    if output == "id":
      data = json.loads(result)
      if data == []:
        raise emptyResultsError(message)
      else:
        return [f"ATCC {data[0]['product_id']}:{data[0]['id']}"]
    elif output == "table" or output == "json":
      data = json.loads(result)
      if data == []:
        raise emptyResultsError(message)
      else:
        if output == "json":
          return data
        else:
          return tabulate(data)
    else:
      logger.warning(kwarg_message)
      return
  except emptyResultsError as ere:
    logger.warning(ere)





def search_text(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  output = kwargs['output'].lower() if "output" in kwargs else "id"
  if 'text' in kwargs:
    text = kwargs['text']
  else:
    print("""
      search_text() is intended for exact string matching or substring matching on taxonomic names. This will also capture partial matching of ATCC product numbers. 
      This mimics the function of using the search bar default on the ATCC Genome Portal, but DOES NOT FULLY SUPPORT FUZZY MATCHING \n

      --------- USAGE ---------
      Required arguments:
      \t text = <str> \n \t\t A free text field to search by (ex. "Salmonella enterica")\n      
      
      Optional arguments:
      \t output = <str> \n \t\t The API response format "output" [(id) | json | table]
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [Globally set "global_api_key" or entered "api_key"] \n
      
      EXAMPLES:
      \t search_text(text='coli') return resulting Genome IDs that match that string
      \t search_text(text='coli',output="table") return resulting metadata in TABULAR output for genomes that contain that text string
      \t metadata = search_text(api_key=YOUR_API_KEY,text='coli',output="table") Same as above, but with a manually entered API Key to overwrite set
      \t search_text(text='coli', output="json") return resulting metadata in table-form for genomes that contain that text string
    """)
    return  

  message="Your search returned zero results. This function uses exact string matching or substrings on taxonomic names, or exact string matching on ATCC catalog numbers. \
          Check your spelling and try again. If you continue to have issues, try search_fuzzy() to determine whether or not the genome is available from https://genomes.atcc.org."
  
  membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."
  
  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"

  try:
    page=1
    all_data=[]
    empty_result=False
    while empty_result == False:
      cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
      cmd += " -d \'{" + "\"text\"" + ": \"" + text + "\"}\'"
      cmd += f" https://genomes.atcc.org/api/genomes/search?page={page}"
      cmd += " 2> /dev/null"
      result_stage = os.popen(cmd)
      result = result_stage.read()
      result_stage.close()
      if "API access" in result:
        logger.critical(membership_message)
        return
      if output == "id":
        data = json.loads(result)
        if data == []:
          if all_data == []:
            raise emptyResultsError(message)
          else:
            return [f"ATCC {e['product_id']}:{e['id']}" for e in all_data]
        else:
          all_data += data
          page+=1
      elif output == "table" or output == "json":
        data = json.loads(result)
        if data == []:
          if all_data == []:
            raise emptyResultsError(message)
          else:
            if output == "table":
              all_data = tabulate(all_data)
            return all_data
        else:
          all_data += data
          page+=1
      else:
        logger.warning(kwarg_message)
        return
  except emptyResultsError as ere:
    logger.warning(ere)



def deep_search(**kwargs):
  if 'text' in kwargs:
    text = kwargs['text']
  else:
    print("""
      deep_search() is intended for deep searching of ATCC JSON metadata behind each genome.
      THIS FUNCTION SUPPORTS EXACT KEY|VALUE|STRING MATCHING, WITH "text" METHOD CAPTURE SUBSTRINGS.
      There is currently no similar function on the ATCC Genome Portal.
      This function will search through the JSON metadata of all available genomes for matching strings or values. \n

      --------- USAGE ---------
      Required arguments:
      \t text = <str> \n \t\t any text field caputured within the JSON of the portal.
      -- a list of genomes (Globally set variable "global_genome_metadata")
      
      Optional arguments:
      \t fuzz_on = <str> \n \t\t If provided with a value, enables fuzzy matching  [(75) | value 0-100]
      \t output = <str> \n \t\t The API response format "output" [(id) | json | table]
      \t mode = <str> \n \t\t Choice to search based on a dictionary structure or just raw text [(text) | json]
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [Globally set "global_api_key" or entered "api_key"]
      \t STORE global_genome_metadata \n \t\t A list of genomes can be set as "global_genome_metadata" variable. Not needed as an argument (Globally set variable "global_genome_metadata") \n
      
      EXAMPLES:
      \t deep_search(text="PGAP") will return a list of genomeIDs that had "PGAP" somewhere in the JSON
      \t deep_search(text="Lake", output="id") return resulting assembly IDs that contain "Lake" in the metadata
      \t deep_search(api_key="<apikey>",text="Lake",output="table") Same as above, but with a manually entered API Key and output as an informational table.
      \t deep_search(api_key="<apikey>",text="Lake",output="table",fuzz_on='75') Same as above, but now fuzzy match to '75'
    """)
    return

  message="Your search returned zero results. This function uses exact string matching on the JSON metadata for each genome. \
  Check your spelling and try again. If you continue to have issues, try downloading an assembly metadata file to ensure the search term is present."
  
  empty_genomes="Your global_genome_metadata variable is empty! If this is an error, try resetting your API key and retry!"

  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"

  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  # Method to search. Defaults to JSON format of typical KEY:VALUE
  mode = kwargs['mode'].lower() if "mode" in kwargs else "text"
  fuzz_on = True if 'fuzz_on' in kwargs else False
  if fuzz_on:
    mode='json'
  fuzzy_value = int(kwargs['fuzz_on']) if 'fuzz_on' in kwargs else 75
  # Store ID only as true
  output = kwargs['output'] if 'output' in kwargs else "id"
  # If global genome list is empty, repull all JSONs
  if output not in ['id','json','table'] or mode not in  ['text','str']:
    logger.warning(kwarg_message)
    return

  genome_list = get_global_metadata()
  if not genome_list:
    logger.warning(empty_genomes)
    return
  try:  
    items_to_return = []
    for item in genome_list:
      if mode == "json":
        gotcha=json_search(item, text, fuzzy_value, fuzz_on)
      else:
        gotcha=text in str(item)
      if gotcha:
        if output != "id":
          items_to_return.append(item)
        else:
          items_to_return.append(f"ATCC {item['product_id']}:{item['id']}")
    if items_to_return:
      if output == "table":
        items_to_return = tabulate(items_to_return)
      return items_to_return
    else:
      emptyResultsError(message)
  except emptyResultsError as ere:
    logger.warning(ere)



def download_assembly(**kwargs):
  if "id" in kwargs:
    id = kwargs['id']
  else:
    print("""
      download_assembly() is function to download the fasta assemblies on the ATCC Genome Portal. The genomes files can be downloaded, or output directly to stdout. \n
      
      --------- USAGE ---------
      Required arguments:
      \t id = <str> \n \t\t An ATCC Genome ID (https://genomes.atcc.org/genomes/<genomeid>) \n     
      
      Optional arguments:
      \t output = <str> \n \t\t The API response format "output" [ (dict) | fasta ]
      \t download_dir = [Path <str>] \n \t\t A directory to download the fasta file to. The fasta file will be named automatically.
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \n

      EXAMPLES:
      \t download_assembly(id='304fd1fb9a4e48ee', output='fasta', download_dir="/directory/for/download/") downloads an assembly file to provided path
      \t download_assembly(id='304fd1fb9a4e48ee', output='dict') return a dictionary of the assembly. Key=Header : Value=Seq.
    """)
    return

  membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."

  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"


  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  output = kwargs['output'].lower() if 'output' in kwargs else 'dict'
  file_path = kwargs["download_dir"] if 'download_dir' in kwargs else False
  if output=='fasta':
    if file_path == False:
      logger.critical("'download_dir' MUST be provided when selecting 'output='fasta'")
      return
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
  cmd += " 2> /dev/null"
  try:
    grab = os.popen(cmd)
    result = grab.read()
    data = json.loads(result)
    grab.close()
    assembly=None
    if 'url' not in data.keys():
      logger.warning(f"There does not appear to be a URL for Genome: {id}. Please verify and try again!")
      return
    if "API access" in result:
      logger.critical(membership_message)
      return
    if output in ['fasta','dict']:
      while not assembly:
        assembly_stage = os.popen(f"curl \"{data['url']}\"")
        assembly = assembly_stage.read()
        assembly_obj = {}
        if not assembly:
          time.sleep(2.5) # Allow 2 seconds per tmp URL generation
      for line in assembly.split("\n"):
        if ">" in line:
          header = line.strip()
          assembly_obj[header] = ""
        else:
          assembly_obj[header] += line.strip()
      assembly_stage.close()
      if output=='dict':
        return assembly_obj
      elif output == 'fasta':
        output_file_path = os.path.join(file_path, data['save_as_filename'])
        if not os.path.isfile(output_file_path) or os.path.getsize(output_file_path) < 500:
          try:
            with open(output_file_path, 'w') as f: 
              for key, value in assembly_obj.items():
                print(key, file=f)
                print(value, file=f)
              print(f"SUCCESS! File: {output_file_path} now exists!")
              return
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
                    break
                  else:
                    logger.info("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
                    incoming_id = assembly[assembly.find('assembly_id='):][13:29]
                    output_file_path = f'{output_file_path.strip(".fasta")}_{incoming_id}.fasta'
                    break
              with open(output_file_path, 'w') as f: 
                for key, value in assembly_obj.items():
                  print(key, file=f)
                  print(value, file=f)
              print(f"SUCCESS! File: {output_file_path} now exists!")
              return
          except Exception as e:
            logger.log(e)
            logger.warning("Whoops, we encountered a file link bug. Please try again!")
      else:
        return assembly_obj
    else:
      logger.warning(kwarg_message)
      return
  except emptyResultsError as ere:
    logger.warning(ere)



def download_annotations(**kwargs):
  if "id" in kwargs:
    id = kwargs['id']
  else:
    print("""
      download_annotations() is a function to download the fasta assemblies on the ATCC Genome Portal. 
      The annotation files can be downloaded, or output directly to stdout. \n

      --------- USAGE ---------
      Required arguments:
      \t id = <str> \n \t\t An ATCC Genome ID (https://genomes.atcc.org/genomes/<genomeid>) \n     
      
      Optional arguments:
      \t output = <str> \n \t\t The API response format "output" [ (dict) | gbk ]
      \t download_dir = [Path <str>] \n \t\t A directory to download the GenBank files to. The file will be named automatically.
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \n
      
      EXAMPLES:
      download_annotations(id='304fd1fb9a4e48ee', output='gbk', download_dir='/directory/for/download/') downloads a GenBank file to provided path
      download_annotations(id='304fd1fb9a4e48ee', output='dict') return the raw genbank file
    """)
    return
  
  membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."
  
  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"


  if "api_key" in kwargs:
    apikey = kwargs['api_key'] 
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  output = kwargs['output'].lower() if 'output' in kwargs else 'dict'
  file_path = kwargs["download_dir"] if 'download_dir' in kwargs else False
  if output=='gbk':
    if file_path == False:
      logger.critical("'download_dir' MUST be provided when selecting 'output='gbk'")

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
  cmd += " 2> /dev/null"
  try:
    grab = os.popen(cmd)
    result = grab.read()
    data = json.loads(result)
    grab.close()
    annotations_stage=None
    annotations='The specified key does not exist'
    if 'url' not in data.keys():
      logger.warning(f"There does not appear to be a URL for Genome: {id}. Please verify and try again!")
      return
    if "API access" in result:
      logger.critical(membership_message)
      return
    if output in ['gbk','dict']:
      counter=0
      while "The specified key does not exist" in annotations and counter <=10:
        annotations_stage = os.popen(f"curl \"{data['url']}\"")
        annotations = annotations_stage.read()
        annotations_stage.close()
        if "The specified key does not exist" in annotations :
          time.sleep(2.5)
          counter += 1
      if "The specified key does not exist" in annotations:
        logger.warning("The URL to download this file appears to be broken. Please try again later!")
      if output == 'dict':
        return annotations
      elif output =='gbk':
        output_file_path = os.path.join(file_path, data['save_as_filename'])
        if not os.path.isfile(output_file_path) or os.path.getsize(output_file_path) < 500:
          try:
            with open(output_file_path, 'w') as f: 
              f.write(annotations)
            print(f"SUCCESS! File: {output_file_path} now exists!")
            return
          except emptyResultsError as ere:
            logger.warning(ere)
        if os.path.isfile(output_file_path) or os.path.getsize(output_file_path) > 500:
          try:
            with open(output_file_path, 'r') as f: 
              for line in f:
                if line.startswith("VERSION     "):
                  filtered=line[line.find('assembly_'):][9:25]
                  continue
            if filtered in str(annotations):
              logger.info("This file already exists, and the assembly version is the same...re-downloading!")
            else:
              logger.info("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
              incoming_id = annotations[annotations.find('assembly_'):][9:25]
              output_file_path = f'{output_file_path.strip(".gbk")}_{incoming_id}.gbk'
            with open(output_file_path, 'w') as f: 
              f.write(annotations)
            print(f"SUCCESS! File: {output_file_path} now exists!")
            return
          except:
            logger.warning("Whoops, we encountered a file link bug. Please try again!")
            return
      else:
        return annotations
    else:
      logger.warning(kwarg_message)
      return
  except emptyResultsError as ere:
    logger.warning(ere)




def download_metadata(**kwargs):
  if "id" in kwargs:
    id = kwargs['id']
  else:
    print("""
      download_metadata() is a function intended to download the JSON metadata behind each assembly on the portal.
      The metadata can be output as a dictionary, or as an informative table with the correct fields already formatted.\n
      
      --------- USAGE ---------
      Required arguments:
      \t id = <str> \n \t\t An ATCC Genome ID (https://genomes.atcc.org/genomes/<genomeid>) \n     
      
      Optional arguments:
      \t output = <str> \n \t\t The API response format "output" [ (dict) | table ]
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \n

    """)
    return 

  message="Your search returned an error. This function uses exact string matching to the hexidecimal string used for assembly identification. \
  The hexidecimal assembly id can be obtained using search_text(), search_product(), or search_fuzzy(). Check your spelling and try again."

  membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."
  
  kwarg_message="Whoops, make sure you are providing all the correct arguments and choices!"


  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  output = kwargs['output'].lower() if 'output' in kwargs else 'dict'

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {apikey}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}"
  cmd += " 2> /dev/null"
  if output not in ['dict','table']:
    logger.warning(kwarg_message)
    return
  try:
    result_stage = os.popen(cmd)
    result = result_stage.read()
    result_stage.close()
    if "API access" in result:
      logger.critical(membership_message)
      return
    if "Not found." in result:
      raise emptyResultsError(message)
    else:
      data = json.loads(result)
      if output == "table":
        data=tabulate([data])
      return data
  except emptyResultsError as ere:
    logger.warning(ere)


def iter_paginated_endpoint(url: str, api_key) -> Generator:
    """Fetch all items from a paginated API endpoint"""
    page = 1
    total = 0
    membership_message="API access to the ATCC Genome Portal requires a supporting membership. Please visit https://genomes.atcc.org/plans to subscribe."
    while True:
        resp = requests.get(
            url,
            auth=(api_key, ""),
            params={"page": page},
        )
        
        if "API access" in resp.text:
          logger.critical(membership_message)
          return
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
        convert_to_genomeid() is a function to convert a list of genomic JSON metadata to a genomeID indexed list. 
        By default, any genomic JSON metadata is indexed based on position of the Dict within the list. \n

        --------- USAGE ---------
        Required arguments:
        \t genome_list = [list] \n \t\t A list of ATCC JSON formatted genome metadata objects \n

        EXAMPLES:
        \t formatted_genomes = convert_to_genomeid(global_genome_metadata) Creates a defined variable that host the same genomes found in "global_genome_metadata".
        \t\t These genomes of formatted_genomes can now be searched directly through formatted_genomes['<genomeID>'].
      """)

  except:
    print("Whoops! Something went wrong. Please double check your arguments and make sure you are passing a list of genomic metadata!")


def download_all_genomes(**kwargs):
  if "api_key" in kwargs:
    apikey = kwargs['api_key']
  else:
    try:
      apikey = global_api_key
    except NameError:
      apikey = get_global_apikey()
  if not apikey:
    print("""
      download_all_genomes() is a function intended to download the JSON metadata for ALL ATCC genomes currently available on the ATCC Genome Portal.
      This function will store the results as the variable "global_genome_metadata", and will also report to stdOUT.\n

      --------- USAGE ---------
      Required arguments: NONE \n
      
      Optional arguments:
      \t api_key = <str> \n \t\t Your Genome Portal APIKey [(global_api_key) | overwrite if provided ] \n

      EXAMPLES:
      \t download_all_genomes() downloads all genomes as a list of JSON dictionaries to the variable "global_genome_metadata".
      \t secondary_var=download_all_genomes() downloads all genomes as a list of JSON dictionaries to the variable "global_genome_metadata" AND "secondary_var".
    """)
    return 
  message="Your search returned zero results. Double check that the page you are searching for exists, and try again."
  message2="Your search returned an error. Double check that the page you are searching for exists, and try again."

  genomes=list(get_genomes(apikey))
  if not genomes:
    return
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
      return data
    else:
      return data

def format_qc(dataframe):
  """Format table of JSON into human readable and digestable"""
  df=dataframe
  new_df=pd.DataFrame()

  new_df['atcc_product_id'] = df['product_id']
  new_df['name'] = df['attributes.atcc_metadata.preferred_taxonomy_name'].combine_first(df['taxon_name'])
  new_df['taxid'] = df['taxon_id']
  new_df['genome_id'] = df['id']
  new_df['assembly_id'] = df['primary_assembly.id']
  new_df['collection'] = "ATCC " + df['collection_name'].str.capitalize()
  
  # Extended metadata inclusion
  df['extended_json_format'] = df.apply(lambda row: True if 'attributes.atcc_metadata.other_metadata.catalog_details.ATCC_catalog_number' in row else False, axis=1)

  new_df['contig_count'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_stats.filtered_contig_count'] if row['extended_json_format'] else row['primary_assembly.attributes.qc_statistics.assembly_statistics.filtered.total_contigs'], axis=1)
  new_df['total_contig_length'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_stats.filtered_contig_length'] if row['extended_json_format'] else row['primary_assembly.attributes.qc_statistics.assembly_statistics.filtered.total_contig_length'], axis=1)
  new_df['total_circular_contigs'] = df.apply(lambda row: row['primary_assembly.attributes.qc_statistics.assembly_statistics.filtered.total_circular_contigs'], axis=1)
  new_df['total_n_assembly'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_stats.number_of_n_bases'] if (row['extended_json_format'] and pd.notnull(row['attributes.atcc_metadata.other_metadata.genome_stats.number_of_n_bases'])) else (sum([i['ambiguous_nucleotide_count'] for i in row['primary_assembly.attributes.qc_statistics.assembly_statistics.filtered.contig_statistics']])) if isinstance(row['primary_assembly.attributes.qc_statistics.assembly_statistics.filtered.contig_statistics'], list) else None, axis=1)
  new_df['illumina_barcoding_kit'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.illumina_metadata.barcoding_kit'] if row['extended_json_format'] else None, axis=1)
  new_df['illumina_library_kit'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.illumina_metadata.library_kit'] if row['extended_json_format'] else None, axis=1)
  new_df['illumina_sequencer'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.illumina_metadata.sequencer'] if row['extended_json_format'] else None, axis=1)
  new_df['illumina_basecalling_model'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.illumina_metadata.basecaller_model'] if row['extended_json_format'] else None, axis=1)
  new_df['illumina_basecalling_version'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.illumina_metadata.basecaller_version'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_barcoding_kit'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.barcoding_kit'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_library_kit'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.library_kit'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_flowcell_type'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.flowcell_type'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_sequencer'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.sequencer'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_basecalling_model'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.basecaller_model'] if row['extended_json_format'] else None, axis=1)
  new_df['nanopore_basecalling_version'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.ont_metadata.basecaller_version'] if row['extended_json_format'] else None, axis=1)

  new_df['genome_page_creation'] = df.apply(lambda row: parse(row['created_at']).strftime('%x %X'), axis=1)  
  new_df['genome_assembled_by'] = df['attributes.atcc_metadata.notes'].apply(lambda x: 'ATCC' if ('attributes.atcc_metadata.notes' in df.columns and ('oatmeal' in str(x).lower() or 'manual' in str(x).lower())) else 'OneCodex')
  df['genome_assembled_by'] = new_df['genome_assembled_by']
  
  new_df['atcc_lotnumber'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.catalog_details.ATCC_lot_number'] if row['extended_json_format'] else None, axis=1)
  new_df['assembled_by'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.asssembled_by'] if row['extended_json_format'] else row['genome_assembled_by'], axis=1)
  new_df['assembled_date'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.asssembly_date'] if row['extended_json_format'] else None, axis=1)
  new_df['assembler_software'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.asssembler_software'] if row['extended_json_format'] else None, axis=1)
  new_df['annotatated_by'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.annotatated_by'] if row['extended_json_format'] else row['genome_assembled_by'], axis=1)
  new_df['annotations_date'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.annotations_date'] if row['extended_json_format'] else None, axis=1)
  new_df['annotations_software'] = df.apply(lambda row: row['attributes.atcc_metadata.other_metadata.genome_provider.annotations_software'] if row['extended_json_format'] else None, axis=1)

  new_df['genome_completeness'] = df.apply(lambda row: row['attributes.atcc_metadata.qc_statistics.assembly_quality_control.genome_completeness'] if row['genome_assembled_by'] == 'ATCC' 
    else row['primary_assembly.attributes.qc_statistics.checkm_results.completeness'] if pd.notnull(row['primary_assembly.attributes.qc_statistics.checkm_results.completeness']) 
    else row['primary_assembly.attributes.qc_statistics.virify_results.completeness'] if pd.notnull(row['primary_assembly.attributes.qc_statistics.virify_results.completeness']) else None, axis=1)
  new_df['genome_contamination'] = df.apply(lambda row: row['attributes.atcc_metadata.qc_statistics.assembly_quality_control.genome_contamination'] if row['genome_assembled_by'] == 'ATCC' 
    else row['primary_assembly.attributes.qc_statistics.checkm_results.contamination'] if pd.notnull(row['primary_assembly.attributes.qc_statistics.checkm_results.contamination']) else None, axis=1)
  
  new_df['genome_completeness'] = new_df.apply(lambda row: (row['genome_completeness']*100) if (row['genome_assembled_by'] == 'OneCodex' and row['collection'] == "ATCC Virology") else None, axis=1)
  new_df['illumina_depth'] = df.apply(lambda row: row['attributes.atcc_metadata.qc_statistics.assembly_quality_control.illumina_depth_of_coverage'] if 'attributes.atcc_metadata.qc_statistics.assembly_quality_control.illumina_depth_of_coverage' in df.columns else row['primary_assembly.attributes.qc_statistics.sequencing_statistics.illumina.depth.mean'], axis=1)
  new_df['nanopore_depth'] = df.apply(lambda row: row['attributes.atcc_metadata.qc_statistics.assembly_quality_control.ont_depth_of_coverage'] if 'attributes.atcc_metadata.qc_statistics.assembly_quality_control.ont_depth_of_coverage' in df.columns else row['primary_assembly.attributes.qc_statistics.sequencing_statistics.ont.depth.mean'], axis=1)
  #AMR Sitecore Section
  new_df['amr_intermediate'] = df.apply(lambda row: row['attributes.atcc_metadata.amr_intermediate'] if row['attributes.atcc_metadata.amr_intermediate'] != [] else None, axis=1)
  new_df['amr_resistant'] = df.apply(lambda row: row['attributes.atcc_metadata.amr_resistant'] if row['attributes.atcc_metadata.amr_resistant'] != [] else None, axis=1)
  new_df['amr_susceptible'] = df.apply(lambda row: row['attributes.atcc_metadata.amr_susceptible'] if row['attributes.atcc_metadata.amr_susceptible'] != [] else None, axis=1)
  new_df['antibiotic_resistance'] = df.apply(lambda row: row['attributes.atcc_metadata.antibiotic_resistance'] if 'attributes.atcc_metadata.antibiotic_resistance' in row else None, axis=1)
  new_df['antigenic_prop'] = df.apply(lambda row: row['attributes.atcc_metadata.antigenic_prop'] if 'attributes.atcc_metadata.antigenic_prop' in row else None, axis=1)
  new_df['drug_repository'] = df.apply(lambda row: row['attributes.atcc_metadata.drug_repository'] if 'attributes.atcc_metadata.drug_repository' in row else None, axis=1)
  new_df['genotype'] = df.apply(lambda row: row['attributes.atcc_metadata.genotype'] if 'attributes.atcc_metadata.genotype' in row else None, axis=1)
  new_df['isolation_new_web'] = df.apply(lambda row: row['attributes.atcc_metadata.isolation_new_web'] if 'attributes.atcc_metadata.isolation_new_web' in row else None, axis=1)
  new_df['biosafety_level'] = df.apply(lambda row: int(row['attributes.atcc_metadata.bsl']) if 'attributes.atcc_metadata.bsl' in row and pd.notnull(row['attributes.atcc_metadata.bsl']) else None, axis=1)
  new_df['notes'] = df.apply(lambda row: row['attributes.atcc_metadata.notes'] if 'notes' in df.columns  else None, axis=1)
  #new_df['genome_page_creation']=new_df['genome_page_creation'].apply(pd.to_datetime)
  #new_df=new_df.sort_values(by='genome_page_creation',ascending=False)
  
  return new_df