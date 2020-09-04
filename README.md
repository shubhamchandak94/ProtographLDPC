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
Install PEG library:
```
cd peg/
make
cd ..
```

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
