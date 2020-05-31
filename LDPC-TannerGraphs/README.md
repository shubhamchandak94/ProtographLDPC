# Implemented Constructions of Regular LDPC matrices 
Where n: codeword length, r: weight of each row, c: weight of each column

## Gallager's Construciton
The eventual parity check matrix is a combination of multiple matrices of column weight 1 and row weight r.
Each of these submatrices is constructed such that each row contains contains r 1's and each column contains one 1. <br/>
<br/>
Example for n=10, r=5, c=3 <br/>
1111100000 <br/>
0000011111 <br/>

Clearly, the height of the submatrix is dependent on n and r and no aspect of this matrix is dependent on c.
The matrix's columns are then shuffled to enable increased protections.

Exactly c amount of these matrices are stacked vertically to create the cumulativeLDPC matrix.

## Radford Neal's construction
An empty matrix is constructed initially, whose columns are populated left to right in the construction process. Every
row has available positions. 

Repeat for every column, or until no more rows are free for increased weightage:
- Choose c random rows from the available rows, place 1's in these locations.
- If for any of the selected rows the weight equals r, remove these rows from the list of available row for future columns
