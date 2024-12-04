
import java.util.ArrayList;
import java.util.List;

public class Day9 extends Day {

    ArrayList<Instruction> parseInput(ArrayList<String> input) {
        ArrayList<Instruction> instructions = new ArrayList();
        for (String line : input) {
            String[] parts = line.split(" ");
            assert parts.length == 2;

            instructions.add(new Instruction(parts[0], Integer.parseInt(parts[1])));
        }

        return instructions;
    }

    class Instruction {

        String direction;
        int steps;

        public Instruction(String direction, int steps) {
            this.direction = direction;
            this.steps = steps;
        }
    }

    class Position {

        int x;
        int y;

        public Position(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public void add(int x, int y) {
            this.x += x;
            this.y += y;
        }

        public boolean strictEquals(Position other) {
            return this.x == other.x && this.y == other.y;
        }

        public Position copy() {
            return new Position(this.x, this.y);
        }
    }

    class Knot {

        Position currentPosition = new Position(0, 0);
        ArrayList<Position> visited = new ArrayList(List.of(this.currentPosition.copy()));

        public void move(String direction) {
            switch (direction) {
                case "L" -> {
                    this.currentPosition.add(-1, 0);
                }
                case "R" -> {
                    this.currentPosition.add(1, 0);
                }
                case "U" -> {
                    this.currentPosition.add(0, -1);
                }
                case "D" -> {
                    this.currentPosition.add(0, 1);
                }
            }

            this.visited.add(this.currentPosition.copy());
        }

        public void follow(Knot knot) {
            if (this.currentPosition.strictEquals(knot.currentPosition)) {
                return;
            }

            if (this.isAdjacentTo(knot)) {
                return;
            }

            this.moveTowards(knot);

            for (Position position : (ArrayList<Position>) new ArrayList(this.visited)) {
                if (position.strictEquals(this.currentPosition)) {
                    return;
                }
            }

            this.visited.add(this.currentPosition.copy());
        }

        boolean isAdjacentTo(Knot knot) {
            int xDistance = Math.abs(this.currentPosition.x - knot.currentPosition.x);
            int yDistance = Math.abs(this.currentPosition.y - knot.currentPosition.y);

            return !(xDistance + yDistance > 2
                    || xDistance > 1 && yDistance == 0
                    || yDistance > 1 && xDistance == 0);
        }

        void moveTowards(Knot knot) {
            int xDistance = this.currentPosition.x - knot.currentPosition.x;
            int yDistance = this.currentPosition.y - knot.currentPosition.y;

            if (xDistance == 2 && yDistance == 0) {
                this.currentPosition.add(-1, 0);
            }

            if (xDistance == -2 && yDistance == 0) {
                this.currentPosition.add(1, 0);
            }

            if (yDistance == 2 && xDistance == 0) {
                this.currentPosition.add(0, -1);
            }

            if (yDistance == -2 && xDistance == 0) {
                this.currentPosition.add(0, 1);
            }

            if (xDistance == 2 && yDistance == 1) {
                this.currentPosition.add(-1, -1);
            }

            if (xDistance == 2 && yDistance == -1) {
                this.currentPosition.add(-1, 1);
            }

            if (xDistance == -2 && yDistance == 1) {
                this.currentPosition.add(1, -1);
            }

            if (xDistance == -2 && yDistance == -1) {
                this.currentPosition.add(1, 1);
            }

            if (yDistance == 2 && xDistance == 1) {
                this.currentPosition.add(-1, -1);
            }

            if (yDistance == 2 && xDistance == -1) {
                this.currentPosition.add(1, -1);
            }

            if (yDistance == -2 && xDistance == 1) {
                this.currentPosition.add(-1, 1);
            }

            if (yDistance == -2 && xDistance == -1) {
                this.currentPosition.add(1, 1);
            }

            if (xDistance == 2 && yDistance == 2) {
                this.currentPosition.add(-1, -1);
            }

            if (xDistance == 2 && yDistance == -2) {
                this.currentPosition.add(-1, 1);
            }

            if (xDistance == -2 && yDistance == 2) {
                this.currentPosition.add(1, -1);
            }

            if (xDistance == -2 && yDistance == -2) {
                this.currentPosition.add(1, 1);
            }

        }
    }

    class Rope {

        ArrayList<Knot> knots;

        public Rope(int len) {
            this.knots = new ArrayList();
            for (int i = 0; i < len; i++) {
                this.knots.add(new Knot());
            }
        }

        public void move(Instruction instruction) {
            for (int i = 0; i < instruction.steps; i++) {
                for (int innerIndex = 0; innerIndex < this.knots.size(); innerIndex++) {
                    if (innerIndex == 0) {
                        Knot head = this.knots.getFirst();
                        head.move(instruction.direction);
                        continue;
                    }

                    Knot previous = this.knots.get(innerIndex - 1);
                    Knot next = this.knots.get(innerIndex);

                    next.follow(previous);
                }
            }
        }
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
            Head follows instructions, check where tail is.
            Head and tail must be touching:
                overlap / adjacent / diagonal
                tail follows hori/verti
                tail follows diagonally if further
            How many positions does the tail visit at least once?
         */
        ArrayList<Instruction> instructions = parseInput(input);
        Knot head = new Knot();
        Knot tail = new Knot();

        for (Instruction instruction : instructions) {
            for (int i = 0; i < instruction.steps; i++) {
                head.move(instruction.direction);
                tail.follow(head);
            }
        }

        System.out.println(tail.visited.size());
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
            Rope is 10 long, head + 8 + tail
         */
        ArrayList<Instruction> instructions = parseInput(input);
        Rope rope = new Rope(10);

        for (Instruction instruction : instructions) {
            rope.move(instruction);
        }

        System.out.println(rope.knots.getLast().visited.size());
    }
}
