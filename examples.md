---
layout: default
title: Examples
nav_order: 3
parent: Overview
---

# Usage examples

### Generate a 1500 by 500 2/3 rate regular ldpc parity check matrix with ~3 1s per column:

```sh
python3 make-pchk.py --output-pchk ./pchk-file --code-type regular --construction populate-columns --n-checks 500 --n-bits 1500 --ones-per-col 3
```
In this example solely a parity check matrix file is create, puncturing is not implemented. The parity check file exists at ./pchk-file.

### Generate a 1500 by 500 2/3 rate regular ldpc parity check matrix with puncture bit rate of 0.7:

```sh
python3 make-pchk.py --output-pchk ./pchk-file --code-type regular --construction populate-columns --n-checks 500 --n-bits 1500 --ones-per-col 3 -f 0.7
```

Here a parity check matrix like the one above is created, along with a pchk-file.transmitted file which contains the information necessary for puncturing. 

### Generate a protograph ldpc parity check matrix based on the ar4ja rate 1/2 protograph (sparse file) with an expansion factor of 4:

```sh
python3 make-pchk.py --output-pchk ./pchk-file --code-type regular --construction quasi-cyclic --protograph-file ./example-protographs/ar4ja_n_0_rate_1_2_sparse --expansion-factor 4
```

A protograph-based ldpc parity check matrix is created based on the template provided at the given location. If puncturing information is included in the protograph template file, a pchk-file.transmitted file will be created with the necessary data for puncturing to take place. 



