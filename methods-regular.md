---
layout: default
title: Regular code construction
parent: Methods
nav_order: 1
---

# Regular code construction

## Table of Contents
* [Background](#background)
* [Construction methods](#construction-methods)
  * [peg](#peg) (default)
  * [gallager](#gallager)
  * [populate-columns](#populate-columns)
  * [populate-rows](#populate-rows)

## Background

We describe below the parity check construction methods available for regular code construction in this library. Note that puncturing is not considered here, since it is applied after the code construction. For the construction methods provided by the base library, see the help for the [`make-ldpc`](https://shubhamchandak94.github.io/LDPC-codes/pchk.html#make-ldpc) command.

## Construction methods
For all the construction methods, the input parameters are:
- `n`: code width/number of variable nodes/number of bits in a codeword
- `m`: code height/number of check nodes
- `c`: column weights (number of 1s per column of parity check matrix)

Recall that the output parity check matrix has dimensions `m x n`. Thus, these parameters also determine the number of 1s per row of the matrix (row weight), which is `r = n x c / m`. Such a code is usually denoted as a `(c,r)`-regular code. When this quantity is not an integer, a perfectly regular code is not possible, and there is some variability in the row or column weights depending on the construction method. The number of message bits is given by `n-m` and hence the rate of the code is given by `(n-m)/n`. Here are two simple examples:
- `n=4000, m=3000, c=3`: We can calculate `r = 4`, hence we have a `(3,4)`-regular code. The number of message bits is `4000-3000=1000` and the rate is `1/4`.
- `n=1500, m=1000, c=3`: We can calculate `r = 4.5`, hence this is not a perfectly regular code and either the row weights or the column weights (or both) will be variable. The number of message bits is `1500-1000=500` and the rate is `1/3`.


### peg
Progressive Edge Growth (PEG) ([Hu et al., 2005](https://ieeexplore.ieee.org/document/1377521)) is the default construction method for regular code construction in this library. This algorithm is an efficient greedy algorithm that constructs graphs (corresponding to parity check matrices) with large girth (i.e., lack short cycles). Note that the absence of shoort cycles is important to ensure the success of the message passing decoder, both theoretically and empirically. We refer the reader to the reference provided earlier for details on this algorithm. The algorithm focuses on ensuring constant column weight of `c`, with as constant row weights as possible. As discussed in the repository [here](https://github.com/shubhamchandak94/ProtographLDPC/tree/master/peg), we reused the implementation provided by the authors at <http://www.inference.org.uk/mackay/PEG_ECC.html>. Due to the complexity of the `peg` algorithm, the base library construction (with parameters `evenboth no4cycle`) or one of the other three constructions in this library might be the best option when constructing extremely large codes with codeword lengths above ~100,000.

### gallager

**WARNING: This construction requires that `m/c` (`= n/r`) is an integer.**

Proposed by Robert Gallager during the conception phase of LDPC codes, this construction concatenates a series of submatrix codes to produce the cumulative LDPC code. Each submatrix has size `m/c x n` and we stack `c` such matrices on top of each other to get the final parity check matrix. The construction ensures that each submatrix has constant row weight of `r` and constant column weight of `1`, which lead to the desired weights for the final matrix.

The construction of such a submatrix can be explained through an example. Let `n = 20, m = 15, c = 3, r = 4`. So the submatrix has dimension `5 x 20` and has constant row weight of `4`. We start with the following submatrix formed by concatenating `4` identity matrices of size `5 x 5`.
```
1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0
0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1
```

Then we perform a random permutation of the columns of this matrix to get the desired submatrix (with independent permutations applied for different submatrices). For example, we might obtain the following random `5 x 20` submatrix with constant row weight of `4` and constant column weight of `1`.
```
0 1 1 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 1 0 1 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0 0 0 0 0 0 1 1 0 0 0 0
1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 1 0 0 0 0 0 0 1 0 1 0 0 0 0 0 1
```

### populate-columns

This construction generates an LDPC code according to the following steps:

1. An empty matrix of dimensions `m x n` is created.
2. A list of length `n x c` is created and populated according to the following:

    ```
    for i in 0, 1, ..., n x c - 1:
        available_indices[i] = i % m
    ```

    Observe that this list contains the entries from `0` to `m-1`, each repeated  `r` times on average (might have some variation when `r = n x c / m` is not an integer). This list denotes the potential check node connections to the variable nodes, and is called `available_indices`.

3. For each column:  
    i. Select random entries from `available_indices` until we can get `c` unique entries.  
    ii. For each such index found, set the corresponding position of the column to 1, and remove the index from `available_indices`.  
    iii. If less than `c` unique entries are present in `available_indices`, choose random positions on the column to set to 1 in order to ensure column weight of `c`.

This algorithm enforces that each column has `c` 1s. However, the number of 1s per row can vary because of two reasons, (i) `r = n x c / m` might not be integral and hence the `available_indices` might have higher repetition of certain indices, and (ii) due to the random assigment process, the columns towards the end might lead to non-uniform assignment to rows (Step 3.iii above). Having constant column weight is usually preferable since every codeword bit is protected by an equal number of parity check equations.

### populate-rows

This is similar to the `populate columns` construction above, except that the `available_indices` has entries in `0` to `n-1`, and the matrix is filled row by row, ensuring that each row has `⌊r⌋ = ⌊n x c / m⌋` 1s. This construction focuses on generating a matrix with constant row weights and might lead to variable column weights, especially when `n x c / m` is not an integer.
