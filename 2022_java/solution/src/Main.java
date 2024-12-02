
public class Main {

    public static void main(String[] args) {
        Day day = getDay(4);
        day.star1();
        day.star2();
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
            default ->
                throw new IllegalArgumentException("Invalid day: " + day);
        }
    }
}
