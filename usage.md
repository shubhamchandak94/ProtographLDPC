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
python3 make-pchk.py pchk-file code-type construction build-params
```
```
build params:
if code-type == regular:
    build-params: width, height, column-weight
if code-type == protograph:
    build-params: protograph-file, expansion-factor 
```

| code-type |  construction options |
|:-:|-|
| regular | {::nomarkdown}<ul><li>gallager</li><li>random</li><li>populate-rows</li><li>populate-columns</li></ul>{:/} |
| protograph | {::nomarkdown}<ul><li>permutation</li><li>regular</li><li>quasi-cyclic</li><li>permuted-quasi-cyclic</li></ul>{:/} |

Generates a parity check code of the following format
```sh
pchk-file
    |_ pchk-file
    |_ .transmitted
```
* the pchk file contains the machine-readable fully constructed LDPC code

the .transmitted file contains the following information
```sh
factor: expansion-factor
total bits before transmission: code-width
[space separated list of transmitted bit indices]
```
If you wish to include puncturing for a regular code, you must edit the .transmitted file to include the necessary information in the above format. Specifically, remove the indices you wish to puncture in transmission from the index list.

## encode
Encodes a message provided a parity check code
```sh
python3 encode.py pchk-file gen-file source-file encoded-path
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
where pchk-file is the parity check file generated, NOT THE PARITY CHECK DIRECTORY

gen-file is the filepath of the output generator matrix file. <br>
method is the encoding schema for the generator matrix file.

###  In the context of the python encode script:

* pchk-file refers to the pchk-directory created by the make-pchk program, not any of the files contained within. <br>
* gen-file refers to the path of the generator matrix file corresponding to the specified parity check code. <br>
* source-file refers to the filepath of the message to be encoded as a string of 1s and 0s.
* encoded-path refers to the path of the encoded message.

the encoded message is in the following format
```sh
encoded-file
    |_ encoded-file
    |_ .preserved
```
The .preserved file contains the message encoding as it would appear before puncturing, separated by newline characters. <br>

The contained encoded-file contains the encoded codewords after puncturing, separated by newline characters.

## Decode
Decodes a given message according to the following
```sh
python3 decode.py received-file channel-params decode-iterations decoded-file pchk-file
```
* received-file is the file produced as a result of the encoding, after undergoing some corruption (the base library provides a [transmit](./LDPC-codes/channel.html#transmit) function which induces corruption)
* channel-params can be one of the following three
```sh
bsc error-probabilioty [0, 1)
awgn standard-deviation
misc 0.0
```
This selection is made based on the type of corruption associated with the selected transmission channel

* decode-iterations dictates the number of decoding iterations used in decoding. The decode script implements a wrapper of the [decode](./LDPC-codes/decoding.html#decode) function of the base library, and the prprp is directly passed as an argument to the base decode program.

* decoded-file is the filepath of the output of the decoding. Each decoded message is separated by a newline character
