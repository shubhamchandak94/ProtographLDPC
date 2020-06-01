import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class ConvertFileToString {
    public static void main(String[] args) {
        try {
            BufferedImage image = ImageIO.read(new File(args[0]));
            String imageAsString = ImageParser.parseImage(image);
            ImageParser.write(imageAsString, args[1]);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
