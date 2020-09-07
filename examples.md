---
layout: default
title: Examples
nav_order: 3
parent: Overview
---

# Examples
## make-pchk

### Generate a 1500 by 500 2/3 rate regular ldpc parity check matrix with ~3 1s per column:

```sh
python3 LDPC-library/make-pchk.py --output-pchk ./pchk-file --code-type regular --construction populate-columns --n-checks 500 --n-bits 1500 --ones-per-col 3
```
In this example solely a parity check matrix file is create, puncturing is not implemented. The parity check file exists at ./pchk-file.

### Generate a 1500 by 500 2/3 rate regular ldpc parity check matrix with puncture bit rate of 0.7:

```sh
python3 LDPC-library/make-pchk.py --output-pchk ./pchk-file --code-type regular --construction populate-columns --n-checks 500 --n-bits 1500 --ones-per-col 3 -f 0.7
```

Here a parity check matrix like the one above is created, along with a pchk-file.transmitted file which contains the information necessary for puncturing.

### Generate a protograph ldpc parity check matrix based on the ar4ja rate 1/2 protograph (sparse file) with an expansion factor of 4:

```sh
python3 LDPC-library/make-pchk.py --output-pchk ./pchk-file --code-type regular --construction quasi-cyclic --protograph-file ./example-protographs/ar4ja_n_0_rate_1_2_sparse --expansion-factor 4
```

A protograph-based ldpc parity check matrix is created based on the template provided at the given location. If puncturing information is included in the protograph template file, a pchk-file.transmitted file will be created with the necessary data for puncturing to take place.

## encode

```sh
python LDPC-library/encode.py [-h] --pchk-file ./pchk-file --gen-file ./gen-file --input-file
message-file --output-file encoded-file
```

This execution assumes a parity check code file and a corresponding generator matrix file already created. These two arguments must correspond with each other: the generator file must be created from the provided parity check file. check [usage](usage.html) for details on how to create the generator matrix. If a pchk-file.transmitted is present in the directory of pchk-file, puncturing is performed as dictated by the .transmitted file. The message provided by message-file is read and encoded, the result is present in the encoded-file, where each encoded block is separated by newline characters.

## decode

```sh
python LDPC-library/decode.py [-h] --pchk-file ./pchk-file --received-file transmitted-file --output-file decoded-file --channel bsc [--channel-parameters 0.01] [--max-iterations 100]
```

Here we use the provided parity check code at pchk-file to corrupt the corrupted data contained in transmitted-file. If a corresponding pchk-file.transmitted file is found in the local directory, a restoration of the punctured transmitted information is performed where erasures are represented by 0s. the decoded-file argument defines the filepath to write the decoded codewords to.  By specifying parameters: <code>bsc 0.01</code> we indicate that the transmitted file was corrupted according to bynary-symetric corruption, where roughly 1% of the bits underwent corruption. <code>--max-iterations 100</code> indicates that in decoding, a maximum belief-propagation iteration count of 100 will be tolerated before the decoding process is terminated.
