
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class InputReader {

    public static ArrayList<String> readFile(int day) {
        try {
            ArrayList<String> result = new ArrayList();

            File file = new File("../input/day" + day + ".input");
            FileReader fr = new FileReader(file);
            BufferedReader reader = new BufferedReader(fr);

            String line;
            while ((line = reader.readLine()) != null) {
                result.add(line);
            }

            return result;

        } catch (IOException ex) {
            throw new RuntimeException("Input for day " + day + "missing!", ex);
        }
    }
}
