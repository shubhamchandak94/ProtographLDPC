---
layout: default
title: Library organization
parent: Methods
nav_order: 4
---

# Library Organization

## Background
This library includes a collection of code classes packaging functionality to describe LDPC Codes. Before any experimentation is performed, it must be noted that this library deals with LDPC Codes in their tanner graph form. Dealing with tanner graphs allows for the complete sidestepping of degree zero entries - they are not indicable on tanner graph representations of codes. Given LDPC codes are majoratively composed of 0s, this presents a considerable optimization.

Althought this library is built to work independently, the python scripts included provide an interaction of the base library with the python library. 

## Structure
The project is structured the following way

```sh
.
|_ LDPC-codes
    |_ base programs  # base library exists in this location
|_ LDPC-library  # addition
    |_ libs
        |_ Identity.py
        |_ Protograph.py
        |_ ProtographLDPC.py
        |_ RegularLDPC.py
        |_ TannerGraph.py
    |_ decode.py
    |_ encode.py
    |_ make-pchk.py
|_ protographs
    |_ protograph1
    |_ protograph2
    |_ protograph3
    |_ protograph4
    |_ protograph5
    |_ protograph6
|_ LDPC-install
|_ test_script_protograph.sh
|_ test_script_regular.sh
```

## LDPC-library

Check [usage](TODO) for a description of the provided scripts

### Implemented classes

<strong>TannerGraph.py</strong>

The class defined by this file provides the superclass for all implemented classes in the library. It provides the base tanner graph structure upon which to other classes must build upon. Specifically, this class defines the tanner_graph dictionary, the fundamental structure behind the library's functionality. 

All subclasses are required to implement the construction of this structure, as well as a definition of the width and height attributes.

The provided api to work with TannerGraphs objects assumes a defined width, a defiend height, and a non-empty tanner_graph dictionary.


<strong>RegularLDPC.py</strong>

