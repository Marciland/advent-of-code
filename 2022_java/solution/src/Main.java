
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        int n = 11;

        Day day = getDay(n);
        ArrayList<String> input = InputReader.readFile(n);

        day.star1(input);
        day.star2(input);
    }

    private static Day getDay(int day) {
        switch (day) {
            case 1 -> {
                return new Day1();
            }
            case 2 -> {
                return new Day2();
            }
            case 3 -> {
                return new Day3();
            }
            case 4 -> {
                return new Day4();
            }
            case 5 -> {
                return new Day5();
            }
            case 6 -> {
                return new Day6();
            }
            case 7 -> {
                return new Day7();
            }
            case 8 -> {
                return new Day8();
            }
            case 9 -> {
                return new Day9();
            }
            case 10 -> {
                return new Day10();
            }
            case 11 -> {
                return new Day11();
            }
            default ->
                throw new IllegalArgumentException("Invalid day: " + day);
        }
    }
}
