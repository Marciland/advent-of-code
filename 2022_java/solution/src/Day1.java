
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class Day1 extends Day {

    ArrayList<Integer> summedCalories() {
        ArrayList<String> input;
        try {
            input = InputReader.readFile(1);
        } catch (IOException ex) {
            throw new RuntimeException("Input for day 1 missing!", ex);
        }

        ArrayList<Integer> summedCalories = new ArrayList();
        int sum = 0;

        for (String line : input) {
            if (!line.isBlank()) {
                sum += Integer.parseInt(line);
                continue;
            }
            if (sum != 0) {
                summedCalories.add(sum);
                sum = 0;
            }
        }

        return summedCalories;
    }

    @Override
    public void star1() {
        /*
            sum calories and find the one with the most
         */

        ArrayList<Integer> summedCalories = summedCalories();
        Collections.sort(summedCalories);
        System.out.println(summedCalories.getLast());
    }

    @Override
    public void star2() {
        /*
            Kinda the same, but for the sum of the top3
         */

        ArrayList<Integer> summedCalories = summedCalories();
        Collections.sort(summedCalories);

        int top3 = summedCalories.get(summedCalories.size() - 1) + summedCalories.get(summedCalories.size() - 2) + summedCalories.get(summedCalories.size() - 3);
        System.out.println(top3);
    }
}
