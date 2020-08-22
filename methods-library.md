---
layout: default
title: Library organization
parent: Methods
nav_order: 4
---

# Library Organization

## Background
This library includes a collection of code classes packaging functionality to describe LDPC Codes. Before any experimentation is performed, it must be noted that this library deals with LDPC Codes in their tanner graph form. Dealing with tanner graphs allows for the complete sidestepping of degree zero entries - they are not indicable on tanner graph representations of codes. Given LDPC codes are majoratively composed of 0s, this presents a considerable optimization.

Although this library is built to work independently, the python scripts included provide an interaction of the base library which decodes matrices, not graphs. The provided encode and decode scripts provide a wrapper for this interaction to take place.

## Structure

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

The class defined by this file provides the superclass for all implemented code classes in this library. It provides the base tanner graph structure upon which to other classes must build upon. Specifically, this class defines the tanner_graph dictionary, the fundamental structure behind the library's functionality. 

All subclasses are required to implement the construction of this structure, as well as a definition of the width and height attributes.

The provided api to work with TannerGraphs objects assumes a defined width, a defiend height, and a non-empty tanner_graph dictionary.

The tanner_graph dictionary maps row indices to a list of column indices. This coordinate system specifies all the 1 entries within the TannerGraph object.


<strong>RegularLDPC.py</strong>

The class defined within this file dictates the interaction and creation of Regular LDPC Codes as sub TannerGraph objects.

<strong>ProtographLDPC.py</strong>

The class defined within this file dictates the interaction and creation of Protogrpah LDPC Codes as sub TannerGraph objects.

<strong>Protograph</strong>

This file contains the implementation of the Protograph class. Protographs are special special TannerGraph objects: the tanner_graph structure maps row indices to a list of ProtographEntry objects instead of a list of integers. Doing so allows Protographs to contain higher order degree values, values necessary for the construction of comprehensive expanded Protograph LDPC Codes.

<strong>Identity.py</strong>

This file defines a class that handles the special case of tanner graphs associated with identity matrices. Should an experimental construction require the creation and otherwise manipulation of identity matrices, this class provides a handling for identity matrix graphs. Because all TannerGraph objects (with the exception of protograph objects) can interact with each other through the merging/absorbtion processes, experimental procedures can be written to build complete LDPC codes using the identity class provided within this file, or using Identity codes in conjunction with other codes.

## Provided Protographs

This library implements a few standard protographs in the protographs directory. These files are directly readable by the library. Navigate to the [Sample Protographs](./methods-protograph.html) page for descriptions.

-----
Refer to the [repository](https://github.com/shubhamchandak94/ProtographLDPC/tree/master/LDPC-library/libs) for the associated api.
