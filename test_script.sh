#!/bin/bash

# Process:
#
# create ldpc matrices (width, height)
# - create using both personal implementation and library implementation
#
# transmit all-zeros codewords through BSC
#
# decode default message with prprp max 100
#
# print error rate (block error rate and bit error rate)
#
# arguments:
# parity-check-width (codeword length), parity-check-height (number of checks),
# 1s per col, error rate, numblocks, number of LDPC iterations
#
# implied:
# library ldpc construction: evenboth
# corruption: binary symmetric

if [ "$#" -ne 7 ]; then
    echo "Illegal number of parameters, see usage in script"
    exit 1
fi

# read arguments
n_bits=$1 # length of codeword (n)
n_checks=$2 # set according to the desired rate (this is n-k)
n_ones_column=$3 # should generally set to 3
error_rate=$4 # BSC error rate
n_blocks=$5 # number of blocks to get estimate of bit/block error rate
n_iterations=$6 # number of LDPC iterations in prprp decoding
protograph_file=$7

clear

# create temporary directory
tempdir=$(mktemp -d)

echo "----------------------------------------------------------------------------------------------------"
echo "------------------------------------ TRANSMITTING MESSAGE ------------------------------------------"
echo "----------------------------------------------------------------------------------------------------"

echo "temporary directory $tempdir"

echo "transmitting all-zero codeword with error probability ${4}..."
./LDPC-codes/transmit $n_bits"x"$n_blocks $tempdir/received 1 bsc $error_rate
echo ""

echo "computing block error rate and bit error rate (at codeword level) for recieved message before decoding"
python3 -u compute_error_rate.py $tempdir/received
echo ""

echo "----------------------------------------------------------------------------------------------------"
echo "------------------------------------- REGULAR CODE TESTS -------------------------------------------"
echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through default implementation..."
./LDPC-codes/make-ldpc $tempdir/default.pchk ${n_checks} ${n_bits} 1 evenboth ${n_ones_column}
echo ""

echo "decoding transmission for library generated parity matrix..."
./LDPC-codes/decode $tempdir/default.pchk $tempdir/received $tempdir/default.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for library generated parity matrix"
python3 -u compute_error_rate.py $tempdir/default.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through python (Gallagher construction)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk regular gallagher ${1} ${2} ${3}
echo ""

echo "decoding transmission for python generated parity matrix (Gallagher construction)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (Gallager construction)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through python (evenboth construction populate rows)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk regular populate-rows ${1} ${2} ${3}
echo ""

echo "decoding transmission for python generated parity matrix (evenboth construction populate rows)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (evenboth construction populate columns)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through python (evenboth construction populate columns)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk regular populate-columns ${1} ${2} ${3}
echo ""

echo "decoding transmission for python generated parity matrix (evenboth construction populate populate columns)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (evenboth construction populate columns)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through python (evenboth construction populate rows row col weights inferred)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk regular populate-rows ${1} ${2}
echo ""

echo "decoding transmission for python generated parity matrix (evenboth construction populate rows)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (evenboth construction populate columns)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating parity check matrix through python (evenboth construction populate columns row col weights inferred)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk regular populate-columns ${1} ${2}
echo ""

echo "decoding transmission for python generated parity matrix (evenboth construction populate populate columns)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (evenboth construction populate columns)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"
echo "------------------------------------ PROTOGRAPH CODE TESTS -----------------------------------------"
echo "----------------------------------------------------------------------------------------------------"

echo "generating protograph parity check matrix through python (regular construction)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk protograph regular ./protographs/${7} ${1}
echo ""

echo "decoding transmission for python generated parity matrix (regular construction)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (permutation construction)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating protograph parity check matrix through python (quasi-cyclic construction)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk protograph quasi-cyclic ./protographs/${7} ${1}
echo ""

echo "decoding transmission for python generated parity matrix (quasi-cyclic construction)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (permutation construction)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

echo "----------------------------------------------------------------------------------------------------"

echo "generating protograph parity check matrix through python (permuted-quasi-cyclic construction)..."
python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk protograph permuted-quasi-cyclic ./protographs/${7} ${1}
echo ""

echo "decoding transmission for python generated parity matrix (permuted-quasi-cyclic construction)..."
./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
echo ""

echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (permutation construction)"
python3 -u compute_error_rate.py $tempdir/python.decoded
echo ""

# echo "----------------------------------------------------------------------------------------------------"

# echo "generating protograph parity check matrix through python (permutation construction)..."
# python3 ./LDPC-TannerGraphs/Exec.py $tempdir/python.pchk protograph permutation ./protographs/${7} ${1}
# echo ""

# echo "decoding transmission for python generated parity matrix (permutation construction)..."
# ./LDPC-codes/decode $tempdir/python.pchk $tempdir/received $tempdir/python.decoded bsc $error_rate prprp $n_iterations
# echo ""

# echo "computing block error rate and bit error rate (at codeword level) for python generated parity matrix (permutation construction)"
# python3 -u compute_error_rate.py $tempdir/python.decoded
# echo ""




# Delete temporary directory
rm -rf $tempdir
