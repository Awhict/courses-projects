import pathlib
import re
import subprocess


DATA = pathlib.Path('./test')


def bplcparser_output(bplc_file):
    out = subprocess.check_output(['./bin/bplc', bplc_file])
    return out.decode().strip()

def check_syntaxonly():
    data = DATA
    for bplfile in data.glob('*.bpl'):
        out = bplcparser_output(bplfile)
        print(f'For file {bplfile.name}:')
        print(out)
        print('#'*80)
        subfolder_name = "test"
        temp=bplfile.name[0:10]
        file_name = f"./{subfolder_name}/"+temp+".out"
        with open(file_name, 'w') as file:
            file.write(out)


check_syntaxonly()
