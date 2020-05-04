import MatrixLibraries.Matrix;

import java.util.ArrayList;

public class LDPCCode extends LinearCode {

    public LDPCCode(int n, int c, int r) {
        this.parityCheckMatrix = getParityCheckMatrix(n, c, r);
    }

    public LDPCCode(int w, int h) {

        if (GCD(w, h) == Math.min(w, h) && GCD2(w, h) != 1)
            this.parityCheckMatrix = getParityCheckMatrix(w, h / GCD2(h, w), w / GCD2(h, w));
        else {
            this.parityCheckMatrix = getParityCheckMatrix(w, h / GCD(h, w), w / GCD(h, w));
        }

//        this(w, h / GCD(h, w), w / GCD(h, w));
//        this(w, h / GCD2(h, w), w / GCD2(h, w));
    }

    /**
     * @param n describes the length of the codeword this LDPC code is created to address
     * @param c describes the number of 1s present in each column
     * @param r describes the number of 1s present in each row
     */
    public static Matrix getParityCheckMatrix(int n, int c, int r) {

        //this just ensures that for every 1 in each row there is a fixed number of zeros
        if (n % r != 0) {
            System.err.println("impossible to handle n: " + n + ", r: " + r);
        }

        /**
         * This implementation constructs the appropriate parity matrix by stacking multiple submatrices. Each submatrix contains
         * exactly one 1 per column, so stacking these submatrices fulfills the column requirement (that's what the loop
         * is doing, just stacking these submatrices on top of each other systematically_
         */

        Matrix parityMatrix = null;
        for (int col = 0; col < c; col++) {

            /**
             * Here each submatrix is constructed. Each is an expanded identity matrix, with the columns shuffled. An
             * identity matrix is the initial matrix which is manipulated into the appropriate submatrix because of its property
             * that each column contains only one 1 (this is a property which extends to the developed submatrix). The identity
             * matrix is expanded horizontally by a factor of r (each column is repeated r times), to produce a submatrix of
             * the appropriate dimension (width n, height n/j). This submatrix is then shuffled so that each parity equation
             * represented by the submatrix has a broader coverage of codeword bits (this allows for the decoding process to
             * function more effectively)
             */

            //This is the initial identity matrix. Its height is the important part, it provides each column with exactly one 1 bit
            Matrix identity = Matrix.identityMatrix(n / r);

            //This expands the identity matrix so that the row requirements of the ldpc matrix are fulfilled.
            //Because this matrix will be stacked on top of other matrices like itself, it will cover the entire width of the parity check matrix,
            //thus it needs to fulfill the row requirement of the ldpc matrix
            Matrix expanded = Matrix.expand(identity, r);

            //This shuffles the submatrix to fulfill the functionality outlined in the description
            Matrix paritySubMatrix = Matrix.getColsShuffled(expanded);


            //Stacking of subsequent submatrices is performed to fulfil the column requirement: each submatrix contains exactly one 1 in each of its columns
            //Because of this, c submatrices must be generated and stacked in order to create the final ldpc matrix
            if (parityMatrix == null) {
                parityMatrix = paritySubMatrix;
            } else {
                parityMatrix = Matrix.concatVertical(parityMatrix, paritySubMatrix); //this just vertically combines two matrices
            }
        }

        return parityMatrix;
    }


    //inefficient, but finds second gcd, needed for now
    public static int GCD2(int i, int j) {
        ArrayList<Integer> factors = new ArrayList<>();
        for (int z = 1; z < Math.min(i, j); z++) {
            if (i % z == 0 && j % z == 0) factors.add(z);
        }
        return factors.get(factors.size() - 1);
    }

    //recursive, efficient GCD finder, does not find second gcd
    public static int GCD(int i, int j) {
        return GCDR(i, j, Math.min(i, j));
    }

    public static int GCDR(int i, int j, int previousRemainder) {

        int remainder = Math.max(i, j) % Math.min(i, j);
//        int multiplier = (Math.max(i, j) - remainder) / Math.min(i, j);

        if (remainder == 0) return previousRemainder;
        else return GCDR(Math.min(i, j), remainder, remainder);
    }

    public Matrix getParityCheckMatrix() {
        return parityCheckMatrix;
    }
}
