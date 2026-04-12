import pathlib
import re
import subprocess

DATA = pathlib.Path('./test')

def jsonparser_output(json_file):
    out = subprocess.check_output(['./bin/bplc.out', json_file])
    return out.decode().strip()

def check_jsonchecker_fail_syntaxonly():
    data = DATA
    for bplfile in data.glob('*.bpl'):
        out = jsonparser_output(bplfile)
        print(f'For file {bplfile.name}:')
        print(out)
        print('='*60)
        subfolder_name = "test"
        temp=bplfile.name[0:10]
        file_name = f"./{subfolder_name}/"+temp+".out"
        with open(file_name, 'w') as file:
            file.write(out)

# check_jsonchecker_fail_withlexical()
check_jsonchecker_fail_syntaxonly()
