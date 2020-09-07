---
layout: default
title: Library organization
parent: Methods
nav_order: 4
---

# Library organization

## Table of Contents
* [Background](#background)
* [Structure](#structure)
* [Implemented classes](#implemented-classes)

## Background
This library includes a collection of code classes packaging functionality to describe LDPC Codes. This library works with LDPC Codes in their sparse Tanner graph form. Although this library is built to work independently, the Python scripts included provide conversion functions for interaction with the [base library](https://github.com/shubhamchandak94/LDPC-codes) which has a specific parity check matrix format. Similarly the script interacts with the [peg](https://github.com/shubhamchandak94/ProtographLDPC/tree/master/peg) library used for parity check matrix construction. We briefly describe the library structure below, for more details please refer to the code [here](https://github.com/shubhamchandak94/ProtographLDPC/tree/master/LDPC-library).

## Structure

```
|_ LDPC-library
    |_ libs
        |_ Identity.py
        |_ Protograph.py
        |_ ProtographLDPC.py
        |_ RegularLDPC.py
        |_ TannerGraph.py
    |_ decode.py
    |_ encode.py
    |_ make-pchk.py
```

## Implemented classes

### TannerGraph.py

The class defined by this file provides the superclass for all implemented code classes in this library. It provides the base Tanner graph structure upon which to other classes must build upon. Specifically, this class defines the tanner_graph dictionary, the fundamental structure behind the library's functionality.

All subclasses are required to implement the construction of this structure, as well as a definition of the width and height attributes. The provided API to work with TannerGraphs objects assumes a defined width, a defined height, and a non-empty tanner_graph dictionary. The tanner_graph dictionary maps row indices to a list of column indices. This specifies all the 1 entries within the TannerGraph object.

The file also contains several utility functions used by different construction methods, as well as an `analyze` function to visualize the generated codes.

### RegularLDPC.py

The class defined within this file dictates the interaction and creation of Regular LDPC Codes as TannerGraph objects.

### ProtographLDPC.py

The class defined within this file dictates the interaction and creation of Protograph LDPC Codes as TannerGraph objects.

### Protograph.py

This file contains the implementation of the Protograph class. Protographs are a special case of TannerGraphs: the tanner_graph structure in protographs maps row indices to a list of ProtographEntry objects instead of a list of integers. Doing so allows Protographs to contain higher order degree values (rather than just binary values), which is required in the construction of expanded Protograph LDPC Codes.

### Identity.py

This file defines a class that handles the special case of Tanner graphs associated with permutation matrices. This is useful for certain construction methods. Because all TannerGraph objects (with the exception of protograph objects) can interact with each other through the merging/absorbtion processes (defined in the TannerGraph superclass), experimental procedures can be written to build complete LDPC codes using the Identity class provided within this file, or using Identity codes in conjunction with other codes.
