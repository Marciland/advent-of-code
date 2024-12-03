
import java.util.ArrayList;
import java.util.Arrays;

public class Day7 extends Day {

    class FileSystem {

        ArrayList<Dir> directories;
        ArrayList<String> stack;
        int currentDir;

        public FileSystem() {
            this.directories = new ArrayList();
            this.stack = new ArrayList();

            this.directories.add(new Dir("/"));
            this.currentDir = -1;
        }

        public void addFile(String name, int size) {
            this.getCwd().files.add(new File(name, size));
        }

        public void addDir(String name) {
            Dir cwd = this.getCwd();

            if (cwd == null) {
                this.directories.add(new Dir(name));
                return;
            }

            for (Dir dir : cwd.directories) {
                if (dir.name.equals(name)) {
                    return;
                }
            }

            cwd.directories.add(new Dir(name));
        }

        Dir getCwd() {
            Dir cwd = null;
            String cwdName = this.stack.get(this.currentDir);
            for (Dir dir : this.directories) {
                cwd = dir.search(cwdName);
                if (cwd != null) {
                    break;
                }
            }

            return cwd;
        }

        public void execute(String command, ArrayList<String> args) {
            if (command.equals("cd")) {
                this.changeDir(args);
                return;
            }

            if (command.equals("ls")) {
                // ignore for now
            }
        }

        void changeDir(ArrayList<String> args) {
            String target = args.removeFirst();
            assert args.isEmpty();

            if (target.equals("..")) {
                assert this.currentDir >= 0;

                this.currentDir -= 1;
                this.stack.removeLast();
                return;
            }

            this.stack.add(target);
            this.currentDir += 1;
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

        public Dir search(String target) {
            if (this.name.equals(target)) {
                return this;
            }

            Dir targetDir;
            for (Dir dir : this.directories) {
                targetDir = dir.search(target);
                if (targetDir != null) {
                    return targetDir;
                }
            }

            return null;
        }

        public int getSizeAtMost(int cap) {
            int sum = 0;

            int dirSize = this.size();
            if (dirSize <= cap) {
                sum += dirSize;
            }

            for (Dir dir : this.directories) {
                sum += dir.getSizeAtMost(cap);
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
    }

    class File {

        String name;
        int size;

        public File(String name, int size) {
            this.name = name;
            this.size = size;
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

        Dir root = fs.directories.get(0);
        int finalSum = 0;

        for (Dir dir : root.directories) {
            finalSum += dir.getSizeAtMost(100000);
        }

        System.out.println(finalSum);
    }

    @Override
    public void star2() {
        /*

         */
        ArrayList<String> input = InputReader.readFile(7);
    }
}
