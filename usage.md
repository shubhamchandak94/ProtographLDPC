---
layout: default
title: Usage
nav_order: 2
parent: Overview
---

# Usage
This page contains the usage of the various scripts in the library. The [Examples](examples.html) page can be helpful to further understand the usage. We refer throughout to tools in the base library documented [here](https://shubhamchandak94.github.io/LDPC-codes/).

Scripts:
* [make-pchk.py](#make-pchkpy)
* [encode.py](#encodepy)
* [decode.py](#decodepy)
* [Test scripts](#test-scripts)
  * [test_script_regular.sh](#test_script_regularsh)
  * [test_script_protograph.sh](#test_script_protographsh)

## make-pchk.py
Generates a regular or protograph parity check matrix.

**General usage:**
```sh
python LDPC-library/make-pchk.py [-h] --output-pchk-file PCHK_FILE --code-type
                    {regular,protograph} [--construction CONSTRUCTION]
                    [--n-checks N_CHECKS] [--n-bits N_BITS]
                    [--checks-per-col CHECKS_PER_COL]
                    [--fraction-transmitted FRACTION_TRANSMITTED]
                    [--protograph-file PROTOGRAPH_FILE]
                    [--expansion-factor EXPANSION_FACTOR] [--seed SEED]

optional arguments:
  -h, --help            show this help message and exit
  --output-pchk-file PCHK_FILE, -o PCHK_FILE
                        File to store generated pchk file. An additional
                        .transmitted file is also generated when puncturing is
                        used. For example, when this argument is my.pchk, then
                        my.pchk.transmitted will also be generated when
                        puncturing is used.
  --code-type {regular,protograph}, -t {regular,protograph}
                        Type of LDPC code to construct.
  --construction CONSTRUCTION, -c CONSTRUCTION
                        Method used for code construction (default peg). Other
                        options: regular: {gallager,populate-rows,populate-
                        columns}. protograph: {sum-permutations,quasi-
                        cyclic,permuted-quasi-cyclic}.
  --n-checks N_CHECKS   For regular codes: number of check nodes.
  --n-bits N_BITS       For regular codes: number of codeword bits (including
                        untransmitted/punctured bits).
  --checks-per-col CHECKS_PER_COL
                        For regular codes: number of 1s per column of parity
                        check matrix. [default: 3]
  --fraction-transmitted FRACTION_TRANSMITTED, -f FRACTION_TRANSMITTED
                        For regular codes: fraction of bits out of n-bits to
                        transmit (randomly chosen). [default: 1.0]
  --protograph-file PROTOGRAPH_FILE, -p PROTOGRAPH_FILE
                        For protograph codes: file containing protograph.
  --expansion-factor EXPANSION_FACTOR, -e EXPANSION_FACTOR
                        For protograph codes: protograph expansion factor.
  --seed SEED, -s SEED  Random seed for reproducibility. [default: 123]
```

For details on the construction methods, see [Methods](methods.html). For details on the protograph file format, see [Sample Protographs](methods-sample-protographs.html).

For regular codes, this reduces to:
```sh
python LDPC-library/make-pchk.py --output-pchk-file PCHK_FILE
                    --code-type regular
                    [--construction CONSTRUCTION]
                    --n-checks N_CHECKS
                    --n-bits N_BITS
                    [--checks-per-col CHECKS_PER_COL]
                    [--fraction-transmitted FRACTION_TRANSMITTED]
                    [--seed SEED]
```
Here, the construction can be one of `peg` (default), `populate-columns`, `populate-rows` or `gallager`. The `--fraction-transmitted` option can be used for random puncturing, by default it is set to `1.0` (no puncturing). We also direct the user to the base library parity check generation script ([`make-ldpc`](https://shubhamchandak94.github.io/LDPC-codes/pchk.html#make-ldpc)) which implements slightly different construction methods but uses a similar interface.

For protograph codes, this reduces to:
```sh
python LDPC-library/make-pchk.py --output-pchk-file PCHK_FILE
                    --code-type protograph
                    [--construction CONSTRUCTION]
                    --protograph-file PROTOGRAPH_FILE
                    --expansion-factor EXPANSION_FACTOR
                    [--seed SEED]
```
Here, the construction can be one of `peg` (default), `sum-permutations`, `quasi-cyclic` or `permuted-quasi-cyclic`.

This script generates a parity check code (`PCHK_FILE`) in a format compatible with the base library. This can be converted from/to the [alist format](http://www.inference.org.uk/mackay/codes/alist.html) using the base library (see [this](https://shubhamchandak94.github.io/LDPC-codes/pchk.html)). Note that the encoding and decoding scripts also work with codes constructed with other libraries as long as the proper format is used. When code puncturing is required, an additional `PCHK_FILE.transmitted` file is created. This human-readable file has the following format (where code-width represents the number of codeword bits before puncturing):
```sh
total bits before transmission: code-width
[space separated list of transmitted bit indices (0-based)]
```

For protograph codes, the transmitted bits are determined from the protograph itself. For regular codes, when using the `--fraction-transmitted` option, the transmitted bits are chosen randomly, and can be modified later according to the user's wishes.

## encode.py
Encodes a message provided a parity check code and a generator matrix. This can be used with any code in the appropriate format, not necessarily generated using this library.

**General usage:**
```sh
python LDPC-library/encode.py [-h] --pchk-file PCHK_FILE --gen-file GEN_FILE --input-file
                 INPUT_FILE --output-file OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --pchk-file PCHK_FILE, -p PCHK_FILE
                        Parity check file. An additional .transmitted file
                        should be present when puncturing is being used. For
                        example, when this argument is my.pchk, then the
                        program will search for my.pchk.transmitted and use it
                        for puncturing if avilable.
  --gen-file GEN_FILE, -g GEN_FILE
                        Generator matrix file. Required for encoding.
  --input-file INPUT_FILE, -i INPUT_FILE
                        Input file containing one or more message blocks (one
                        per line).
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Output file to store encoded blocks (one per line).
```

The generator matrix file can be generated using the base library tool [`make-gen`](https://shubhamchandak94.github.io/LDPC-codes/encoding.html#make-gen). This automatically checks for the `PCHK_FILE.transmitted` file and applies puncturing if this exists. This is simply a wrapper around the base library [`encode`](https://shubhamchandak94.github.io/LDPC-codes/encoding.html#encode) utility, chiefly adding the puncturing capability.

Finally, the [`extract`](https://shubhamchandak94.github.io/LDPC-codes/decoding.html#extract) and [`extract_systematic`](https://shubhamchandak94.github.io/LDPC-codes/support.html#extract_systematic) utilities in the base library can be used to find the positions of and extract the message bits in the codeword.


## decode.py
Decodes a received message using the parity check matrix. This can be used with any code in the appropriate format, not necessarily generated using this library.

General usage:
```sh
python LDPC-library/decode.py [-h] --pchk-file PCHK_FILE --received-file RECEIVED_FILE
                 --output-file OUTPUT_FILE --channel {misc,awgn,bsc}
                 [--channel-parameters CHANNEL_PARAMETERS]
                 [--max-iterations MAX_ITERATIONS]

optional arguments:
  -h, --help            show this help message and exit
  --pchk-file PCHK_FILE, -p PCHK_FILE
                        Parity check file. An additional .transmitted file
                        should be present when puncturing is being used. For
                        example, when this argument is my.pchk, then the
                        program will search for my.pchk.transmitted and use it
                        for puncturing if avilable.
  --received-file RECEIVED_FILE, -i RECEIVED_FILE
                        Received file containing one or more blocks (one per
                        line).
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        Output file to store decoded blocks (one per line).
  --channel {misc,awgn,bsc}
                        Channel for computing LLR. Supported options: binary
                        symmetric channel, additive white gaussian noise
                        channel (modulation: 0 -> -1, 1 -> +1), miscellaneous
                        channel (for general channels, input is LLRs (log-
                        likelihood ratios) as space separated quantities).
  --channel-parameters CHANNEL_PARAMETERS
                        Channel parameters for computing LLR. Required when
                        channel is bsc or awgn. For bsc, this is the bit flip
                        probability. For awgn, this is the standard deviation
                        of the Gaussian noise.
  --max-iterations MAX_ITERATIONS
                        Maximum number of decoding iterations for LDPC belief
                        propagation decoding [default = 100].
```

The channels and channel parameters are discussed in the base library documentation [here](https://shubhamchandak94.github.io/LDPC-codes/channel.html). This automatically checks for the `PCHK_FILE.transmitted` file and applies puncturing if this exists. This is simply a wrapper around the base library [`decode`](https://shubhamchandak94.github.io/LDPC-codes/decoding.html#decode) utility, chiefly adding the puncturing capability. Puncturing is done by converting the received message into log-likelihood ratios (LLRs), inserting an LLR of 0.0 at the punctured positions (to denote erasures). Then we use the `misc` channel in the base library decoder which directly works with LLRs rather than any specific channel model.

The base library provides a [`transmit`](https://shubhamchandak94.github.io/LDPC-codes/channel.html#transmit) function which induces corruption according to a binary-symetric or gaussian noice channel).

Finally, the [`extract`](https://shubhamchandak94.github.io/LDPC-codes/decoding.html#extract) and [`extract_systematic`](https://shubhamchandak94.github.io/LDPC-codes/support.html#extract_systematic) utilities in the base library can be used to find the positions of and extract the message bits in the codeword.


## Test scripts

The test scripts perform a communication roundtrip and print the decoding error rates. We first provide two commands for testing the library and then explain the usage of the scripts in more detail. Also see the [Simulations](simulations.html) page which can be helpful for more comprehensive experimentation.

**Quick test:**
```sh
./test_script_regular.sh 1500 750 3 1000 bsc 0.07 85
./test_script_protograph.sh sample-protographs/ar4ja_n_0_rate_1_2 375 750 1000 bsc 0.07 85
```

The channel can also be set to `awgn` in which case the channel parameter represents the standard deviation of the Gaussian noise. The channels are described in more detail [here](https://shubhamchandak94.github.io/LDPC-codes/channel.html).

### test_script_regular.sh
**General usage:**
```sh
./test_script_regular.sh $n $m $c $n_blocks $channel $channel_param $seed
```
**Sample usage:**
```sh
./test_script_regular.sh 1500 750 3 1000 bsc 0.07 85
```

This tests all the construction methods for a (3,6) regular code with the following parameters:
```
block length (n) = 1500
number of check nodes (m) = 750
number of message bits = m - n = 750
Rate = #message bits/n = 1/2
c = #1s per column (i.e., connections per check node) = 3
#1s per row (i.e., connections per variable node) = n * #1s per column / m = 6
Number of blocks simulated = 1000
Channel = bsc (binary symmetric channel)
Channel parameter (error probability) = 0.07
Seed = 85
```

### test_script_protograph.sh
**General usage:**
```sh
./test_script_protograph.sh $protograph_file $expansion_factor $num_message_bits $n_blocks $channel $channel_param $seed
```

**Sample usage:**

For testing the AR4JA rate 1/2 protograph ([here](https://github.com/shubhamchandak94/ProtographLDPC/blob/master/sample-protographs/ar4ja_n_0_rate_1_2)), we first look at the header of the protograph file:
```
3 5
transmitted_bits 1 2 3 4
```
This tells us that the protograph has 3 check nodes, 5 variable nodes. And 4 out of the 5 variable nodes are actually transmitted. Thus the number of message bits is 5 - 3 = 2, and the rate is 2/4 = 1/2. To get a block length of 1500 as in the regular code example above, the expansion factor of the protograph is 1500/4 = 375. The test script is called below.
```sh
./test_script_protograph.sh sample-protographs/ar4ja_n_0_rate_1_2 375 750 1000 bsc 0.07 85
```
This tests all the construction methods for the code with the following parameters:
```
protograph file = sample-protographs/ar4ja_n_0_rate_1_2
expansion factor = 375
number of message bits = 750
Rate = #message bits/n = 1/2
Number of blocks simulated = 1000
Channel = bsc (binary symmetric channel)
Channel parameter (error probability) = 0.07
Seed = 85
```
