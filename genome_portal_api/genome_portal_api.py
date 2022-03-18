import os
import argparse
from argparse import RawTextHelpFormatter
import json

def search_product(jwt,product_id,output,id_only):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += " -d \'{" + "\"product_id\"" + ": \"" + product_id + "\"}\' https://genomes.atcc.org/api/genomes/search"
    result = os.popen(cmd).read()
    if id_only:
        data = json.loads(result)
        if output == '-':
            print(data[0]['id'])
        else:
            with open(output,'w') as out:
                out.write(data[0]['id'])
    else:
        if output == '-':
          print(json.dumps(json.loads(result),indent=1))
        else:
          with open(output,'w') as out:
            out.write(json.dumps(json.loads(result),indent=1))

def search_text(jwt,text,output,id_only):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += " -d \'{" + "\"text\"" + ": \"" + text + "\"}\' https://genomes.atcc.org/api/genomes/search"
    result = os.popen(cmd).read()
    if id_only:
        data = json.loads(result)
        if output == '-':
            print(data[0]['id'])
        else:
            with open(output,'w') as out:
                out.write(data[0]['id'])
    else:
        if output == '-':
          print(json.dumps(json.loads(result),indent=1))
        else:
          with open(output,'w') as out:
            out.write(json.dumps(json.loads(result),indent=1))


def download_assembly(jwt,id,output,download_link_only,print_out_results):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_assembly"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if download_link_only:
      if output == '-':
        print(data['url'])
      else:
        with open(output,'w') as out:
          out.write(data['url'])
    elif print_out_results:
      assembly = os.popen(f"curl \"{data['url']}\"").read()
      if output == '-':
        print(assembly)
      else:
        with open(output,'w') as out:
          out.write(assembly)
    else:
        print(json.dumps(data,indent=1))

def download_annotations(jwt,id,output,download_link_only,print_out_results):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}/download_annotations"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if download_link_only:
      if output == '-':
        print(data['url'])
      else:
        with open(output,'w') as out:
          out.write(data['url'])
    elif print_out_results:
        annotations = os.popen(f"curl \"{data['url']}\"").read()
        if output == '-':
          print(annotations)
        else:
          with open(output,'w') as out:
            out.write(annotations)
    else:
      if output == '-':
        print(json.dumps(data,indent=1))
      else:
        with open(output,'w') as out:
          out.write(json.dumps(data,indent=1))

def download_metadata(jwt,id,output):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes/{id}"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if output == '-':
      print(json.dumps(data,indent=1))
    else:
      with open(output,'w') as out:
        out.write(json.dumps(data,indent=1))

def download_all_genomes(jwt,page,output):
    cmd = f"curl --insecure --header \'Content-Type: Application/json\' --header \"Authorization: Bearer {jwt}\""
    cmd += f" https://genomes.atcc.org/api/genomes?page={page}"
    result = os.popen(cmd).read()
    data = json.loads(result)
    if output == '-':
      print(json.dumps(data,indent=1))
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
    parser.add_argument('-o', metavar='text',default='-',type=str, nargs='?', required=False, help='The output file location')
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
                search_product(args.j,args.p,args.o)
        elif len(args.t) > 0:
            if args.id_only:
                search_text(args.j,args.t,args.o,args.id_only)
            else:
                search_text(args.j,args.t,args.o)
        else:
            print(' Program to search for genomes using the OneCodex api. \
            \n You must include either a product id or text string to search for. \
            \n usage: python oc_api.py -m search -j [JWT] -p [product id] -t [text] ')
    elif args.m == 'download_assembly':
        if len(args.i) > 0:
            if args.download_link_only and args.print_out_results:
                print('You may select only one of download_link_only or print_out_results.')
            elif args.download_link_only:
                download_assembly(args.j,args.i,args.o,args.download_link_only)
            elif args.print_out_results:
                download_assembly(args.j,args.i,args.o,args.print_out_results)
            else:
                download_assembly(args.j,args.i,args.o)
        else:
            print(' Program to download a genome assembly using the OneCodex api. \
            \n You must include a genome id, e.g., 304fd1fb9a4e48ee. \
            \n usage: python oc_api.py -m download_assembly -j [JWT] -i [genome id]')
    elif args.m == 'download_annotations':
        if len(args.i) > 0:
            if args.download_link_only and args.print_out_results:
                print('You may select only one of download_link_only or print_out_results.')
            elif args.download_link_only:
                download_annotations(args.j,args.i,args.o,args.download_link_only)
            elif args.print_out_results:
                download_annotations(args.j,args.i,args.o,args.print_out_results)
            else:
                download_annotations(args.j,args.i,args.o)
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
