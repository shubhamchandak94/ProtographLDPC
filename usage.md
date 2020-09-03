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
* Puncturing for protographs is defined within the protograph template passed - the punctured indices are excluded from the list of transmitted bits within the protograph. Read more [here](TODO).
* Puncturing for regular codes is achieved with the optional -f flag. if this flag is provided, the value passed specifies the proportion of bits to transmit; a .transmitted file is generated accordingly. Read more [here](TODO).

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
