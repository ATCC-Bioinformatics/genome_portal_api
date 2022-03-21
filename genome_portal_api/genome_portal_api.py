import os
import argparse
from argparse import RawTextHelpFormatter
import json
def search_product(**kwargs):
    if set(kwargs.keys()) == set(['jwt','product_id','output','id_only']):
      jwt = kwargs['jwt']
      product_id = kwargs['product_id']
      output = kwargs['output']
      id_only = kwargs['id_only']
    else:
      print("""
        To use search_product(), you must include your jwt, a product_id, 
        your desired output, and a boolean id_only flag. The output may be
        a file path, such as path/to/file.txt, or the string "return" which
        returns the output from the function. If the id_only boolean is set 
        to True, then only the assembly id is retrieved.
        E.g., search_product(jwt=YOUR_JWT,product_id=35638,output="output.txt",id_only=False) print resulting
        metadata to file
        E.g., x = search_product(jwt=YOUR_JWT,product_id=35638,output="return",id_only=True) return only the assembly id
      """)
      return
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += " -d \'{" + "\"product_id\"" + ": \"" + product_id + "\"}\' https://genomes.atcc.org/api/genomes/search"
    result = os.popen(cmd).read()
    if id_only == True or id_only == "True":
        data = json.loads(result)
        if output == 'return':
            return data[0]['id']
        else:
            with open(output,'w') as out:
                out.write(data[0]['id'])
    else:
        if output == 'return':
          return json.loads(result)
        else:
          with open(output,'w') as out:
            out.write(json.dumps(json.loads(result),indent=1))

def search_text(**kwargs):
    if set(kwargs.keys()) == set(['jwt','text','output','id_only']):
      jwt = kwargs['jwt']
      text = kwargs['text']
      output = kwargs['output']
      id_only = kwargs['id_only']
    else:
      print("""
        To use search_text(), you must include your jwt, a search string, 
        your desired output, and a boolean id_only flag. The output may be
        a file path, such as path/to/file.txt, or the string "return" which
        returns the output from the function. If the id_only boolean is set 
        to True, then only the assembly id is retrieved.
        E.g., search_product(YOUR_JWT,"coli","output.txt","False") print resulting
        metadata to file
        E.g., x = search_product(YOUR_JWT,"asp","return","True") return list of assembly ids
      """)
      return  
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += " -d \'{" + "\"text\"" + ": \"" + text + "\"}\' https://genomes.atcc.org/api/genomes/search"
    result = os.popen(cmd).read()
    if id_only == True or id_only == "True":
        data = json.loads(result)
        ids = [e['id'] for e in data]
        if output == 'return':
            return ids
        else:
            with open(output,'w') as out:
                out.write(','.join(ids))
    else:
        if output == 'return':
          return json.loads(result)
        else:
          with open(output,'w') as out:
            out.write(json.dumps(json.loads(result),indent=1))


def download_assembly(**kwargs):
    if set(kwargs.keys()) == set(["jwt","id","output","download_link_only","download_assembly"]):
      jwt = kwargs['jwt']
      id = kwargs['id']
      output = kwargs['output']
      download_link_only = kwargs['download_link_only']
      download_assembly = kwargs['download_assembly']
      if download_link_only == download_assembly and download_link_only in [True,"True"]:
          print("""
          download_link_only and download_assembly cannot both be True
          """)
          return
    else:
      print("""
        To use download_assembly(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        download_assembly flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function. If the download_link_only boolean is set to True, then only 
        the assembly download link is retrieved. If the download_assembly boolean is
        set to True, then only the assembly download link is retrieved.
        E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="output.txt",download_link_only="True",download_assembly="False") print assembly url to file
        E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="return",download_link_only="False",download_assembly="True") return assembly dict 
        E.g., download_assembly(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="return",download_link_only="False",download_assembly="False") return raw json result
      """)
      return  
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if download_link_only == True or download_link_only == "True":
      if output == 'return':
        return data['url']
      else:
        with open(output,'w') as out:
          out.write(data['url'])
    elif download_assembly == True or download_assembly == "True":
      assembly = os.popen(f"curl \"{data['url']}\"").read()
      if output == 'return':
        assembly_obj = {}
        for line in assembly.split("\n"):
          if ">" in line:
            header = line.strip()
            assembly_obj[header] = ""
          else:
            assembly_obj[header] += line.strip()
        return assembly_obj
      else:
        with open(output,'w') as out:
          out.write(assembly)
    else:
        return data

def download_annotations(**kwargs):
    if set(kwargs.keys()) == set(["jwt","id","output","download_link_only","download_annotations"]):
      jwt = kwargs['jwt']
      id = kwargs['id']
      output = kwargs['output']
      download_link_only = kwargs['download_link_only']
      download_annotations = kwargs['download_annotations']
      if download_link_only == download_annotations and download_link_only in [True,"True"]:
          print("""
          download_link_only and download_annotations cannot both be True
          """)
          return
    else:
      print("""
        To use download_annotations(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        download_annotations flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function. If the download_link_only boolean is set to True, then only 
        the assembly download link is retrieved. If the download_annotations boolean is
        set to True, then only the assembly download link is retrieved.
        E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="output.txt",download_link_only="True",download_annotations="False") print annotation data url to file
        E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="return",download_link_only="False",download_annotations="True") return the raw genbank file
        E.g., download_annotations(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="return",download_link_only="False",download_annotations="False") return the raw json result
      """)
      return 
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if download_link_only == True or download_link_only == "True":
      if output == 'return':
        return data['url']
      else:
        with open(output,'w') as out:
          out.write(data['url'])
    elif download_annotations == True or download_annotations == "True":
        annotations = os.popen(f"curl \"{data['url']}\"").read()
        if output == 'return':
          return annotations
        else:
          with open(output,'w') as out:
            out.write(annotations)
    else:
      if output == 'return':
        return data
      else:
        with open(output,'w') as out:
          out.write(json.dumps(data,indent=1))

def download_metadata(**kwargs):
    if set(kwargs.keys()) == set(["jwt","id","output"]):
      jwt = kwargs['jwt']
      id = kwargs['id']
      output = kwargs['output']
    else:
      print("""
        To use download_metadata(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        print_out_results flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function. If the download_link_only boolean is set to True, then only 
        the assembly download link is retrieved. If the print_out_results boolean is
        set to True, then only the assembly download link is retrieved.
        E.g., download_metadata(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="output.txt") print metadata to file
        E.g., download_metadata(jwt=YOUR_JWT,id=304fd1fb9a4e48ee,output="return") return metadata
      """)
      return 
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if output == 'return':
      return data
    else:
      with open(output,'w') as out:
        out.write(json.dumps(data,indent=1))

def download_all_genomes(*args):
    if set(kwargs.keys()) == set(["jwt","page","output"]):
      jwt = kwargs['jwt']
      page = kwargs['page']
      output = kwargs['output']
    else:
      print("""
        To use download_all_genomes(), you must include your jwt, a page number, 
        and your desired output. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function.
        E.g., download_all_genomes(jwt=YOUR_JWT,page=1,output="output.txt") print page 1 of metadata to file
        E.g., download_all_genomes(jwt=YOUR_JWT,page=2,output="return") return page 2 of metadata
      """)
      return 
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if output == 'return':
      return data
    else:
      with open(output,'a') as out:
        out.write(json.dumps(data,indent=1))


### Create test function