---
layout: default
title: Protograph code construction
parent: Methods
nav_order: 2
---

# Protograph code construction
## Table of Contents
* [Background](#background)
* [Construction methods](#construction-methods)
  * [peg](#peg) (default)
  * [sum-permutations](#sum-permutations)
  * [quasi-cyclic](#quasi-cyclic)
  * [permuted-quasi-cyclic](#permuted-quasi-cyclic)

## Background

This library includes different constructions for the creation of Protograph-based LDPC Codes. Protograph codes are created through the expansion of a base protograph. The resulting LDPC code matrix is a combination of "submatrices", each submatrix constructed according to the corresponding degree specified in the protograph. Given an expansion factor f, these submatrices are strictly f by f dimensions.

For example assume a protograph whose matrix representation has a width <strong>w</strong> a height <strong>h</strong> an expansion factor <strong>f</strong> and is populated with integers in the following domain: [0, ∞).

The resulting LDPC code would be representable by a <strong>w * f</strong> by <strong>h * f</strong> matrix, where each <strong>f</strong> by <strong>f</strong> scope positioned at <strong>(r, c)</strong> for all <strong>r % f == 0, c % f == 0</strong> within the resulting matrix would correspond to a submatrix whose construction depended on the protograph degree specified at location <strong>(r/f, c/f)</strong>.

The protograph code constructions following are constructions of this submatrix. <strong>f</strong> is used to represent the expansion factor (and thus width of the submatrix) and <strong>v</strong> is used to represent the protograph degree upon which the submatrix construction is to operate.

## Construction methods
### peg

This construction generates a submatrix equivalent to a regular code built according to parameters width = <strong>f</strong>, height = <strong>f</strong>, 1s per col = <strong>v</strong>, construction = <code>peg</code>.

You can read more about the peg code construction [here](./methods-regular.html#peg). This construction method was chosen over other regular construction methods as it is the current state of the art for regular code construction.

### sum-permutations

This construction generates a submatrix the result of a summation of <strong>v</strong> non-overlapping permutation matrices.

Implications:
* the resulting matrix is strictly regular in the weightages of its rows and columns - each permutation matrix adds exactly one node to each row and to each column of the submatrix.

This library provides an api for the handling of the special case of tanner graphs for identity matrices. The permutation construction utilizes this class to generate respective submatrices.

### quasi-cyclic

This construction generates a submatrix according to the following schema:

The initial matrix row is created of width <strong>f</strong>, height = 1. This row is populated randomly with <strong>v</strong> 1s. The next following <strong>f</strong> - 1 rows are circular right shifts of the preceeding row.

You can read more about Quasi-Cyclic LDPC Codes [here](https://ieeexplore.ieee.org/document/6145509).

### permuted-quasi-cyclic

This construction generates a submatrix according to a similar schema:

The initial submatrix row is created of width <strong>f</strong>, height = 1. The first <strong>v</strong> indicies of this row are populated with 1s, the following <strong>f</strong> - 1 rows are merely circular right shifts of the preceeding row.

After achieving the necessary height dimension for the submatrix, the rows are re-ordered according to a random permutation [0, <strong>f</strong>). Following this is a random permutation of of the columns according to another random permutation [0, <strong>f</strong>).
