---
layout: default
title: Examples
nav_order: 3
parent: Overview
---

# Examples
On this page we discuss a simple example illustrating the generation and application of LDPC codes using this library. You can also see the [Simulations](simulations.html) page and the [test scripts](usage.html#test-scripts.html) for more examples. For some of the commands in the example, we rely on the base library which is documented [here](https://shubhamchandak94.github.io/LDPC-codes/). Throughout the example we use a seed value of 43 to allow reproducibility.

## Table of Contents
* [Parity check matrix generation](#parity-check-matrix-generation)
* [Generator matrix creation](#generator-matrix-creation)
* [Generating random source](#generating-random-source)
* [Encoding](#encoding)
* [Simulating transmission over a BSC](#simulating-transmission-over-a-bsc)
* [Decoding](#decoding)
* [Extract message bits](#extract-message-bits)

## Parity check matrix generation

We discuss generation of a regular and a protograph code of rate 2/3 and block length 3000 bits.

### Regular code:
We generate a regular code with block length 3000 and rate 2/3. The number of message bits can be determined from the rate as 2000 and hence the number of check bits is 1000. We set the number of 1s per column to 3 and use the default `peg` construction method.

```sh
python LDPC-library/make-pchk.py --output-pchk-file myCode.pchk \
                                 --code-type regular \
                                 --n-checks 1000 \
                                 --n-bits 3000 \
                                 --checks-per-col 3 \
                                 --seed 43
```
The file `myCode.pchk` contains the parity check matrix.

### Regular code with puncturing:
Here we first generate a rate 1/2 regular code with block length 4000 and then puncture it to get the desired parameters. The number of message bits is still 2000, and the number check bits is now 2000 (4000-2000). We need to transmit 75% of the bits so that the final block length becomes 3000 and the code rate becomes 2/3.
```sh
python LDPC-library/make-pchk.py --output-pchk-file myCode.pchk \
                                 --code-type regular \
                                 --n-checks 1000 \
                                 --n-bits 3000 \
                                 --checks-per-col 3 \
                                 --fraction-transmitted 0.75 \
                                 --seed 43
```
The file `myCode.pchk` contains the parity check matrix and the file `myCode.pchk.transmitted` contains the list of transmitted bits in the block of 4000 bits (chosen randomly).


### Protograph code (AR4JA):
We now generate a code with the rate 2/3 AR4JA protograph. To calculate the expansion factor, we look at the header of the protograph file [sample-protographs/ar4ja_n_1_rate_2_3](https://github.com/shubhamchandak94/ProtographLDPC/blob/master/sample-protographs/ar4ja_n_1_rate_2_3).

```
3 7
transmitted_bits 1 2 3 4 6 7
```

This shows that the protograph has 3 check nodes, 7 variable nodes, and 6 transmitted variable nodes. Thus we need an expansion factor of 500 to obtain the desired block length of 3000. We use the default `peg` construction.

```sh
python LDPC-library/make-pchk.py --output-pchk-file myCode.pchk \
                                 --code-type protograph \
                                 --protograph-file sample-protographs/ar4ja_n_1_rate_2_3 \
                                 --expansion-factor 500 \
                                 --seed 43
```

The file `myCode.pchk` contains the parity check matrix and the file `myCode.pchk.transmitted` contains the list of transmitted bits in the block of 3500 bits (chosen based on the protograph structure).

## Generator matrix creation
We now create the generator matrix from the parity check matrix. We use the base library tool [`make-gen`](https://shubhamchandak94.github.io/LDPC-codes/encoding.html#make-gen) with the sparse construction method for this purpose.
```sh
./LDPC-codes/make-gen myCode.pchk myCode.gen sparse
```
The generator matrix is stored in the file `myCode.gen`.

## Generating random source
Since we do not have actual data to transmit, we will generate some random data using the base library [`rand-src`](https://shubhamchandak94.github.io/LDPC-codes/support.html#rand-src) tool. We will generate 100 blocks to be encoded, each with length 2000 bits (which is the message length for our code).
```sh
./LDPC-codes/rand-src myMessage.txt 43 2000x100
```
The random message blocks are generated and stored in the file `myMessage.txt`, which is human-readable and contains sequences of 0s and 1s with one block per line.

## Encoding
Now we encode the random source generated above using the code. This automatically performs the puncturing (if applicable) and provides the final encoded codewords of length 3000 (total 100 blocks).


```sh
python LDPC-library/encode.py --pchk-file myCode.pchk \
                              --gen-file myCode.gen \
                              --input-file myMessage.txt \
                              --output-file myCodewords.txt
```

The encoded codewords is present in the file `myCodewords.txt`, which is human-readable and contains sequences of 0s and 1s with one block per line.

## Simulating transmission over a BSC
For the purposes of this example, we simulate errors in the transmission using the base library [`transmit`](https://shubhamchandak94.github.io/LDPC-codes/channel.html#transmit). We use a binary symmetric channel (BSC) with error probability `0.01`.

```sh
./LDPC-codes/transmit myCodewords.txt myReceived.txt 43 bsc 0.01
```
The received blocks are present in the file `myReceived.txt`, which is human-readable and contains sequences of 0s and 1s with one block per line.

## Decoding
Now we perform the decoding by providing the channel parameters to the decoding script. This automatically handles the puncturing (if applicable) and provides the final decoded codewords of length 3000 (total 100 blocks).
```sh
python LDPC-library/decode.py --pchk-file myCode.pchk \
                              --received-file myReceived.txt \
                              --output-file myDecoded.txt
                              --channel bsc
                              --channel-parameters 0.01
```

This writes the decoded codewords to the file `myDecoded.txt`, which has a similar format as `myCodewords.txt`. Note that the encoding and decoding scripts also produce a `.unpunctured` file when puncturing is being used (e.g., `myDecoded.txt.unpunctured` in this case). This file contains all the codeword bits including the punctured bits and allows interaction with the base library that is unaware of the puncturing.

## Extract message bits
Finally we attempt to extract the message bits from the decoded codewords. We will rely on the base library [`extract`](https://shubhamchandak94.github.io/LDPC-codes/decoding.html#extract) tool, and as mentioned above this requires access to the unpunctured decoded codewords. Therefore, we use the following command when puncturing is in use
```sh
./LDPC-codes/extract myCode.gen myDecoded.txt.unpunctured myExtracted.txt
```
and the following when puncturing is not in use
```sh
./LDPC-codes/extract myCode.gen myDecoded.txt myExtracted.txt
```
The final output message bits are in the file `myExtracted.txt` which has a similar format as the `myMessage.txt` file.
