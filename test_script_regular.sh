#!/bin/bash

if [ "$#" -ne 7 ]; then
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
channel_value=$6 # corresponding error probability/standard deviation
seed=$7 # seed for reproducibility

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
  python3 ./LDPC-library/make-pchk.py --output-pchk-file $tempres/pchk \
                                      --code-type regular \
                                      --construction $construction \
                                      --n-checks $n_checks \
                                      --n-bits $n_bits \
                                      --checks-per-col $n_ones_column \
                                      --seed $seed

  # create a generator matrix
  ./LDPC-codes/make-gen $tempres/pchk $tempres/genfile sparse

  # encode message according to this code
  python3 ./LDPC-library/encode.py  --pchk-file $tempres/pchk \
                                    --gen-file $tempres/genfile \
                                    --input-file $tempdir/message/message \
                                    --output-file $tempres/encoded

  # introduce corruption
  ./LDPC-codes/transmit $tempres/encoded $tempres/received $seed $channel $channel_value

  # decode corrupted message
  python3 ./LDPC-library/decode.py  --pchk-file $tempres/pchk \
                                    --received-file $tempres/received \
                                    --output-file $tempres/decoded \
                                    --channel $channel \
                                    --channel-parameters $channel_value
  echo ""
  echo "------------------------------------------------------------------------"
  echo "------------------------------------------------------------------------"
  echo "${construction} construction"
  echo "percent difference after decoding: "
  python3 compute_error_rate.py $tempres/encoded $tempres/decoded
  echo "------------------------------------------------------------------------"
  echo "------------------------------------------------------------------------"
  echo ""

  rm -rf $tempres/*
}

test_construction peg
test_construction gallager
test_construction populate-rows
test_construction populate-columns

# Delete temporary directory
rm -rf $tempdir
