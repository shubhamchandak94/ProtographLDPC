import subprocess
import sys
import os
import shutil

# arguments: pchk-directory, gen-file, source-file, encoded-path

pchk_dir = sys.argv[1]
pchk_file = os.path.join(pchk_dir, os.path.basename(pchk_dir))
transmitted_bits_filepath = os.path.join(pchk_dir, '.transmitted')

gen_file = sys.argv[2]
src_file = sys.argv[3]
out_path = sys.argv[4]

if len(sys.argv) != 5:
    print("incorrect number of arguments for encoding")
    exit()

# if a directory already exists at this path, delete it
if os.path.isdir(out_path):
    delete = input("a directory exists at the specified encoded location, replace? [y/n]: ")
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

if len(os.listdir(pchk_dir)) == 2:

    codewords = open(os.path.join(out_path, os.path.basename(out_path)), 'r').read().split('\n')
    codewords = codewords[:len(codewords) - 1]

    transmitted_bits = [int(i) for i in open(transmitted_bits_filepath, 'r').read().split('\n')[2].split(' ')]

    punctured_codewords = []
    for code in codewords:
        punctured_codeword = ""
        for i in range(len(code)):
            if i in transmitted_bits:
                punctured_codeword += code[i]
        punctured_codewords.append(punctured_codeword)

    open(os.path.join(out_path, os.path.basename(out_path)), 'w').write('\n'.join(punctured_codewords))
    open(os.path.join(out_path, '.preserved'), 'w').write('\n'.join(codewords))
