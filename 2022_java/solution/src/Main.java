
public class Main {

    public static void main(String[] args) {
        Day day = getDay(2);
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
            default ->
                throw new IllegalArgumentException("Invalid day: " + day);
        }
    }
}
