---
layout: default
title: Sample protographs
parent: Methods
nav_order: 3
---

# Protographs

In order to generate a protograph ldpc code, a protograph file must be supplied to the make-pchk program. <br>
This file is always of the following format:

```sh
n_checks n_bits
transmitted_bits [list of bits NOT punctured]
switch
protograph representation
```
If <code>switch</code> is sparse, <code>protograph representation</code> is given by a list coordinates where list elements are specified by newline characters. Each list element contains three integers: the row value within the protograph matrix, the column value within the protograph matrix, and the entry value at that given coordinate location.

If <code>switch</code> is dense, <code>protograph representation</code> is given by the direct matrix representation of the protograph.

Consider the following example where a protograph is defined by the following matrix:
```sh
0 0 1 0 2
1 1 0 1 3
1 2 0 2 1
```
If <code>switch</code> is toggled to dense, this is the direct text that would replace <code>protograph representation</code> in the protograph template file. If <code>switch</code> is toggled to sparse, the following text would be the replacement for <code>protograph representation</code>:

```sh
1 3 1
1 5 2
2 1 1
2 2 1
2 4 1
2 5 3
3 1 1
3 2 2
3 4 2
3 5 1
```

You can find a list of example protograph files already implemented for your convenience [here](https://github.com/shubhamchandak94/ProtographLDPC/tree/master/sample-protographs).



