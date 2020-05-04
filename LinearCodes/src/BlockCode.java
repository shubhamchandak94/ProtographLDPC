import MatrixLibraries.Matrix;

public class BlockCode extends LinearCode {

    public BlockCode(int messageLength) {
        Matrix parityCheckMatrix = new Matrix(2 * messageLength - 1, messageLength - 1);
        for (int r = 0; r < parityCheckMatrix.height(); r++) {
            parityCheckMatrix.set(r, r + 1, 1);
        }
        for (int r = 0; r < parityCheckMatrix.height(); r++) {
            for (int c = messageLength; c < 2 * messageLength - 1; c++) {
                if (r == c - messageLength) parityCheckMatrix.set(r, c, 1);
            }
        }
        parityCheckMatrix.flipAllBits(0, 0, parityCheckMatrix.height(), messageLength);
        this.parityCheckMatrix = parityCheckMatrix;

        Matrix transposedParity = parityCheckMatrix.getSubMatrix(0, 0, parityCheckMatrix.height(), messageLength).transpose();
        Matrix identity = Matrix.identityMatrix(transposedParity.height());
        this.generatorMatrix = Matrix.concatHorizontal(identity, transposedParity);
    }

    public Matrix getParityCheckMatrix() {return parityCheckMatrix;}

    public Matrix getGeneratorMatrix() {return generatorMatrix;}
}
