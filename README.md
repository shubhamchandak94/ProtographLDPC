# LDPC-Codes
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

Additions to the base library
---
---
- An implementation of LDPC matrices directly from factor graphs. Written in Python.\
Implementation can be found at ./LDPC-TannerGraphs
```bash
./MakePCHKT parity-matrix-file [n-checks, codeword-length/n-bits | codeword-length, checks-per-bit, bits-per-check]
```
---
- An implementation of LDPC matrices directly to matrix form. Written in Java.\
Implementation can be found at ./LinearCodes
```bash
./MakePCHK parity-matrix-file [n-checks, codeword-length/n-bits | codeword-length, checks-per-bit, bits-per-check]
```
---
- An automation of the testing pipeline for parity check matrices.\
(message -> encoded message -> transmitted/corrupted corrupted -> decoded codewords -> extracted message)
- Written for the testing of different implementations of LDPC matrices.
- Pipeline defaults:
    - The control LDPC matrix pipeline is constructed using the evenboth operation
    - All corresponding generator matrices are constructed in the dense format
    - All corruption is binary symmetric and follows the user-provided switch the probability
    - Decoding utilizes the prprp 1000000 process
```bash
./PipelineExecutor n-checks codeword-length/n-bits checks-per-bit error-probability
```
- Analyzing the results
    - the original message is stored at ./PipelineRES/Message/PipelineDefault
    - the resulting message after transmission and decoding is stored at ./PipelineRES/ExtractedMessage
    - All files named PipelineDefaultLibraryGenerated belong to the control pipeline (LDPC matrix generated using default programs)
    - All files named PipelineDefaultPythonGenerated belong to the Python pipeline
        - The result of this pipeline is to be compared to the result of the control pipeline in order to provide the basis for analysis
---
Note
---
- Change run permissions for all necessary bash scripts before attempting to run any of the added processes
    - ./MakePCHK
    - ./MakePCHKT
    - ./PipelineExecutor

```bash
chmod +x file
```
(for all files  listed)

- The directory and all contained subdirectories within PipelineRES are crucial to the automation process. If you wish to rename any of these directories, make sure to the change the corresponding information in PipelineExecutor.sh

---
Added test script
---
arguments: parity-check-width (codeword length), parity-check-height (number of checks), # 1s per col, error rate, numblocks, number of LDPC iterations

Sample usage:
```
./test_script.sh 2000 1000 3 0.03 10 100
```
This does 10 blocks for a 2000-bit codeword containing 1000 parity checks (so 2000-1000=1000 message bits). The codewords are transmitted through a BSC(0.03) and decoded using 100 LDPC iterations. Both the default library implementation and the new python implementation are used and the respective bit error and block rates are printed out. Note that the encoding is not actually performed, we just transmit the all-zeros codeword (which is general enough considering the symmetry of the channel).
