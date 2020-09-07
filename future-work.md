---
layout: default
title: Future work
nav_order: 5
---
# Future work
LDPC codes, and protograph codes in particular, are areas of active research and we intend to provide an easy-to-use open source library to enable widespread use of these codes in the wider community. There are several features that are not currently implemented in the library and we briefly mention a few of those below as future work. We hope to incorporate some of these in the future versions.
- **Efficient encoding and optimized quasi-cyclic construction**: Certain protograph constructions such as the quasi-cyclic (QC) construction allows for low-complexity encoding (e.g., see [Mitchell et al. (2014)](https://ieeexplore.ieee.org/document/6089477)) which are important for certain applications, and are widely used in the standards (deep space, 5G, etc.). But QC-LDPC codes have issues with minimum distance and error floors, so the construction needs to be done carefully to get the best results.
- **Protograph design and optimization**: While commonly used protograph codes like AR4JA with certain nice properties can be applied to several channels, better results can generally be obtained by optimizing the protograph for the specific channel. Protograph design and optimization has been an active research area (e.g., see [Fang et al. (2016)](https://ieeexplore.ieee.org/abstract/document/7112076)) but there is a lack of open source implementations for the task.
