#!/bin/bash

# args: protograph-file factor message-length num-blocks channel channel-value unpunctured-block-length

#
# create a message
#
# for all protograph construction methods:
#
# create a parity check file
# create a generator matrix file
#
# encode message
# transmit encoded message with specified corruption
#
# cmp decoded encoded



if [ "$#" -ne 7 ]; then
    echo "Illegal number of parameters, see usage in script"
    exit 1
fi

# read arguments
protograph_file=$1
expansion_factor=$2
message_length=$3
n_blocks=$4
channel=$5
channel_value=$6
seed=$7

# create temporary directory
tempdir=$(mktemp -d)
tempres=$tempdir/tempres

mkdir $tempdir/message
mkdir $tempdir/tempres

echo "----- creating message"
./LDPC-codes/rand-src $tempdir/message/message $seed "${message_length}x${n_blocks}"

test_construction () {
	construction=$1

	echo "----- testing: ${construction} construction"

	# create a parity check equation
	python3 ./LDPC-library/make-pchk.py --output-pchk $tempres/pchk --code-type protograph --construction $construction --protograph-file $protograph_file --expansion-factor $expansion_factor --seed $seed > /dev/null 2>&1

	# create a generator matrix
	./LDPC-codes/make-gen $tempres/pchk $tempres/genfile sparse > /dev/null 2>&1

	# encode message according to this code
	python3 ./LDPC-library/encode.py --pchk-file $tempres/pchk --gen-file $tempres/genfile --input-file $tempdir/message/message --output-file $tempres/encoded > /dev/null 2>&1

	# introduce corruption
	./LDPC-codes/transmit $tempres/encoded $tempres/received $seed $channel $channel_value > /dev/null 2>&1

	# decode corrupted message
	python3 ./LDPC-library/decode.py --pchk-file $tempres/pchk --received-file $tempres/received --output-file $tempres/decoded --channel $channel --channel-parameters $channel_value > /dev/null 2>&1

	echo -n "percent difference after decoding: "
	python3 compute_error_rate.py $tempres/encoded $tempres/decoded

	rm -rf $tempres/*
}

test_construction quasi-cyclic
test_construction permuted-quasi-cyclic
test_construction permutation
test_construction regular


# Delete temporary directory
rm -rf $tempdir
