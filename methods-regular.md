---
layout: default
title: Parity check construction - regular
parent: Methods
nav_order: 1
---

# Regular-type LDPC Code Constructions

## Table of Contents
* [background](./methods-regular.html#background)
* [gallager](./methods-regular.html#gallager)
* [populate-columns](./methods-regular.html#populate-columns)
* [populate-rows](./methods-regular.html#populate-rows)

### Background

Unlike Protograph-based LDPC Constructions, all regular code constructions included in this library directly construct the conclusive LDPC Code.

### Gallager

Proposed by Robert Gallager during the conception phase of LDPC codes, this construction merges a series of submatrix codes to produce the cumulative LDPC code. 

Given a code width <strong>n</strong>, a constant row weightage <strong>r</strong>, and a constant column weightage <strong>c</strong>, <strong>c</strong> independent matrices each of constant column weight 1 are generated individually.

Because of the property that all strictly regular codes share: <strong>height = width (c / r)</strong>, the height of these submatrices is equivalent equivalent by <strong>w (width)</strong> / <strong>r</strong>. 

These <strong>c</strong> <strong>w</strong> by <strong>w / r</strong> matrices are populated according to the following algorithm:

```sh
for h in range([0, w/r - 1)):
    for x in range([0, r)):
        populate(submatrix[h * r + x][h]) 
```

The submatrix thus derived is then permuted in its columns according to a random permutation [0, <strong>w</strong>)

This construction enforces strict regularity on the resulting code. There is a trade-off: the condition <strong>height = width (c / r)</strong> does not hold for all variable values <strong>w</strong>, <strong>r</strong>, <strong>c</strong>. The library implementation refuses construction arguments that do not fit this regularity condition. 

The cumulative LDPC code consists of a vertical merging of these individual submatrices.

### populate-columns

This construction generates an LDPC code according to the following schema:

1. An empty matrix is created of dimension <strong>w</strong> by <strong>h</strong>.
2. A list l of length <strong>w * c</strong> is created and popualted according to the following:

```sh
for i in range([0, w * c)):
    l[i] = i % h
```

Because this list always consists of <strong>w</strong> sets of <strong>[0, c)</strong>, the list is guaranteed to be of a length n such that n entries can be placed within the matrix without compromising the vertical regularity.

This enforcement of vertical regularity comes at the expense of the horizontal regularity: no enforcement of constant row weightages is maintained in this implementation. In doing so, this algorithm provides a code by which decoding is made slightly more even. Every codeword bit is protected by an equal number of parity check equations, therefore the distribution of code protection tends to uniformity.

### populate-rows

The populate-columns matrix performs the same operations. Simply put, if the blank code before population is transposed and populated according to populate-columns, then the result is transposed, the effect will be the same as if the matrix were constructed using populate-rows.

As is suggested, this construction enforces constant row weightages on the resulting code at the expense of the vertical regularity.

### peg
// TODO
