import os
import argparse
from argparse import RawTextHelpFormatter
import json
import pickle as pkl
from fuzzywuzzy import fuzz
import logging

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
  result = os.popen(cmd).read()

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
  result = os.popen(cmd).read()
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
  if set(kwargs.keys()) == set(["api_key","id","download_link_only","download_assembly"]):
    api_key = kwargs['api_key']
    id = kwargs['id']
    download_link_only = kwargs['download_link_only']
    download_assembly = kwargs['download_assembly']
    if download_link_only == download_assembly and download_link_only in [True,"True"]:
        logger.warning("download_link_only and download_assembly cannot both be True")
        return
  else:
    print("""
      To use download_assembly(), you must include your api_key, an assembly ID, a boolean download_link_only flag, and a boolean 
      download_assembly flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved. 
      If the download_assembly boolean is set to True, then only the assembly download link is retrieved.
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="True",download_assembly="False") return assembly url
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="True") return assembly dict 
      E.g., download_assembly(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="False") return raw json result
    """)
    return

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
  cmd += " 2> /dev/null"
  try:
    result = os.popen(cmd).read()
    data = json.loads(result)
    if download_link_only == True or download_link_only == "True":
      return data['url']
    elif download_assembly == True or download_assembly == "True":
      assembly = os.popen(f"curl \"{data['url']}\"").read()
      assembly_obj = {}
      for line in assembly.split("\n"):
        if ">" in line:
          header = line.strip()
          assembly_obj[header] = ""
        else:
          assembly_obj[header] += line.strip()
      return assembly_obj
    else:
      return data
  except emptyResultsError as ere:
    logger.warning(ere)




def download_annotations(**kwargs):
  if set(kwargs.keys()) == set(["api_key","id","download_link_only","download_annotations"]):
    api_key = kwargs['api_key']
    id = kwargs['id']
    download_link_only = kwargs['download_link_only']
    download_annotations = kwargs['download_annotations']
    if download_link_only == download_annotations and download_link_only in [True,"True"]:
        logger.warning("download_link_only and download_assembly cannot both be True")
        return
  else:
    print("""
      To use download_annotations(), you must include your api_key, an assembly ID, a boolean download_link_only flag, and a boolean 
      download_annotations flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved.
      If the download_annotations boolean is set to True, then only the assembly download link is retrieved.
      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="True",download_annotations="False") return annotation data url 
      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="True") return the raw genbank file
      E.g., download_annotations(api_key=YOUR_API_KEY,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="False") return the raw json result
    """)
    return

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
  cmd += " 2> /dev/null"
  try:
    result = os.popen(cmd).read()
      # if "<!DOCTYPE html>" in result:
      #   raise emptyResultsError(message)
      # else:
    data = json.loads(result)
    if download_link_only == True or download_link_only == "True":
      return data['url']
    elif download_annotations == True or download_annotations == "True":
      annotations = os.popen(f"curl \"{data['url']}\"").read()
      return annotations
    else:
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
    result = os.popen(cmd).read()
    if "Not found." in result:
      raise emptyResultsError(message)
    else:
      data = json.loads(result)
      return data
  except emptyResultsError as ere:
    logger.warning(ere)


def download_all_genomes(**kwargs):
  if set(kwargs.keys()) == set(["api_key","page"]):
    api_key = kwargs['api_key']
    page = kwargs['page']
  else:
    print("""
      To use download_all_genomes(), you must include your api_key, and a page number.
      E.g., download_all_genomes(api_key=YOUR_API_KEY,page=1,output="output.txt") return page 1 of metadata
    """)
    return 
  message="Your search returned zero results. Double check that the page you are searching for exists, and try again."
  message2="Your search returned an error. Double check that the page you are searching for exists, and try again."

  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"X-API-Key: {api_key}\""
  cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
  cmd += " 2> /dev/null"
  try:
    result = os.popen(cmd).read()
    if "errors" in result:
      raise emptyResultsError(message2)
    else:
      data = json.loads(result)
      if data == [] or result == []:
        raise emptyResultsError(message)
      else:
        return data
  except emptyResultsError as ere:
    logger.warning(ere)

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
      result = os.popen(cmd).read()
      data = json.loads(result)
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
  stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
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

### Create test function
