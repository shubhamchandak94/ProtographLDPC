import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

public class MakePCHK {

    public static void main(String[] args) {

        LDPCCode code;
        if (args.length == 3) {
            //construct based on width, height
            code = new LDPCCode(Integer.parseInt(args[1]), Integer.parseInt(args[2]));
        } else if (args.length == 4) {
            //construct based on n, r, c
            code = new LDPCCode(Integer.parseInt(args[1]), Integer.parseInt(args[2]), Integer.parseInt(args[3]));
        } else {
            System.out.println("Usage: MakePCHK someOutputFile [n c r, w h]");
            return;
        }
        String toWrite = code.getParityCheckMatrix().getCExecutable(args[0]);
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("transfer.txt"));
            writer.write(toWrite);
            writer.close();
        } catch (IOException e) {
            System.out.println("could not create or interact with transfer file");
        }
    }
}
