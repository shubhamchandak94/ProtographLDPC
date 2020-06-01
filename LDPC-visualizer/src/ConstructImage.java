import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class ConstructImage {
    public static void main(String[] args) {
        try {
            BufferedImage parsedImage = ImageParser.parseImage(ImageParser.read(args[0]));
            ImageIO.write(parsedImage, "png", new File(args[1]));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
