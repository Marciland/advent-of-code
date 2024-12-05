
import java.util.ArrayList;
import java.util.List;

public class Day10 extends Day {

    ArrayList<Instruction> parseInput(ArrayList<String> input) {
        ArrayList<Instruction> instructions = new ArrayList();

        for (String line : input) {
            String[] i = line.split(" ");
            if (i.length == 2) {
                instructions.add(new Instruction(i[0], Integer.parseInt(i[1])));
                continue;
            }
            instructions.add(new Instruction(i[0], 0));
        }

        return instructions;
    }

    class Instruction {

        String operation;
        int value;

        public Instruction(String operation, int value) {
            this.operation = operation;
            this.value = value;
        }
    }

    class CRT {

        // x,y
        boolean[][] pixels;

        public CRT(int width, int height) {
            this.pixels = new boolean[width][height];
        }

        public void render() {
            for (int y = 0; y < this.pixels[0].length; y++) {
                for (boolean[] pixel : this.pixels) {
                    if (pixel[y]) {
                        System.err.print("#");
                    } else {
                        System.err.print(".");
                    }
                }
                System.out.println();
            }
        }

        public int getY(int currentCycle) {
            double y = Math.floor(currentCycle / this.pixels.length);
            return (int) y;
        }
    }

    class CPU {

        ArrayList<Integer> marker = new ArrayList(List.of(20, 60, 100, 140, 180, 220));
        int currentCycle = 0;
        int xRegister = 1;

        public int run(Instruction instruction) {
            this.currentCycle++;

            int signal = 0;

            if (this.marker.contains(this.currentCycle)) {
                signal += this.xRegister * this.currentCycle;
            }

            if (instruction.operation.equals("noop")) {
                return signal;
            }

            this.currentCycle++;

            if (this.marker.contains(this.currentCycle)) {
                signal += this.xRegister * this.currentCycle;
            }

            this.xRegister += instruction.value;

            return signal;
        }

        public void prepare_render(Instruction instruction, CRT crt) {
            if (this.should_render(crt)) {
                int y = crt.getY(this.currentCycle);
                crt.pixels[this.currentCycle - crt.pixels.length * y][y] = true;
            }

            this.currentCycle++;

            if (instruction.operation.equals("noop")) {
                return;
            }

            if (this.should_render(crt)) {
                int y = crt.getY(this.currentCycle);
                crt.pixels[this.currentCycle - crt.pixels.length * y][y] = true;
            }

            this.currentCycle++;

            this.xRegister += instruction.value;
        }

        boolean should_render(CRT crt) {
            int y = crt.getY(this.currentCycle);

            int cycle = this.currentCycle - y * crt.pixels.length;
            return cycle == this.xRegister
                    || cycle == this.xRegister + 1
                    || cycle == this.xRegister - 1;
        }
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
            What is the sum of the signal strengths at:
                20th
                60th
                100th
                140th
                180th
                220th

            strength during cycle = cycle * value
            operation completes after
                noop 1 cycle
                addx 2 cycle
         */
        ArrayList<Instruction> instructions = parseInput(input);
        CPU cpu = new CPU();

        int summedSignalStrengths = 0;
        for (Instruction instruction : instructions) {
            summedSignalStrengths += cpu.run(instruction);
        }

        System.out.println(summedSignalStrengths);
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
            What eight capital letters appear on your CRT?

            CRT is 40 wide and 6 high
            xRegister is middle of sprite with width 3

            draw left to right
            40x6
            draw before add
         */
        ArrayList<Instruction> instructions = parseInput(input);
        CPU cpu = new CPU();
        CRT crt = new CRT(40, 6);

        for (Instruction instruction : instructions) {
            cpu.prepare_render(instruction, crt);
        }

        crt.render();
    }
}
