
import java.util.ArrayList;

public class Day3 extends Day {

    class Rucksacks {

        ArrayList<String> left;
        ArrayList<String> right;

        public Rucksacks(ArrayList<String> input) {
            this.left = new ArrayList();
            this.right = new ArrayList();

            for (String line : input) {
                assert line.length() % 2 == 0;
                this.left.add(line.substring(0, line.length() / 2));
                this.right.add(line.substring(line.length() / 2, line.length()));
            }
        }

        public char getMatch(int index) {
            String leftCompartment = this.left.get(index);
            String rightCompartment = this.right.get(index);

            for (char c : leftCompartment.toCharArray()) {
                if (rightCompartment.contains(Character.toString(c))) {
                    return c;
                }
            }

            throw new RuntimeException("Cannot find matching chars");
        }

        public static int getValue(char c) {
            int unicode = (int) c;
            if (Character.isLowerCase(c)) {
                return unicode - 96;
            } else {
                return unicode - 38;
            }
        }

    }

    class Groups {

        ArrayList<String> firsts;
        ArrayList<String> seconds;
        ArrayList<String> thirds;

        public Groups(ArrayList<String> input) {
            this.firsts = new ArrayList();
            this.seconds = new ArrayList();
            this.thirds = new ArrayList();

            int counter = 1;
            for (String line : input) {
                switch (counter) {
                    case 1 -> {
                        this.firsts.add(line);
                        counter = 2;
                    }
                    case 2 -> {
                        this.seconds.add(line);
                        counter = 3;
                    }
                    case 3 -> {
                        this.thirds.add(line);
                        counter = 1;
                    }
                }
            }
        }

        public char getMatch(int index) {
            String first = this.firsts.get(index);
            String second = this.seconds.get(index);
            String third = this.thirds.get(index);

            for (char c : first.toCharArray()) {
                if (!second.contains(Character.toString(c))) {
                    continue;
                }
                if (!third.contains(Character.toString(c))) {
                    continue;
                }
                return c;
            }

            throw new RuntimeException("Cannot find matching chars");
        }
    }

    @Override
    public void star1() {
        /*
            Split in half, then find doubles.

            a = 1
            ...
            z = 26
            A = 27
            ...
            Z = 52

            sum the priority based on table

                using unicode and subtracting the fitting values
                https://en.wikipedia.org/wiki/List_of_Unicode_characters
         */
        ArrayList<String> input = InputReader.readFile(3);
        Rucksacks rucksacks = new Rucksacks(input);

        int summedPriority = 0;
        for (int i = 0; i < rucksacks.left.size(); i++) {
            char match = rucksacks.getMatch(i);
            summedPriority += Rucksacks.getValue(match);
        }

        System.out.println(summedPriority);
    }

    @Override
    public void star2() {
        /*
            find in groups of 3 instead of left and right
         */
        ArrayList<String> input = InputReader.readFile(3);
        Groups groups = new Groups(input);

        int summedPriority = 0;
        for (int i = 0; i < groups.firsts.size(); i++) {
            char match = groups.getMatch(i);
            summedPriority += Rucksacks.getValue(match);
        }

        System.out.println(summedPriority);
    }
}
