import subprocess
import sys
import os
import shutil

# arguments: pchk-directory, gen-file, source-file, encoded-path

pchk_dir = sys.argv[1]
pchk_file = os.path.join(pchk_dir, os.path.basename(pchk_dir))
transmitted_bits = os.path.join(pchk_dir, '.transmitted')

gen_file = sys.argv[2]
src_file = sys.argv[3]
out_path = sys.argv[4]

if len(sys.argv) != 6:
    print("incorrect number of arguments for encoding")
    exit()

# if a directory already exists at this path, delete it
if os.path.isdir(out_path):
    delete = input("a directory exists at this location, replace? [y/n]: ")
    if delete == 'y':
        shutil.rmtree(out_path)
    else:
        exit()

# create ldpc directory
try:
    os.mkdir(out_path)
except FileExistsError:
    print("a directory already exists at the specified location")
    exit()

os.system('../LDPC-codes/encode ' + pchk_file + ' ' + gen_file +
          ' ' + src_file + ' ' + os.path.join(out_path, os.path.basename(out_path)))
