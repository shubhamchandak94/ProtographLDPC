### Progressive Edge Growth (PEG) algorithm
PEG is an algorithm for constructing parity check matrices avoiding short cycles (for details see reference below). We use this in the regular code construction and in the submatrix construction for protograph codes (see the [documentation](https://shubhamchandak94.github.io/ProtographLDPC/methods.html)). We use the implementation provided at http://www.inference.org.uk/mackay/PEG_ECC.html (patched version) and thank the developers for making this available. Note that this library provides functionalities beyond those used in this work, including ability to handle irregular codes and ability to specify target girth.

We made some minor changes to the code:
- use modern random number generator and provide option to use a seed
- Disable generation of leftHandGirth.log in quiet mode

#### Reference
Hu, Xiao-Yu, Evangelos Eleftheriou, and Dieter-Michael Arnold. “Regular and irregular progressive edge-growth tanner graphs.” _IEEE Transactions on Information Theory_ 51.1 (2005): 386-398.
