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

if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters, see usage in script"
    exit 1
fi

# read arguments
n_bits=$1 # length of codeword (n)
n_checks=$2 # set according to the desired rate (this is n-k) - number of parity bits
n_ones_column=$3 # should generally set to 3
message_length=$((n_bits - n_checks)) # length of a message before encoding
n_blocks=$4 # number of messages
channel=$5 # bsc, awgn
channel_value=$6 # corresponding error probability


# create temporary directory
tempdir=$(mktemp -d)
tempres=$tempdir/tempres

mkdir $tempdir/message
mkdir $tempdir/tempres


echo "----- creating message"
./LDPC-codes/rand-src $tempdir/message/message 0 "${message_length}x${n_blocks}"


test_construction () {
	construction=$1

	echo "----- testing: ${construction} construction"

	# create a parity check equation
	python3 ./LDPC-library/make-pchk.py --output-pchk $tempres/pchk --code-type regular --construction $construction --n-checks $n_checks --n-bits $n_bits --checks-per-col $n_ones_column > /dev/null 2>&1

	# create a generator matrix
	./LDPC-codes/make-gen $tempres/pchk $tempres/genfile sparse > /dev/null 2>&1

	# encode message according to this code
	python3 ./LDPC-library/encode.py --pchk-file $tempres/pchk --gen-file $tempres/genfile --input-file $tempdir/message/message --output-file $tempres/encoded > /dev/null 2>&1

	# introduce corruption
	./LDPC-codes/transmit $tempres/encoded $tempres/received 0 $channel $channel_value > /dev/null 2>&1

	# display difference between encoded and corrupted
	difference=`cmp -l $tempres/encoded $tempres/received| wc -l`
	echo -n "percent difference before decoding: "
	echo $difference/$n_bits/$n_blocks|bc -l

	# decode corrupted message
	python3 ./LDPC-library/decode.py --pchk-file $tempres/pchk --received-file $tempres/received --output-file $tempres/decoded --channel $channel --channel-parameters $channel_value > /dev/null 2>&1

	# display difference between encoded and decoded (the lower this value the better)
	difference=`cmp -l $tempres/encoded $tempres/decoded | wc -l` > /dev/null 2>&1
	echo -n "percent difference after decoding: " 
	echo $difference/$n_bits/$n_blocks|bc -l

	rm -rf $tempres/*
}

# test_construction gallager
# test_construction random
test_construction populate-rows
test_construction populate-columns

# Delete temporary directory
rm -rf $tempdir
