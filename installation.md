---
layout: default
title: Installation
nav_order: 1
parent: Overview
---

# Installation
The relevant code is contained on GitHub at [https://github.com/shubhamchandak94/ProtographLDPC/](https://github.com/shubhamchandak94/ProtographLDPC/).  
The code has been tested on Linux and MacOS with Python 3.

Do a recursive download:
```sh
git clone --recursive https://github.com/shubhamchandak94/ProtographLDPC/
```

Enter the project directory:
```sh
cd ProtographLDPC/
```

To update submodule in existing clone, run
```sh
git pull --recurse-submodules
git submodule update --init --recursive
```
Install LDPC-codes submodule:
```sh
cd LDPC-codes/
make
cd ..
```
Install PEG library:
```sh
cd peg/
make
cd ..
```

For usage and test scripts, see [this](usage.html) page.
