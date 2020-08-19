---
layout: default
title: LDPC codes
parent: Background
nav_order: 2
---

# LDPC Codes
## Background
LDPC codes--(L)ow (D)ensity (P)arity (C)heck Codes--are codes which are defined by particularly sparse parity check matrices. The quality of being sparse is defined by an absurdly small ratio of 1s to 0s, as well as a large distribution uniformity of  1s within the parity check matrix. Unlike other types of linear codes, LDPC codes are not restricted in their hamming distance by larger code rates (code rate being the ratio of message length to encoded codeword length).

## Representation
All linear codes can be represented in a variety of ways. Thought operations are performed on the matrix level, linear codes can also be represented by gaphs, among the most prevalant of which is the Tanner (Bi-partite) graph.

This graph represents codes as follows:
given a layer of nodes representing the parity check equations and a layer of nodes representing the indices in the codeword, connections are made between parity-check node and codeword-index node if the parity-check equation includes the code-word index in its summation.

For example, consider the following code in both its matrix form and bipartite graph form:
![example code](./figures/example_code.png)

<strong>num message bits:</strong> 4 <br>
<strong>num parity check bits:</strong> 4 <br>
<strong>rate:</strong> 1/2 <br>

Each of the four parity check nodes (a.k.a. check nodes) in the tanner graph maps to multiple codeword nodes (a.k.a. variable nodes). The connected variable nodes for each check node are represented by the location of 1s in the corresponding row of the matrix form.

Understanding this representation is crucial to customize the provided library. All functions (with the exception of wrappers of the base library) work with parity check codes in their bipartite graph form. Doing so allows for the sole handling of 1s (graph connections), thus sidestepping the processing of 0s. This is ideal: LDPC Codes by definition contain many 0s and few 1s.


## LDPC Code Classification
LDPC codes can be further classified according to their characteristics and constructions.

The three most relevant to this library are:
* Irregular codes
* Regular codes
* Protograph codes

NOTE: When discussing weight, weight refers to the number of ones in defined scope.


### Irregular LDPC Codes
Irregular codes are codes whose parity check matrices contain row and column weightages that
are not necessarily constant for the entire matrix.

### Regular LDPC Codes
Regular codes are represented by matrices whos row weights are constant and whose column weights are constant. It is important to note that although by definition row and column weights must be constant in regular codes, some constructions do not allow this: there are tradeoffs. 

Specifically, for all entirely regular LDPC codes, the width <strong>w</strong> of the matrix relates to its height <strong>h</strong> according to the following relationship:

<strong>h</strong> = <strong>w (c / r)</strong>

If the constant <strong>c / r</strong> is to be maintained, then there is restriction placed on both <strong>w</strong and <strong>h</strong>. Some regular code constructions defined in this library enforce complete regularity at the expense of width and height values, while some enforce the given width and height at the expense of the regularity of the matrix.

In this sense, both comoletely regular and mostly regular matrices can repreesnt a regular LDPC code. 

### Protograph LDPC Codes

Protograph LDPC Codes implement the expanding of a protograph into a full-fledged LDPC Code. 
A protograph is a tanner graph with a few special properties:
* protographs contain a relatively small number of of nodes
* protographs allow for parallel connections, meaning more than one connection between a check note and variable node
    * In the representative matrix for the protograph, this would manifest as a value greater than 1

You can read more about protographs [here](https://personal.utdallas.edu/~aria/papers/NguyenNosratinia2012a.pdf). <br>
**Sections 2A and 2B are particularly helpful

Expanded protograph LDPC codes can be assessed through the direct analyzation of the protograph itself. Each lifted code, regardless of the construction algorithm, inherits the density distribution defined by the protograph (higher degree indicates a higher density in the corresponding section of the expanded code) as well as the local graph structure (associatively dense areas are located according to their positions in the protograph).

You can read more about the properties of expanded protographs and the benefits of protograph codes  [here](https://math.nd.edu/assets/210003/06089477.pdf). <br>
Benefits of protograph codes - Section 1 <br>
Properties of expanded protographs - Section 2C <br>








