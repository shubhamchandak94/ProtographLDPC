# Protograph LDPC Codes

### Documentation: https://shubhamchandak94.github.io/ProtographLDPC/

TODO: update readme

A library developed for the exploration of LDPC matrices. Built off of radfordneal's [library](https://github.com/radfordneal/LDPC-codes) for the research of general LDPC codes.
The README for the base library can be found [here](https://github.com/radfordneal/LDPC-codes/blob/master/README).

Installation
---
Do a recursive download
```
git clone --recursive https://github.com/roshanprabhakar/LDPC-SandboxLibrary
```
To update submodule in existing clone, run
```
git pull --recurse-submodules
git submodule update --init --recursive
```
Install LDPC-codes submodule:
```
cd LDPC-codes/
make
cd ..
```
