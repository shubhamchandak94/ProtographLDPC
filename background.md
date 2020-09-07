---
layout: default
title: Background
nav_order: 2
---

We provide here a very brief background on error correction codes, specifically linear codes and LDPC codes (regular and protograph). For a more detailed introduction, please see the [References](references.html) page.

# Linear Codes
## Background
Linear codes were developed as a means to enable the correction of errors induced in the streaming of data. They are defined by their property that any linear sum of messages results in a message. These codes can be broken into two types - block codes and convolutional codes. This library focuses on code construction as it relates to block codes.

Linear block codes are designed in such a way that upon encoding a message, this message can be decoded assuming a non-critical corruption rate through an analysis of the received message bits. This is accomplished through an evaluation of parity check equations where a modulo summation is performed on the received message indicated by the indices of the parity check equation for each parity check equation in the code. For our purposes, each parity check equation yields a zero for a given correct message.

A code is defined by a collection of parity check equations, and the number of conforming codewords that can possibly be created is referred to as the size of the code. This collection of parity check equations is represented in the form of a parity check matrix, where each row of the matrix indicates a parity check equation. Within these rows, a 1 at bit n indicates the inclusion of received bit n in the equation defined by the row.

Important:
* <strong>n</strong>: commonly used to denote codeword length
* <strong>k</strong>: commonly used to denote message length
* <strong>code rate</strong>: the ratio <strong>k/n</strong> where <strong>k</strong> is the length of a message before encoding and <strong>n</strong> is the length of the encoded codeword

## Parity Check Matrix
The matrix containing the cumulation of parity check equations is known as the parity check matrix. Its width n is equivalent to the length of all codewords defined by the code. Assuming a binary character system, the number of all messages of length n is equal to 2<sup>n</sup>. By including a nonzero number of parity check equations, the number of codewords that conform to the code decreases.

As the number of possible codewords decreases, but the length of all codewords stays the same, the distance between codewords increases where distance is defined by the number of nonidentical values between two codewords. For example, there is a distance of 3 between the codewords 100101 and 000011. The minimum distance between any two possible codewords that conform to a given code is known as the hamming distance of that code. This value is important - the larger the hamming distance, the larger the necessary corruption to render a received message undecodeable.

## Generator Matrix
A generator matrix is defined by the parity check matrix H. The generator matrix G performs the lifting of a message to a proper codeword. Optimized codes define parity check matrices, and therefore generator matrices, in such a way that if messages are of length m, and the number of possible codewords defined by the code is equal to z < 2<sup>n</sup> (where n is the length of resulting codewords), 2<sup>m</sup> (the number of possible messages) is as close to z (the number of possible codewords) as possible. Such codes where 2<sup>m</sup> = z are known as perfect codes.

## Library specification
The encoding/decoding processes defined by this library assume the following schema

Assuming a codeword can be divided into <strong>M</strong> parity check bits *<strong>c</strong>* preceeding <strong>K</strong> message bits *<strong>s</strong>*:

a parity check matrix *<strong>H</strong>* can be divided into an <strong>M</strong> by <strong>M</strong> matrix *<strong>A</strong>* occupying the first <strong>M</strong> columns of <strong>H</strong> and an <strong>M</strong> by <strong>K</strong> matrix *<strong>B</strong>* occupying the remaining <strong>K</strong> columns of *<strong>H</strong>*.

All codewords conforming to the code H follow the rule:
<strong>*Ac* + *Bs* = 0</strong>

From here, we derive <strong>*Ac* = *Bs*</strong>. Modulo arithmetic is performed thus addition and subtraction are identical in effect.

Given *<strong>A</strong>* is invertible, the following equation relates parity check bits to message bits:
<strong>*c* = *A<sup>-1</sup>Bs*</strong>

Both a parity check matrix and generator matrix must be initialized before the encoding/decoding proccesses can occur. This libraries provides multiple constructions for different types of parity check matrices, and generator matrices are generated from this matrix.

###### ** The api to interact with these matrices is defined in the usage section

## Puncturing
The process of puncturing is simple: the rate of a given linear code can be made larger by transmitting fewer codeword indices.

In order to effectively "puncture" a codeword, only the transmission of the weakest protected indices within that codeword is performed. For any given code, the parity check equations defined by the parity check matrix will render a few codeword indices more susceptible to irreversible corruption than other codeword indices. By transmitting solely these "weakly protected" indices, and assuming erasure corruption for the strongest protected bits, the code rate can be drastically increased while maintaining code viability.

In the provided implementations, puncturing is implemented by streaming the codeword after removing punctured bits, then reconstructing the received message with 0s representing erasures in the punctured indices.

# LDPC Codes
## Background
LDPC codes--(L)ow (D)ensity (P)arity (C)heck Codes--are codes which are defined by particularly sparse parity check matrices. The quality of being sparse is defined by an extremely small ratio of 1s to 0s, as well as a large distribution uniformity of  1s within the parity check matrix. Unlike other types of linear codes, LDPC codes are not restricted in their hamming distance by larger code rates (code rate being the ratio of message length to encoded codeword length).

## Representation
All linear codes can be represented in a variety of ways. Though operations are performed on the matrix level, linear codes can also be represented by gaphs, among the most prevalant of which is the Tanner (Bi-partite) graph representation.

This graph represents codes as follows:
given a layer of nodes representing the parity check equations and a layer of nodes representing the indices in the codeword, connections are made between parity-check node and codeword-index node if the parity-check equation of the parity-check node includes the code-word index in its summation.

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

NOTE: When discussing weight, weight refers to the number of ones in the defined scope.


### Irregular LDPC Codes
Irregular codes are codes whose parity check matrices contain row and column weightages that
are not necessarily constant for the entire matrix.

### Regular LDPC Codes
Regular codes are represented by matrices whos row weights are constant and whose column weights are constant. It is important to note that although by definition row and column weights must be constant in regular codes, some constructions do not allow this: there are tradeoffs.

Specifically, for all entirely regular LDPC codes, the width <strong>w</strong> of the matrix relates to its height <strong>h</strong> according to the following relationship:

<strong>h</strong> = <strong>w (c / r)</strong>

where <strong>c</strong> represents the constant column weightage of the code and <strong>r</strong> represents the constant row weightage.

If the constant <strong>c / r</strong> is to be maintained, then there is restriction placed on both <strong>w</strong> and <strong>h</strong>, specifically

<strong>c / r</strong> = <strong>h / w</strong>.

Some regular code constructions defined in this library enforce complete regularity at the expense of width and height values, while some enforce the given width and height at the expense of the regularity of the matrix.

In this sense, both completely regular and mostly regular matrices can repreesnt a regular LDPC code.

### Protograph LDPC Codes

Protograph LDPC Codes implement the expanding of a protograph into a full-fledged LDPC Code.
A protograph is a tanner graph with a few special properties:
* protographs contain a relatively small number of of nodes
* protographs allow for parallel connections, meaning more than one connection between a check node and variable node
    * In the representative matrix for the protograph, this would manifest as a value greater than 1

You can read more about protographs [here](https://personal.utdallas.edu/~aria/papers/NguyenNosratinia2012a.pdf). <br>
**Sections 2A and 2B are particularly helpful

Expanded protograph LDPC codes can be assessed through the direct analyzation of the protograph itself. Each lifted code, regardless of the construction algorithm, inherits the density distribution defined by the protograph (higher degree indicates a higher density in the corresponding section of the expanded code) as well as the local graph structure (associatively dense areas are located according to their positions in the protograph).

You can read more about the properties of expanded protographs and the benefits of protograph codes  [here](https://math.nd.edu/assets/210003/06089477.pdf). <br>
Benefits of protograph codes - Section 1 <br>
Properties of expanded protographs - Section 2C <br>
