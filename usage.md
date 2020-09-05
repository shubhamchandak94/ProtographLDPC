---
layout: default
title: Usage
nav_order: 2
parent: Overview
---

# Library Usage
---

The following scripts are included
* [make-pchk](usage.html#make-pchk)
* [encode](usage.html#encode)
* [decode](usage.html#decode)

The encoding script requires prequisite calls to the base library's programs. For reference purposes, you can find the documentation for that library [here](./LDPC-codes/progs.html).

## make-pchk
Creates a regular or protograph parity check matrix
```sh
python3 make-pchk.py --output-pchk pchk-file --code-type {regular, protograph} --construction construction-option build-params
```
```
build-params:
if --code-type == protograph:
    build-params: --protograph-file protograph-file --expansion-factor lift-factor
if --code-type == regular:
    build-params: --n-checks num-rows --n-bits num-cols --ones-per-col ones-per-column [-f percent-transmitted]
```

| code-type |  construction options |
|:-:|-|
| regular | {::nomarkdown}<ul><li>gallager</li><li>random</li><li>populate-rows</li><li>populate-columns</li></ul>{:/} |
| protograph | {::nomarkdown}<ul><li>permutation</li><li>regular</li><li>quasi-cyclic</li><li>permuted-quasi-cyclic</li></ul>{:/} |

This script generates a readable parity check code represented by the following files
```sh
pchk-file
pchk-file.transmitted
```

* the pchk file contains the machine-readable fully constructed LDPC code
* if puncturing is implemented, an additional pchk-file.transmitted file is created containing the necessary meta information for puncturing. If puncturing is not implemented, this file is not created.

the .transmitted file contains the puncturing information
```sh
total bits before transmission: code-width
[space separated list of transmitted bit indices]
```
* Puncturing for protographs is defined within the protograph template passed - the punctured indices are excluded from the list of transmitted bits within the protograph. Y
* Puncturing for regular codes is achieved with the optional -f flag. if this flag is provided, the value passed specifies the proportion of bits to transmit; a .transmitted file is generated accordingly.

If puncturing is implemented, you can mess with the default configuration by altering the index list within the .transmitted file.

## encode
Encodes a message provided a parity check code
```sh
python3 encode.py --pchk-file pchk-file --gen-file gen-file --input-file message-file --output-file encoded-file
```
This script implements a wrapper of the base-library's encode program which requires
the construction of a generator matrix before encoding.

To achieve this, run
```sh
../LDPC-codes/make-gen pchk-file gen-file method
```
```sh
method:
    - sparse
    - dense
    - mixed
```
pchk-file is the file containing the parity check matrix from which to build the generator matrix. If the parity check file was generated using the make-pchk.py script, the pchk file is to be passed not the .transmitted

gen-file is the filepath of the output generator matrix file. <br>
method is the encoding schema for the generator matrix file.

###  In the context of the python encode script:

* pchk-file refers to the parity check matrix file. The local directory will be searched for a .transmitted file as an indicator for puncturing to take place.
* gen-file refers to the path of the generator matrix file corresponding to the specified parity check code.
* message-file refers to the filepath of the message to be encoded as a string of 1s and 0s.
* encoded-file refers to the path of the encoded message.

The contained encoded-file contains the encoded codewords after puncturing, separated by newline characters.

## Decode
Decodes a given message according to the following
```sh
python3 decode.py --pchk-file pchk-file --received-file message-to-decode --output-file decodeed-output --channel {bsc, awgn} --channel-parameters channel-value [--decode-iterations decode-iterations]
```
* pchk-fil is the parity check code. The local directory will be searched for a .transmitted file which would indicate puncturing.
* received-file is the file produced as a result of the encoding, after undergoing some corruption (the base library provides a [transmit](./LDPC-codes/channel.html#transmit) function which induces corruption according to a binary-symetric or gaussian noice channel). the channel and channel-value parameters must match the corruption schema which was induced through the transmission.
* decode-iterations dictates the number of decoding iterations used in the belief propagation decoding. The decode script implements a wrapper of the [decode](./LDPC-codes/decoding.html#decode) function of the base library, and the iteration value is directly passed as an argument to the base decode program.
* decoded-file is the filepath of the output of the decoding. Each decoded message is separated by a newline character

### Test scripts
Run test scripts to verify the library works. More details on the test scripts are available in the documentation [here](https://shubhamchandak94.github.io/ProtographLDPC/usage.html#test-scripts). The test scripts perform a communication roundtrip and print the decoding error rates.
```
./test_script_regular.sh 1500 750 3 1000 bsc 0.07 85
```
This tests all the construction methods for a (3,6) regular code with the following parameters:
```
block length (n) = 1500
number of check nodes (m) = 750
number of message bits = m - n = 750
Rate = #message bits/n = 1/2
#1s per column (i.e., connections per check node) = 3
#1s per row (i.e., connections per variable node) = n * #1s per column / m = 6
Number of blocks simulated = 1000
Channel = bsc (binary symmetric channel)
Channel parameter (error probability) = 0.07
Seed = 85
```

For testing the AR4JA rate 1.2 protograph at [sample-protographs/ar4ja_n_0_rate_1_2](sample-protographs/ar4ja_n_0_rate_1_2), we first look at the header of the protograph file:
```
3 5
transmitted_bits 1 2 3 4
```
This tells us that the protograph has 3 check nodes, 5 variable nodes. And 4 out of the 5 variable nodes are actually transmitted. Thus the number of message bits is 5 - 3 = 2, and the rate is 2/4 = 1/2. To get a block length of 1500 as in the regular code example above, the expansion factor of the protograph is 1500/4 = 375. The tesst script is called below.
```
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
