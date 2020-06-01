import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;

public class ImageParser {

    private static int dimensionSize = 30;

    public static BufferedImage parseImage(String image) {

        //may have to manually set these values of decoding does not leave these numbers 100% accurate
        int width = decompressed(image.substring(0, dimensionSize));
        int height = decompressed(image.substring(dimensionSize, 2 * dimensionSize));

        BufferedImage parsedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);

        int index = dimensionSize * 2;
        int row = 0;
        int col = 0;
        while (index + 24 < image.length()) {
            Color pixel = new Color(
                    decompressed(image.substring(index, index + 8)),
                    decompressed(image.substring(index + 8, index + 16)),
                    decompressed(image.substring(index + 16, index + 24))
            );
            parsedImage.setRGB(col, row, pixel.getRGB());

            index += 24;
            col++;

            if (col == width) {
                row++;
                col = 0;
            }

        }
        return parsedImage;
    }

    private static int decompressed(String compressed) {
        return Integer.parseInt(compressed, 2);
    }

    /**
     * converts given image to a string containing only binary information
     */
    public static String parseImage(BufferedImage image) {
        StringBuilder out = new StringBuilder();
        out.append(compressed(image.getWidth(), dimensionSize));
        out.append(compressed(image.getHeight(), dimensionSize));
        for (int r = 0; r < image.getHeight(); r++) {
            for (int c = 0; c < image.getWidth(); c++) {
                Color pixel = new Color(image.getRGB(c, r));
                out.append(compressed(pixel.getRed(), 8));
                out.append(compressed(pixel.getGreen(), 8));
                out.append(compressed(pixel.getBlue(), 8));
            }
        }
        return out.toString();
    }

    /**
     * length = 8 for colors, 30 for dimensions (first 60 bits describe dimension)
     */
    private static String compressed(int j, int length) {
        StringBuilder out = new StringBuilder();
        String rep = Integer.toString(j, 2);
        for (int i = 0; i < length - rep.length(); i++) {
            out.append("0");
        }
        return out.append(rep).toString();
    }

    public static void write(String image, String filepath) {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(new File(filepath)));
            writer.write(image);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void write(BufferedImage image, String filepath) {
        try {
            ImageIO.write(image, "png", new File(filepath));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String read(String filepath) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(new File(filepath)));
            return reader.readLine().replace("\n", "").replace(" ", "");
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static double percentDifference(String str1, String str2) {
        if (str1.length() != str2.length()) return -1;
        double count = 0;
        for (int i = 0; i < str1.length(); i++) {
            if (str1.charAt(i) != str2.charAt(i)) count++;
        }
        return count / str1.length();
    }

    public static void main(String[] args) {
        try {
            BufferedImage image = ImageIO.read(new File(args[0]));

            String imageAsString = parseImage(image);
            write(imageAsString, "fileAsString");

            BufferedImage parsedImage = parseImage(read("fileAsString"));
            BufferedImage corruptedImage = parseImage(read("corrupted"));

            JFrame frame = new JFrame();
            frame.getContentPane().add(new JLabel(new ImageIcon(parsedImage)));
            frame.pack();
            frame.setVisible(true);

            JFrame frame2 = new JFrame();
            frame2.getContentPane().add(new JLabel(new ImageIcon(corruptedImage)));
            frame2.pack();
            frame2.setVisible(true);

            try {Thread.sleep(10000);} catch (InterruptedException ignored) {}



        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

/*
create parity check matrices from all three methods
convert image to string
encode string
corrupt string
display image before corruption
fix image for each parity check matrix
display all images
 */
