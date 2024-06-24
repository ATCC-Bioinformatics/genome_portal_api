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
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

class emptyResultsError(Exception):
  def __init__(self, message):
    self.message = message

def search_product(**kwargs):
  if set(kwargs.keys()) == set(['api_key','product_id','id_only']):
    api_key = kwargs['api_key']
    product_id = kwargs['product_id']
    id_only = kwargs['id_only']
  else:
    print("""
      To use search_product(), you must include your api_key, a product_id, and a boolean id_only flag. If the 
      id_only boolean is set to True, then only the assembly id is retrieved.
      E.g., search_product(api_key=YOUR_API_KEY,product_id=35638,id_only=False) return resulting metadata
      E.g., x = search_product(api_key=YOUR_API_KEY,product_id=35638,id_only=True) return only the assembly id
    """)
    return

  message="Your search returned zero results. This function uses exact string matching on ATCC catalog numbers. \
  Check your spelling and try again. If you continue to have issues, try search_fuzzy() to determine whether or not the genome is available from https://genomes.atcc.org."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
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
  if set(kwargs.keys()) == set(['api_key','text','id_only']):
    api_key = kwargs['api_key']
    text = kwargs['text']
    id_only = kwargs['id_only']
  else:
    print("""
      To use search_text(), you must include your api_key, a search string and a boolean id_only flag. If the id_only boolean is set 
      to True, then only the assembly id is retrieved.
      E.g., search_text(api_key=YOUR_API_KEY,text="coli",id_only="False") return resulting metadata
      E.g., x = search_text(api_key=YOUR_API_KEY,text="asp",id_only="True") return list of assembly ids
    """)
    return  

  message="Your search returned zero results. This function uses exact string matching or substrings on taxonomic names, or exact string matching on ATCC catalog numbers. \
  Check your spelling and try again. If you continue to have issues, try search_fuzzy() to determine whether or not the genome is available from https://genomes.atcc.org."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
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
    if "membership" in result:
      logger.critical("REST API access to the ATCC Genome Portal is only available to supporting member!")
      return result
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
        # if os.path.isfile(output_file_path):
        #     if os.path.getsize(output_file_path) > 500:
        #         print(f"{output_file_path} already exists in download folder! Moving on!")
        #         return
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
                                    logger.log("This file already exists, and the assembly version is the same...re-downloading!")
                                else:
                                    logger.log("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
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
    if "message" in result:
      logger.critical("REST API access to the ATCC Genome Portal is only available to supporting member!")
      return result
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
        # if os.path.isfile(output_file_path):
        #     if os.path.getsize(output_file_path) > 500:
        #         print(f"{output_file_path} already exists in download folder! Moving on!")
        #         return
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
                                logger.log("This file already exists, and the assembly version is the same...re-downloading!")
                            else:
                                logger.log("You had a previous version of this genome, but we have updated the assembly version...downloading with assembly ID appended to name!")
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
  if "genome_list" in kwargs:
    genomes = kwargs['genome_list']
    final_format = {g["id"]: g for g in genomes}
  if "annotations_list" in kwargs:
    annotations = kwargs['annotations_list']
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
    return final_format


def download_all_genomes(**kwargs):
  if "api_key" in kwargs:
    api_key = kwargs['api_key']
    genomes=list(get_genomes(api_key))
    print(f"Fetched {len(genomes):,} genomes")
    for visibility, count in Counter(
      [g["primary_assembly"]["visibility"] for g in genomes]
        ).items():
            print(f"genomes {visibility=}: {count:,}")
  else:
    print("""
      To use download_all_genomes(), you must include your api_key, and a page number.
      E.g., download_all_genomes(api_key=YOUR_API_KEY) returns all metadata
    """)
    return 
  message="Your search returned zero results. Double check that the page you are searching for exists, and try again."
  message2="Your search returned an error. Double check that the page you are searching for exists, and try again."

  if "errors" in genomes:
    raise emptyResultsError(message2)
  else:
    data = genomes
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
