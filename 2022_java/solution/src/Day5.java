
import java.util.ArrayList;
import java.util.List;

public class Day5 extends Day {

    class Stacks {

        ArrayList<Stack> stacks;

        public Stacks(List<String> stacksInput) {
            this.stacks = new ArrayList();

            for (String index : stacksInput.removeLast().split(" ")) {
                if (index.isBlank()) {
                    continue;
                }
                this.stacks.add(new Stack());
            }

            for (String line : stacksInput.reversed()) {
                ArrayList<Character> crates = new ArrayList();

                for (int i = 1; i < line.length(); i += 4) {
                    crates.add(line.charAt(i));
                }

                for (int i = 0; i < crates.size(); i++) {
                    if (Character.isWhitespace(crates.get(i))) {
                        continue;
                    }

                    this.stacks.get(i).push(crates.get(i));
                }
            }
        }

        public String solution() {
            StringBuilder builder = new StringBuilder();

            for (Stack stack : this.stacks) {
                builder.append(stack.crates.getLast());
            }

            return builder.toString();
        }
    }

    class Stack {

        ArrayList<Character> crates;

        public Stack() {
            this.crates = new ArrayList();
        }

        public void push(char crate) {
            this.crates.add(crate);
        }

        public char pop() {
            return this.crates.removeLast();
        }

        public List<Character> pop_many(int amount) {
            ArrayList<Character> popped_crates = new ArrayList();

            for (int i = 0; i < amount; i++) {
                char crate = this.crates.removeLast();
                popped_crates.add(crate);
            }

            return popped_crates.reversed();
        }

        public void push_many(List<Character> crates) {
            for (Character crate : crates) {
                this.crates.add(crate);
            }
        }

    }

    class Instruction {

        int amount;
        int from;
        int to;

        public Instruction(String line) {
            String[] instructions = line.split(" ");
            for (int i = 0; i < instructions.length; i += 2) {
                switch (instructions[i]) {
                    case "move" -> {
                        this.amount = Integer.parseInt(instructions[i + 1]);
                    }
                    case "from" -> {
                        this.from = Integer.parseInt(instructions[i + 1]) - 1;
                    }
                    case "to" -> {
                        this.to = Integer.parseInt(instructions[i + 1]) - 1;
                    }
                }
            }
        }

        public void modify(Stacks stacks) {
            for (int i = 0; i < this.amount; i++) {
                char crate = stacks.stacks.get(this.from).pop();
                stacks.stacks.get(this.to).push(crate);
            }
        }

        public void modify9001(Stacks stacks) {
            List<Character> crates = stacks.stacks.get(this.from).pop_many(this.amount);
            stacks.stacks.get(this.to).push_many(crates);
        }
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
        Rearrange crates based on instructions

        Crates contain a char
        Which crates are on top?
        Solution is a string
         */
        int sep = 0;
        for (int i = 0; i < input.size(); i++) {
            if (input.get(i).isBlank()) {
                sep = i;
                break;
            }
        }
        List<String> stacksInput = input.subList(0, sep);
        Stacks stacks = new Stacks(stacksInput);

        List<String> instructionInput = input.subList(sep, input.size());
        ArrayList<Instruction> instructions = new ArrayList();
        for (String line : instructionInput) {
            instructions.add(new Instruction(line));
        }

        for (Instruction instruction : instructions) {
            instruction.modify(stacks);
        }

        System.out.println(stacks.solution());
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
            Move amount at once (keep order of moved crates)
         */
        int sep = 0;
        for (int i = 0; i < input.size(); i++) {
            if (input.get(i).isBlank()) {
                sep = i;
                break;
            }
        }
        List<String> stacksInput = input.subList(0, sep);
        Stacks stacks = new Stacks(stacksInput);

        List<String> instructionInput = input.subList(sep, input.size());
        ArrayList<Instruction> instructions = new ArrayList();
        for (String line : instructionInput) {
            instructions.add(new Instruction(line));
        }

        for (Instruction instruction : instructions) {
            instruction.modify9001(stacks);
        }

        System.out.println(stacks.solution());
    }
}
