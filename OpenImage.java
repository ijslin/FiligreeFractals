import ij.*;
import ij.io.*;

public class OpenImage {
    public static void main (String [] args) {
        ImageJ ij = new ImageJ();
        Object image = ij.io.open("/Users/marcobresciani/Documents/PycharmProjects/fractalsFiligree/images/filigrees/Corale1/C1-2r-Opening V-cropped.jpg");
    }
}
