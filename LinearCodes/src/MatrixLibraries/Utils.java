package MatrixLibraries;

import java.util.ArrayList;
import java.util.List;

public class Utils {

    public static ArrayList<Integer> ascendingIntegers(int start, int end) {
        ArrayList<Integer> ascending = new ArrayList<>();
        for (int i = start; i < end; i++) {
            ascending.add(i);
        }
        return ascending;
    }
}
