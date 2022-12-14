from cPARSER import *
import json
source_files_list = ['bubbletest.c']

dest_code = ''
for file in source_files_list:
    with open(file, 'r') as f:
        src_code = f.read()
        ast = yacc.parse(src_code)
        # print(dict.printtree())
    
file ='AST.json'
out_file = open(file, "w")
json.dump(ast.printtree(), out_file, indent= 2)
out_file.close()

  