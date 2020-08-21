---
layout: default
title: Parity pheck construction - protograph codes
parent: Methods
nav_order: 2
---

# Protograph-based LDPC Code Constructions

## Table of Contents
* [background](./methods-protograph.html#background)
* [permutation](./methods-protograph.html#permutation)
* [regular](./methods-protograph.html#regular)
* [quasi-cyclic](./methods-protograph.html#quasi-cyclic)
* [permuted-quasi-cyclic](./methods-protograph.html#permuted-quasi-cuclic)

### Background

This library includes different constructions for the creation of Protograph-based LDPC Codes. Protograph codes are created through the expansion of a base protograph. The resulting LDPC code matrix is a combination of "submatrices", each submatrix corresponding to the degree specified in the corresponding section of the protograph. Given an expansion factor f, these submatrices are strictly f by f dimensions. 

For example assume a protograph whose matrix representation has a height width <strong>w</strong> a height <strong>h</strong> an expansion factor <strong>f</strong> and is populated with integers in the following domain: [0, ∞).

The resulting LDPC code would be representable by a <strong>w * f</strong> by <strong>h * f</strong> matrix, where each <strong>f</strong> by <strong>f</strong> scope positioned at <strong>(r, c)</strong> within the resulting matrix would correspond to a submatrix whose construction depended on the protograph degree specified at location <strong>(r/f, c/f)</strong>.

The protograph code constructions following are constructions of this submatrix. <strong>f</strong> is used to represent the expansion factor (and thus width of the submatrix) and <strong>v</strong> is used to represent the protogrpah degree upon which the submatrix construction is to operate.

### Permutation

This construction generates a submatrix the result of a summation of <strong>v</strong> non-overlapping permutation matrices.

Implications:
* the resulting matrix is strictly regular in the weightages of its rows and columns - each permutation matrix adds exactly one node to each row and each column of the submatrix.

This library contains an api for the handling of the special case of tanner graphs being identity matrces. The permutation construction utilizes this class to generate respective submatrices.

### Regular

This construction generates a submatrix equivalent to a regular code built according to parameters width = <strong>f</strong>, height = <strong>f</strong>, 1s per col = <strong>v</strong>, construction = <code>populate-columns</code>. 

You can read more about the populate-columns code construction [here](TODO). This construction method was chosen over other regular construction methods because of its ability to enforce a constant column weightage in the prescence of dimension constraints. 

### Quasi-Cyclic

This construction generates a submatrix according to the following schema:

The initial matrix row is created of width <strong>f</strong>, height = 1. This row is populated randomly with <strong>v</strong> 1s. The next following <strong>f</strong> - 1 rows are circular right shifts of the preceeding row.

You can read more about Quasi-Cyclic LDPC Codes [here](https://ieeexplore.ieee.org/document/6145509).

### Permuted Quasi Cuclic

This construction generates a submatrix according to a similar schema:

The initial submatrix row is created of width <strong>f</strong>, height = 1. The first <strong>v</strong> indicies of this row are populated with 1s, the following <strong>f</strong> - 1 rows are merely circular right shifts of the preceeding row.

After achieving the necessary height dimension for the submatrix, the rows are re-ordered according to a random permutation of list [1 - <strong>f</strong>]. Following this is a random permutation of of the columns according to a second random permutation of list [1 - <strong>f</strong>]
