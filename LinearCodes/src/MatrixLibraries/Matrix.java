package MatrixLibraries;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

//developed for block codes, all summation operations are bitwise
public class Matrix {

    private double[][] matrix;

    public Matrix(double[][] matrix) {
        this.matrix = matrix;
    }

    public int height() {
        return matrix.length;
    }

    public int width() {
        return matrix[0].length;
    }

    public Matrix(int width, int height) {
        matrix = new double[height][width];
    }

    public void set(int r, int c, double v) {
        matrix[r][c] = v;
    }

    public double get(int r, int c) {
        return matrix[r][c];
    }

    public double[] getRow(int r) {
        return matrix[r];
    }

    public double[] getCol(int c) {
        double[] col = new double[matrix.length];
        for (int i = 0; i < matrix.length; i++) {
            col[i] = matrix[i][c];
        }
        return col;
    }

    public void setRow(int r, double[] row) {
        matrix[r] = row;
    }

    public void setCol(int c, double[] col) {
        assert height() == col.length;
        for (int i = 0; i < height(); i++) {
            matrix[i][c] = col[c];
        }
    }

    private static double dotProduct(double[] u, double[] v) {
        assert u.length == v.length;
        double out = 0;
        for (int i = 0; i < u.length; i++) {
            out += u[i] * v[i];
        }
        return out % 2;
    }

    public static Matrix multiply(Matrix u, Matrix v) {
        assert u.width() == v.height();
        Matrix product = new Matrix(v.width(), u.width());
        for (int r = 0; r < product.height(); r++) {
            for (int c = 0; c < product.width(); c++) {
                product.set(r, c, dotProduct(u.getRow(r), v.getCol(c)));
            }
        }
        return product;
    }

    public Matrix transpose() {
        Matrix out = new Matrix(height(), width());
        for (int r = 0; r < height(); r++) {
            for (int c = 0; c < width(); c++) {
                out.set(c, r, matrix[r][c]);
            }
        }
        return out;
    }

    public static Matrix identityMatrix(int sideLength) {
        Matrix identity = new Matrix(sideLength, sideLength);
        for (int r = 0; r < identity.height(); r++) {
            for (int c = 0; c < identity.width(); c++) {
                if (c == r) identity.set(r, c, 1);
            }
        }
        return identity;
    }

    public static Matrix concatHorizontal(Matrix u, Matrix v) {
        assert u.height() == v.height();
        Matrix out = new Matrix(u.width() + v.width(), u.height());
        for (int r = 0; r < u.height(); r++) {
            for (int c = 0; c < u.width(); c++) {
                out.set(r, c, u.get(r, c));
            }
        }
        for (int r = 0; r < v.height(); r++) {
            for (int c = u.width(); c < u.width() + v.width(); c++) {
                out.set(r, c, v.get(r, c - u.width()));
            }
        }
        return out;
    }

    public static Matrix concatVertical(Matrix u, Matrix v) {
        return concatHorizontal(u.transpose(), v.transpose()).transpose();
    }

    public static Matrix expand(Matrix u, int reps) {
        Matrix expanded = new Matrix(u.width() * reps, u.height());
        for (int r = 0; r < u.height(); r++) {
            for (int c = 0; c < u.width(); c++) {
                for (int rep = 0; rep < reps; rep++) {
                    expanded.set(r, c * reps + rep, u.get(r, c));
                }
            }
        }
        return expanded;
    }

    public void flipAllBits(int rstart, int cstart, int rend, int cend) {
        for (int r = rstart; r < rend; r++) {
            for (int c = cstart; c < cend; c++) {
                assert (matrix[r][c] == 1 || matrix[r][c] == 0);
                if (matrix[r][c] == 1) matrix[r][c] = 0;
                else if (matrix[r][c] == 0) matrix[r][c] = 1;
            }
        }
    }

    public static Matrix getRowsShuffled(Matrix u) {
        ArrayList<Integer> indices = Utils.ascendingIntegers(0, u.height());
        Collections.shuffle(indices);

        Matrix out = new Matrix(u.width(), u.height());
        for (int r = 0; r < out.height(); r++) {
            out.setRow(r, u.getRow(indices.get(r)));
        }
        return out;
    }

    public static Matrix getColsShuffled(Matrix u) {
        return getRowsShuffled(u.transpose()).transpose();
    }

    public Matrix getSubMatrix(int rstart, int cstart, int rend, int cend) {
        Matrix slice = new Matrix(cend - cstart, rend - rstart);
        for (int r = rstart; r < rend; r++) {
            for (int c = cstart; c < cend; c++) {
                slice.set(r - rstart, c - cstart, matrix[r][c]);
            }
        }
        return slice;
    }

    public String toString() {
        StringBuilder out = new StringBuilder();
        for (int r = 0; r < matrix.length; r++) {
            for (int c = 0; c < matrix[r].length; c++) {
                out.append((int) matrix[r][c]).append(" ");
            }
            if (r < matrix.length - 1) out.append("\n");
        }
        return out.toString();
    }

    /**
     * Converts matrix to LDPC-SandboxLibrary readable under make-pchk
     */
    public String getCExecutable(String outputFile) {
        StringBuilder out = new StringBuilder();
        out.append("./make-pchk ");
        out.append(outputFile).append(" ");
        out.append(this.height()).append(" ");
        out.append(this.width()).append(" ");
        for (int r = 0; r < height(); r++) {
            for (int c = 0; c < width(); c++) {
                if (this.get(r, c) == 1) {
                    out.append(r).append(":").append(c).append(" ");
                }
            }
        }
        return out.toString().substring(0, out.toString().length() - 1);
    }
}
