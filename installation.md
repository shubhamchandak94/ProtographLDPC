---
layout: default
title: Installation
nav_order: 1
parent: Overview
---

# Installation
---
The relevant code is contained at [this](https://github.com/shubhamchandak94/ProtographLDPC/) repository <br>

Do a recursive download
```sh
git clone --recursive https://github.com/shubhamchandak94/ProtographLDPC
```

To update the contained submodule, run
```sh
git pull --recurse-submodules
git submodule update --init --recursive
```

After cloning, install the LDPC-codes submodule
```sh
cd LDPC-codes/
make
cd ..
```
