import subprocess
import sys

# arguments: pchk-file, gen-file, source-file, encoded-file, will-puncture

pchk_file = sys.argv[1]
gen_file = sys.argv[2]
src_file = sys.argv[3]
out_file = sys.argv[4]
puncture = bool(sys.argv[5])

if len(sys.argv) != 6:
    print("incorrect number of arguments for encoding")
    exit()
