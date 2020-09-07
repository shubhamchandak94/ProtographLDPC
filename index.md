---
layout: default
title: Overview
nav_order: 1
has_children: true
---
**Implementation of Protograph LDPC error correction codes**  
*Roshan Prabhakar<sup>1</sup>, Shubham Chandak<sup>2</sup>, Kedar Tatwawadi<sup>2</sup>*

<sup>1</sup>Fremont High School, Sunnyvale, CA, USA  
<sup>2</sup>Stanford University, Stanford, CA, USA  

[![DOI](https://zenodo.org/badge/287030442.svg)](https://zenodo.org/badge/latestdoi/287030442)

**Code**: [https://github.com/shubhamchandak94/ProtographLDPC](https://github.com/shubhamchandak94/ProtographLDPC)

LDPC codes are a class of linear error-correction codes on sparse bipartite graphs providing efficient decoding using message passing (between variable and check nodes on the graph) and excellent error correction performance. Among the various classes of LDPC codes, regular LDPC codes have fixed degree variable and check nodes and perform quite well in the high rate regimes for finite block lengths. Irregular LDPC codes can achieve performance closer to capacity but need some fixes to achieve good finite block length performance. Protograph LDPC codes offer the best of both worlds by lifting a small protograph with desirable properties. This work aims to provide an open-source library for protograph LDPC codes that is easy to use and extend. We hope this can be useful for researchers and practitioners in traditional and modern areas like DNA-based data storage. The library includes functionality for:

- Generation of regular and protograph LDPC matrices using PEG and other construction methods.
- Encoding and decoding of these codes, including support for puncturing.
- Utility and test scripts to allow analysis of these codes.

This library heavily uses two prior libraries and we would like to thank the corresponding developers:
- [LDPC-codes](https://github.com/shubhamchandak94/LDPC-codes): Library for construction, encoding, decoding of regular and irregular LDPC codes, also containing several utility scripts. This is a fork of Radford Neal's library available [here](https://github.com/radfordneal/LDPC-codes).
- [peg](peg/): Implementation of the Progressive Edge Growth (PEG) algorithm used for parity check matrix construction. This was obtained from [http://www.inference.org.uk/mackay/PEG_ECC.html](http://www.inference.org.uk/mackay/PEG_ECC.html).

This website contains details about the library including installation instructions, usage, examples, methods, simulation results, references and citation information.


### Acknowledgement
This project began as part of the [STEM to SHTEM](https://compression.stanford.edu/summer-internships-high-school-students) summer internship program, and we thank Prof. Tsachy Weissman, who initiated this program and supported us in this project.

We would also like to thank Prof. Andrea Montanari, who taught a class on modern coding theory at Stanford ([EE 388](https://web.stanford.edu/class/ee388/)) which provided the original inspiration for this project.

### History
We worked on a [project](https://github.com/shubhamchandak94/LDPC_DNA_storage) on DNA-based data storage a few years back and had to settle for regular LDPC codes because of a lack of easy-to-use implementations of protograph codes. We hope this project can meet this need for similar future projects and inspire other open-source libraries. Enjoy!
