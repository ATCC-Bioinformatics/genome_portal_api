import os
import argparse
from argparse import RawTextHelpFormatter
import json
import pickle as pkl
from fuzzywuzzy import fuzz

def search_product(**kwargs):
  if set(kwargs.keys()) == set(['jwt','product_id','id_only']):
    jwt = kwargs['jwt']
    product_id = kwargs['product_id']
    id_only = kwargs['id_only']
  else:
    print("""
      To use search_product(), you must include your jwt, a product_id, and a boolean id_only flag. If the 
      id_only boolean is set to True, then only the assembly id is retrieved.
      E.g., search_product(jwt=YOUR_JWT,product_id=35638,id_only=False) return resulting metadata
      E.g., x = search_product(jwt=YOUR_JWT,product_id=35638,id_only=True) return only the assembly id
    """)
    return
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += " -d \'{" + "\"product_id\"" + ": \"" + product_id + "\"}\' https://genomes.atcc.org/api/genomes/search"
  cmd += " 2> /dev/null"
  result = os.popen(cmd).read()
  if id_only == True or id_only == "True":
      data = json.loads(result)
      return data[0]['id']
  else:
      return json.loads(result)

def search_text(**kwargs):
  if set(kwargs.keys()) == set(['jwt','text','id_only']):
    jwt = kwargs['jwt']
    text = kwargs['text']
    id_only = kwargs['id_only']
  else:
    print("""
      To use search_text(), you must include your jwt, a search string and a boolean id_only flag. If the id_only boolean is set 
      to True, then only the assembly id is retrieved.
      E.g., search_text(jwt=YOUR_JWT,text="coli",id_only="False") return resulting metadata
      E.g., x = search_text(jwt=YOUR_JWT,text="asp",id_only="True") return list of assembly ids
    """)
    return  
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += " -d \'{" + "\"text\"" + ": \"" + text + "\"}\' https://genomes.atcc.org/api/genomes/search"
  cmd += " 2> /dev/null"
  result = os.popen(cmd).read()
  if id_only == True or id_only == "True":
      data = json.loads(result)
      ids = [e['id'] for e in data]
      return ids
  else:
      return json.loads(result)

def download_assembly(**kwargs):
  if set(kwargs.keys()) == set(["jwt","id","download_link_only","download_assembly"]):
    jwt = kwargs['jwt']
    id = kwargs['id']
    download_link_only = kwargs['download_link_only']
    download_assembly = kwargs['download_assembly']
    if download_link_only == download_assembly and download_link_only in [True,"True"]:
        print("""
        download_link_only and download_assembly cannot both be True
        """)
        return
  else:
    print("""
      To use download_assembly(), you must include your jwt, an assembly ID, a boolean download_link_only flag, and a boolean 
      download_assembly flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved. 
      If the download_assembly boolean is set to True, then only the assembly download link is retrieved.
      E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="True",download_assembly="False") return assembly url
      E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="True") return assembly dict 
      E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_assembly="False") return raw json result
    """)
    return  
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
  cmd += " 2> /dev/null"
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

def download_annotations(**kwargs):
  if set(kwargs.keys()) == set(["jwt","id","download_link_only","download_annotations"]):
    jwt = kwargs['jwt']
    id = kwargs['id']
    download_link_only = kwargs['download_link_only']
    download_annotations = kwargs['download_annotations']
    if download_link_only == download_annotations and download_link_only in [True,"True"]:
        print("""
        download_link_only and download_annotations cannot both be True
        """)
        return
  else:
    print("""
      To use download_annotations(), you must include your jwt, an assembly ID, a boolean download_link_only flag, and a boolean 
      download_annotations flag. If the download_link_only boolean is set to True, then only the assembly download link is retrieved.
      If the download_annotations boolean is set to True, then only the assembly download link is retrieved.
      E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="True",download_annotations="False") return annotation data url 
      E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="True") return the raw genbank file
      E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,download_link_only="False",download_annotations="False") return the raw json result
    """)
    return 
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
  cmd += " 2> /dev/null"
  result = os.popen(cmd).read()
  data = json.loads(result)
  if download_link_only == True or download_link_only == "True":
    return data['url']
  elif download_annotations == True or download_annotations == "True":
    annotations = os.popen(f"curl \"{data['url']}\"").read()
    return annotations
  else:
    return data

def download_metadata(**kwargs):
  if set(kwargs.keys()) == set(["jwt","id"]):
    jwt = kwargs['jwt']
    id = kwargs['id']
  else:
    print("""
      To use download_metadata(), you must include your jwt and an assembly ID.
      E.g., download_metadata(jwt=YOUR_JWT,id=304fd1fb9a4e48ee) return metadata
    """)
    return 
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += f" https://genomes.atcc.org/api/genomes/{id}"
  cmd += " 2> /dev/null"
  result = os.popen(cmd).read()
  data = json.loads(result)
  return data


def download_all_genomes(**kwargs):
  if set(kwargs.keys()) == set(["jwt","page"]):
    jwt = kwargs['jwt']
    page = kwargs['page']
  else:
    print("""
      To use download_all_genomes(), you must include your jwt, and a page number.
      E.g., download_all_genomes(jwt=YOUR_JWT,page=1,output="output.txt") return page 1 of metadata
    """)
    return 
  cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
  cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
  cmd += " 2> /dev/null"
  result = os.popen(cmd).read()
  data = json.loads(result)
  return data

def download_catalogue(**kwargs):
  if "jwt" in kwargs.keys(): 
    jwt = kwargs['jwt']
    if "output" in kwargs.keys():
      output = kwargs['output']
    else:
      output = False
  else:
    print("""
      To use download_catalogue(), you must include your jwt. The output argument is optional and
      should be used to save the resulting data to a .pkl file. This is required to use the 
      search_fuzzy() function.
      E.g., download_catalogue(jwt=YOUR_JWT) # returns the complete list of assembly objects
      E.g., download_catalogue(jwt=YOUR_JWT,output="output.txt") # write the list to file
    """)
    return 
  page=1
  all_data = []
  empty_result=False
  while empty_result == False:
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
    cmd += " 2> /dev/null"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if data == []:
      empty_result=True
    else:
      all_data += data
      page+=1
  if output == False:
    return all_data
  else:
    with open(output, 'wb') as file:
      pkl.dump(all_data, file)

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