
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Day7 extends Day {

    class FileSystem {

        Dir root;
        ArrayList<String> stack;

        public FileSystem() {
            this.root = new Dir("/");
            this.stack = new ArrayList(List.of("/"));
        }

        public void addFile(String name, int size) {
            this.getCwd().files.add(new File(name, size));
        }

        public void addDir(String name) {
            Dir cwd = this.getCwd();

            for (Dir dir : cwd.directories) {
                if (dir.name.equals(name)) {
                    return;
                }
            }

            cwd.directories.add(new Dir(name));
        }

        Dir getCwd() {
            return this.root.search(new ArrayList(this.stack));
        }

        public void execute(String command, ArrayList<String> args) {
            if (command.equals("cd")) {
                String target = args.removeFirst();
                this.changeDir(target);
                return;
            }

            if (command.equals("ls")) {
                // ignore for now
            }
        }

        void changeDir(String target) {
            if (target.equals("/")) {
                this.stack.clear();
                this.stack.add("/");
                return;
            }

            if (target.equals("..")) {
                if (!this.stack.isEmpty()) {
                    this.stack.removeLast();
                }
                return;
            }

            this.stack.add(target);
        }

        int freeSpace(int toBeFreed) {
            ArrayList<Dir> deleteCandidates = new ArrayList();

            this.root.collectDeleteCandidates(toBeFreed, deleteCandidates);

            while (deleteCandidates.size() > 1) {
                Dir first = deleteCandidates.removeFirst();
                if (first.size() > deleteCandidates.getFirst().size()) {
                    continue;
                }
                deleteCandidates.add(first);
            }

            return deleteCandidates.getFirst().size();
        }
    }

    class Dir {

        String name;
        ArrayList<File> files;
        ArrayList<Dir> directories;

        public Dir(String name) {
            this.name = name;
            this.files = new ArrayList();
            this.directories = new ArrayList();
        }

        public Dir search(ArrayList<String> stack) {
            ArrayList<String> copy = new ArrayList(stack);

            String dirName = copy.removeFirst();
            assert dirName.equals(this.name);

            if (copy.isEmpty()) {
                return this;
            }

            String next = copy.getFirst();
            for (Dir dir : this.directories) {
                if (dir.name.equals(next)) {
                    return dir.search(copy);
                }
            }

            return null;
        }

        public int getSizeSummedIfBelow(int cap) {
            int sum = 0;

            for (Dir dir : this.directories) {
                sum += dir.getSizeSummedIfBelow(cap);
            }

            int dirSize = this.size();
            if (dirSize <= cap) {
                sum += dirSize;
            }

            return sum;
        }

        public int size() {
            int sum = 0;

            for (Dir dir : this.directories) {
                sum += dir.size();
            }

            for (File file : this.files) {
                sum += file.size;
            }

            return sum;
        }

        public void collectDeleteCandidates(int toBeFreed, ArrayList<Dir> deleteCandidates) {
            if (this.size() < toBeFreed) {
                return;
            }

            for (Dir dir : this.directories) {
                dir.collectDeleteCandidates(toBeFreed, deleteCandidates);
            }

            deleteCandidates.add(this);
        }
    }

    class File {

        @SuppressWarnings("unused")
        String name;
        int size;

        public File(String name, int size) {
            this.name = name;
            this.size = size;
        }
    }

    void parseInputIntoFs(ArrayList<String> input, FileSystem fs) {
        for (String line : input) {
            ArrayList<String> parts = new ArrayList(Arrays.asList(line.split(" ")));

            String id = parts.removeFirst();
            switch (id) {
                case "$" -> {
                    String command = parts.removeFirst();
                    fs.execute(command, parts);
                }
                case "dir" -> {
                    String name = parts.removeFirst();
                    fs.addDir(name);
                }
                default -> {
                    int size = Integer.parseInt(id);
                    String name = parts.removeFirst();
                    fs.addFile(name, size);
                }
            }
        }
    }

    @Override
    public void star1() {
        /*
          sum of size where dirs size <= 100.000

          find directories and push files into them
          filter dirs and calc sum
         */
        ArrayList<String> input = InputReader.readFile(7);

        FileSystem fs = new FileSystem();

        parseInputIntoFs(input, fs);

        int finalSum = fs.root.getSizeSummedIfBelow(100000);

        System.out.println(finalSum);
    }

    @Override
    public void star2() {
        /*
            Find smallest to delete to free enough space:
            30000000 free needed,
            70000000 total
         */
        ArrayList<String> input = InputReader.readFile(7);
        FileSystem fs = new FileSystem();
        parseInputIntoFs(input, fs);

        int totalCap = 70000000;
        int needed = 30000000;
        int usedSpace = fs.root.size();
        int freeSpace = totalCap - usedSpace;
        int toBeFreed = needed - freeSpace;

        int freedSpace = fs.freeSpace(toBeFreed);
        System.out.println(freedSpace);
    }
}
