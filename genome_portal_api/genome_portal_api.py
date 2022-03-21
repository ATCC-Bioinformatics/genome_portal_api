import os
import argparse
from argparse import RawTextHelpFormatter
import json
def search_product(*args):
    if len(args) == 4:
      jwt,product_id,output,id_only = args 
    else:
      print("""
        To use search_product(), you must include your jwt, a product_id, 
        your desired output, and a boolean id_only flag. The output may be
        a file path, such as path/to/file.txt, or the string "return" which
        returns the output from the function. If the id_only boolean is set 
        to True, then only the assembly id is retrieved.
        E.g., search_product(YOUR_JWT,35638,"output.txt","False") print resulting
        metadata to file
        E.g., x = search_product(YOUR_JWT,35638,"return","True") return only the assembly id
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

def search_text(*args):
    if len(args) == 4:
      jwt,text,output,id_only = args 
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


def download_assembly(*args):
    if len(args) == 5:
      jwt,id,output,download_link_only,print_out_results = args 
      if download_link_only == print_out_results and download_link_only in [True,"True"]:
        print("""
        download_link_only and print_out_results cannot both be True or False
        """)
        return
    else:
      print("""
        To use download_assembly(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        print_out_results flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function. If the download_link_only boolean is set to True, then only 
        the assembly download link is retrieved. If the print_out_results boolean is set to True,
        then only the assembly download link is retrieved.
        E.g., download_assembly(YOUR_JWT,304fd1fb9a4e48ee,"output.txt","True","False") print assembly url to file
        E.g., download_assembly(YOUR_JWT,304fd1fb9a4e48ee,"return","False","True") return assembly dict 
        E.g., download_assembly(YOUR_JWT,304fd1fb9a4e48ee,"return","False","False") return raw json result
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
    elif print_out_results == True or print_out_results == "True":
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

def download_annotations(*args):
    if len(args) == 5:
      jwt,id,output,download_link_only,print_out_results = args 
      if download_link_only == print_out_results and download_link_only in [True,"True"]:
        print("""
        download_link_only and print_out_results cannot both be True
        """)
        return
    else:
      print("""
        To use download_annotations(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        print_out_results flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function.
        E.g., download_annotations(YOUR_JWT,304fd1fb9a4e48ee,"output.txt","True","False") print annotation data url to file
        E.g., download_annotations(YOUR_JWT,304fd1fb9a4e48ee,"return","False","True") return the raw genbank file
        E.g., download_annotations(YOUR_JWT,304fd1fb9a4e48ee,"return","False","False") return the raw json result
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
    elif print_out_results == True or print_out_results == "True":
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

def download_metadata(*args):
    if len(args) == 3:
      jwt,id,output = args 
    else:
      print("""
        To use download_metadata(), you must include your jwt, an assembly ID, 
        your desired output, a boolean download_link_only flag, and a boolean 
        print_out_results flag. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function.
        E.g., download_metadata(YOUR_JWT,304fd1fb9a4e48ee,"output.txt") print metadata to file
        E.g., download_metadata(YOUR_JWT,304fd1fb9a4e48ee,"return") return metadata
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
    if len(args) == 3:
      jwt,page,output = args 
    else:
      print("""
        To use download_all_genomes(), you must include your jwt, a page number, 
        and your desired output. The output may be a file path, such as 
        path/to/file.txt, or the string "return" which returns the output from
        the function.
        E.g., download_all_genomes(YOUR_JWT,1,"output.txt") print page 1 of metadata to file
        E.g., download_all_genomes(YOUR_JWT,2,"return") return page 2 of metadata
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

def main():
    parser = argparse.ArgumentParser(description=' Program to access the OneCodex api. \
    \n Pass in desired mode, e.g., -m search, with no additional arguments to learn how to use \
    \n that specific function \
    \n usage: python oc_api.py -j [JWT] -m [mode] options',
    formatter_class=RawTextHelpFormatter)
    parser.add_argument('-j', metavar='JWT',type=str, nargs='?', required=True, help='The user\'s JWT',default='')
    parser.add_argument('-m', metavar='mode',type=str, nargs='?', required=True, help='An API endpoint: {download_metadata, download_assembly, download_annotations, search, all_genomes}')
    parser.add_argument('-p', metavar='product_id',default='',type=str, nargs='?', required=False, help='The product ID to search for.')
    parser.add_argument('-t', metavar='text',default='',type=str, nargs='?', required=False, help='The text to search for')
    parser.add_argument('-i', metavar='text',default='',type=str, nargs='?', required=False, help='The genome id')
    parser.add_argument('-o', metavar='text',default='return',type=str, nargs='?', required=False, help='The output file location')
    parser.add_argument('--page_number', metavar='text',default=0,type=str, nargs='?', required=False, help='The number of pages you want to download with all_genomes, 50 results per page.\nEnter 0 (default) to download information for all genomes')
    parser.add_argument('--id_only', action='store_true', help='Return only the genome ID.')
    parser.add_argument('--download_link_only', action='store_true', help='Return only the link to download the assembly or annotations.')
    parser.add_argument('--print_out_results', action='store_true', help='Print assembly to standard out.')
    args = parser.parse_args()

    print(u"\u001b[38;5;" + "55;15m" + "By using this code, you agree to ATCC's End User License Agreement:\nhttps://www.atcc.org/policies/product-use-policies/data-use-agreement\n" + "\u001b[0m")

    if args.m == 'search':
        if len(args.p) > 0:
            if args.id_only:
                search_product(args.j,args.p,args.o,args.id_only)
            else:
                search_product(args.j,args.p,args.o,False)
        elif len(args.t) > 0:
            if args.id_only:
                search_text(args.j,args.t,args.o,args.id_only)
            else:
                search_text(args.j,args.t,args.o,False)
        else:
            print(' Program to search for genomes using the OneCodex api. \
            \n You must include either a product id or text string to search for. \
            \n usage: python oc_api.py -m search -j [JWT] -p [product id] -t [text] ')
    elif args.m == 'download_assembly':
        if len(args.i) > 0:
            if args.download_link_only and args.print_out_results:
                print('You may select only one of download_link_only or print_out_results.')
            elif args.download_link_only:
                download_assembly(args.j,args.i,args.o,args.download_link_only,False)
            elif args.print_out_results:
                download_assembly(args.j,args.i,args.o,False,args.print_out_results)
            else:
                download_assembly(args.j,args.i,args.o,False,False)
        else:
            print(' Program to download a genome assembly using the OneCodex api. \
            \n You must include a genome id, e.g., 304fd1fb9a4e48ee. \
            \n usage: python oc_api.py -m download_assembly -j [JWT] -i [genome id]')
    elif args.m == 'download_annotations':
        if len(args.i) > 0:
            if args.download_link_only and args.print_out_results:
                print('You may select only one of download_link_only or print_out_results.')
            elif args.download_link_only:
                download_annotations(args.j,args.i,args.o,args.download_link_only,False)
            elif args.print_out_results:
                download_annotations(args.j,args.i,args.o,False,args.print_out_results)
            else:
                download_annotations(args.j,args.i,args.o,False,False)
        else:
            print(' Program to download a genome\'s annotations using the OneCodex api. \
            \n You must include a genome id, e.g., 304fd1fb9a4e48ee. \
            \n usage: python oc_api.py -m download_assembly -j [JWT] -i [genome id]')
    elif args.m == 'download_metadata':
        if len(args.i) > 0:
            download_metadata(args.j,args.i,args.o)
        else:
            print(' Program to download a genome\'s metadata using the OneCodex api. \
            \n You must include a genome id, e.g., 304fd1fb9a4e48ee. \
            \n usage: python oc_api.py -m download_metadata -j [JWT] -i [genome id]')
    elif args.m == 'all_genomes':
        if args.page_number == 0:
          for page_number in range(0,100):
              download_all_genomes(args.j, page_number,args.o)
        elif len(args.page_number) > 0:
            for page_number in range(0,int(args.page_number)):
              download_all_genomes(args.j,page_number,args.o)
        else:
            print(' Program to download metadata for all genome assemblies using the OneCodex api. \
            \n You must include a genome id, e.g., 304fd1fb9a4e48ee. \
            \n usage: python oc_api.py -m all_genomes -j [JWT] -i [genome id]')

if __name__ == "__main__":
    main()
