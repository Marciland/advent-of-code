
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class Day11 extends Day {

    ArrayList<Monkey> parseInput(ArrayList<String> input) {
        ArrayList<Monkey> monkeys = new ArrayList<Monkey>();

        Monkey monkey = new Monkey();
        for (String line : input) {
            if (line.contains("Monkey")) {
                monkey = new Monkey();
                continue;
            }

            if (line.isBlank()) {
                monkeys.add(monkey);
                continue;
            }

            if (line.contains("items")) {
                List<String> items = new ArrayList<String>(Arrays.asList(line.split(",")));
                String starting = items.remove(0);
                monkey.items.add(Integer.parseInt(starting.split(": ")[1]));
                for (String item : items) {
                    monkey.items.add(Integer.parseInt(item.trim()));
                }
                continue;
            }

            if (line.contains("Operation")) {
                String[] parts = line.split("=");
                String[] op = parts[1].trim().split(" ");
                monkey.operation.operator = op[1];
                monkey.operation.operand = op[2];
                continue;
            }

            if (line.contains("Test")) {
                String[] parts = line.split("by");
                monkey.test = Integer.parseInt(parts[1].trim());
                continue;
            }

            if (line.contains("true")) {
                String[] parts = line.split(" ");
                monkey.trueTarget = Integer.parseInt(parts[parts.length - 1]);
                continue;
            }

            if (line.contains("false")) {
                String[] parts = line.split(" ");
                monkey.falseTarget = Integer.parseInt(parts[parts.length - 1]);
                continue;
            }
        }
        monkeys.add(monkey);

        return monkeys;
    }

    class Operation {

        String operator;
        String operand;

        public int inspect(int item) {
            int operand;
            if (this.operand.equals("old")) {
                operand = item;
            } else {
                operand = Integer.parseInt(this.operand);
            }

            switch (this.operator) {
                case "*" -> {
                    item *= operand;
                }
                case "/" -> {
                    item /= operand;
                }
                case "+" -> {
                    item += operand;
                }
                case "-" -> {
                    item -= operand;
                }
            }

            return item;
        }
    }

    class Monkey {

        ArrayList<Integer> items = new ArrayList<>();
        int inspected = 0;
        Operation operation = new Operation();

        int test;
        int trueTarget;
        int falseTarget;

        public void takeTurn(ArrayList<Monkey> monkeys) {
            for (int item : new ArrayList<Integer>(this.items)) {
                int newItem = this.operation.inspect(item);
                this.inspected++;
                newItem = (int) Math.floor(newItem / 3);

                int target;
                if (this.test(newItem)) {
                    target = this.trueTarget;
                } else {
                    target = this.falseTarget;
                }

                monkeys.get(target).items.add(newItem);

                Iterator<Integer> it = this.items.iterator();
                while (it.hasNext()) {
                    if (it.next() == item) {
                        it.remove();
                        break;
                    }
                }
            }
        }

        boolean test(int item) {
            return item % this.test == 0;
        }
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
         * Monkey business after 20 rounds.
         * two most active monkeys inspected multiplied
         */

        ArrayList<Monkey> monkeys = parseInput(input);

        for (int round = 0; round < 20; round++) {
            for (Monkey monkey : monkeys) {
                monkey.takeTurn(monkeys);
            }
        }

        int mostActive = 0;
        int secondMostActive = 0;

        for (Monkey monkey : monkeys) {
            if (monkey.inspected > mostActive) {
                secondMostActive = mostActive;
                mostActive = monkey.inspected;
            }
        }

        System.out.println(mostActive * secondMostActive);
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
         * Same, 10000 rounds and no relief (divided by 3)
         */
        ArrayList<Monkey> monkeys = parseInput(input);

        for (long round = 0; round < 10000; round++) {
            for (Monkey monkey : monkeys) {
                // remove relief, fix overflowing
                monkey.takeTurn(monkeys);
            }
        }

        long mostActive = 0;
        long secondMostActive = 0;

        for (Monkey monkey : monkeys) {
            if (monkey.inspected > mostActive) {
                secondMostActive = mostActive;
                mostActive = monkey.inspected;
            }
        }

        System.out.println(mostActive * secondMostActive);
    }
}
