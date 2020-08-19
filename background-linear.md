---
layout: default
title: Linear codes
parent: Background
nav_order: 1
---

# Linear Codes
## Background
Linear codes were developed as a means to enable the correction of errors induced in the streaming of data. They are defined by their property that any linear sum of messages results in a message. These codes can be broken into two types - block codes and convolutional codes. This library focuses on code construction as it relates to block codes.

Linear block codes are designed in such a way that upon encoding a message, this message can be decoded assuming a non-critical corruption rate through an analysis of the received message bits. This is accomplished through an evaluation of parity check equations where a modulo summation is performed on the received message indicated by the indices of the parity check equation. For our purposes, the result will be zero.

A code is defined by a collection of these parity check equations, and the number of conforming codewords that can possibly be created is referred to as the size of the code. This collection of parity check equations is represented in the form of a parity check matrix, where each row of the matrix indicates a parity check equation. Within these rows, a 1 at bit n indicates the inclusion of received bit n in the equation defined by the row.

Important:
* <strong>n</strong>: commonly used to denote codeword length
* <strong>k</strong>: commonly used to denote message length
* <strong>code rate</strong>: the ratio <strong>k/n</strong> where k is the length of a message before encoding and n is the length of the encoded codeword
* <strong>block</strong>: codeword

## Parity Check Matrix
The matrix containing the cumulation of parity check equations is known as the parity check matrix. Its width n is equivalent to the length of all codewords defined by the code. Assuming a binary character system, the number of all messages of length n is equal to 2<sup>n</sup>. By including a nonzero number of parity check equations, the number of codewords that conform to the code decreases. 

As the number of possible codewords decreases, but the length of all codewords stays the same, the distance between codewords increases where distance is defined by the number of nonidentical values between two codewords. For example, there is a distance of 3 between the codewords 100101 and 000011. The minimum distance between any two possible codewords that conform to a given code is known as the hamming distance of that code. This value is important - the larger the hamming distance, the larger the necessary corruption to render a received message undecodeable. 

## Generator Matrix
A generator matrix is defined by the parity check matrix H. The generator matrix G performs the lifting of a message to a proper codeword. Optimized codes define parity check matrices, and therefore generator matrices, in such a way that if messages are of length m, and the number of possible codewords defined by the code is equal to z < 2<sup>n</sup> (where n is the length of resulting codewords), 2<sup>m</sup> (the number of possible messages) is as close to z (the number of possible codewords) as possible. Such codes where 2<sup>m</sup> = z are known as perfect codes.

## Library specification
The encoding/decoding processes defined by this library assume the following schema 

Assuming a codeword can be divided into <strong>M</strong> parity check bits *<strong>c</strong>* preceeding <strong>K</strong> message bits *<strong>s</strong>*:

a parity check matrix *<strong>H</strong>* can be divided into an <strong>M</strong> by <strong>M</strong> matrix *<strong>A</strong>* occupying the first <strong>M</strong> columns of <strong>H</strong> and an <strong>M</strong> by <strong>K</strong> matrix *<strong>B</strong>* occupying the remaining <strong>K</strong> columns of *<strong>H</strong>*. 

And all codewords conforming to the code H follow the rule:
<strong>*Ac* + *Bs* = 0</strong>

From here, we derive <strong>*Ac* = *Bs*</strong>. Modulo arithmetic is performed thus addition and subtraction are identical in effect.

Given *<strong>A</strong>* is invertible, the following relationship is given relating parity bits to message bits:
<strong>*c* = *A<sup>-1</sup>Bs*</strong>

Both a parity check matrix and generator matrix must be initialized before the encoding/decoding proccesses can occur. This libraries provides multiple constructions for different types of parity check matrices, and generator matrices are generated from this matrix.

###### ** The api to interact with these matrices is defined in the usage section

## Puncturing
The process of puncturing is simple: the rate of a given linear code can be made larger by transmitting fewer codeword indices.

In order to effectively "puncture" a codeword, only the transmission of the weakest protected indices within that codeword is performed. For any given code, the parity check equations defined by the parity check matrix will render a few codeword indices more susceptible to irreversible corruption than other codeword indices. By transmitting solely these "weakly protected" indices, and assuming erasure corruption for the strongest protected bits, the code rate can be drastically increased while maintaining code viability.

In the provided implementations, puncturing is implemented by streaming the codeword after removing punctured bits, then reconstructing the received message with 0s representing erasures in the punctured indices.
