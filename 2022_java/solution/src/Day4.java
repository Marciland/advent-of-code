
import java.util.ArrayList;

public class Day4 extends Day {

  ArrayList<Pair> getPairs(ArrayList<String> input) {
    ArrayList<Pair> pairs = new ArrayList();

    for (String line : input) {
      pairs.add(new Pair(line));
    }

    return pairs;
  }

  class Pair {

    Sections firstElf;
    Sections secondElf;

    public Pair(String line) {
      String[] parts = line.split(",");
      assert parts.length == 2;

      this.firstElf = new Sections(parts[0]);
      this.secondElf = new Sections(parts[1]);
    }

    public boolean fullyOverlaps() {
      ArrayList<Integer> firstRange = this.firstElf.toRange();
      ArrayList<Integer> secondRange = this.secondElf.toRange();

      return firstRange.containsAll(secondRange) ||
          secondRange.containsAll(firstRange);
    }

    public boolean overlaps() {
      ArrayList<Integer> firstRange = this.firstElf.toRange();
      ArrayList<Integer> secondRange = this.secondElf.toRange();

      for (int section : firstRange) {
        if (secondRange.contains(section)) {
          return true;
        }
      }

      for (int section : secondRange) {
        if (firstRange.contains(section)) {
          return true;
        }
      }

      return false;
    }
  }

  class Sections {

    int start;
    int end;

    public Sections(String linePart) {
      String[] numbers = linePart.split("-");
      assert numbers.length == 2;

      this.start = Integer.parseInt(numbers[0]);
      this.end = Integer.parseInt(numbers[1]);
    }

    public ArrayList<Integer> toRange() {
      ArrayList<Integer> range = new ArrayList();

      for (int i = this.start; i <= this.end; i++) {
        range.add(i);
      }

      return range;
    }
  }

  @Override
  public void star1() {
    /*
        Find overlaps of sections for each elf pair
        how many overlaps are fully contained ones?
     */
    ArrayList<String> input = InputReader.readFile(4);
    ArrayList<Pair> pairs = getPairs(input);

    int fullOverlaps = 0;

    for (Pair pair : pairs) {
      if (pair.fullyOverlaps()) {
        fullOverlaps += 1;
      }
    }

    System.out.println(fullOverlaps);
  }

  @Override
  public void star2() {
    /*
        Now find any sort of overlap
     */
    ArrayList<String> input = InputReader.readFile(4);
    ArrayList<Pair> pairs = getPairs(input);

    int overlaps = 0;

    for (Pair pair : pairs) {
      if (pair.overlaps()) {
        overlaps += 1;
      }
    }

    System.out.println(overlaps);
  }
}
