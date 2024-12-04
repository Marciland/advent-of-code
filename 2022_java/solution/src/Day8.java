
import java.util.ArrayList;

public class Day8 extends Day {

    class Grid {

        // x,y
        int[][] trees;

        public Grid(ArrayList<String> input) {
            int width = input.get(0).length();
            int height = input.size();

            this.trees = new int[width][height];

            for (int y = 0; y < height; y++) {
                String line = input.get(y);
                char[] chars = line.toCharArray();

                for (int x = 0; x < width; x++) {
                    this.trees[x][y] = Integer.parseInt(Character.toString(chars[x]));
                }
            }
        }

        public ArrayList<Integer> getScenicScores() {
            ArrayList<Integer> scores = new ArrayList();

            for (int y = 0; y < this.trees[0].length; y++) {
                for (int x = 0; x < this.trees.length; x++) {
                    scores.add(this.getScenicScore(x, y));
                }
            }

            return scores;
        }

        int getScenicScore(int x, int y) {
            if (this.isEdge(x, y)) {
                return 0;
            }
            /*
                count trees until blocked
             */
            return this.getViewingDistanceRight(x, y) * this.getViewingDistanceLeft(x, y) * this.getViewingDistanceUp(x, y) * this.getViewingDistanceDown(x, y);
        }

        int getViewingDistanceRight(int x, int y) {
            int viewingDistance = 0;
            int size = this.trees[x][y];

            for (int i = x + 1; i < this.trees.length; i++) {
                int otherSize = this.trees[i][y];
                if (otherSize >= size) {
                    viewingDistance += 1;
                    break;
                }
                viewingDistance += 1;
            }

            return viewingDistance;
        }

        int getViewingDistanceLeft(int x, int y) {
            int viewingDistance = 0;
            int size = this.trees[x][y];

            for (int i = x - 1; i >= 0; i--) {
                int otherSize = this.trees[i][y];
                if (otherSize >= size) {
                    viewingDistance += 1;
                    break;
                }
                viewingDistance += 1;
            }

            return viewingDistance;
        }

        int getViewingDistanceUp(int x, int y) {
            int viewingDistance = 0;
            int size = this.trees[x][y];

            for (int i = y - 1; i >= 0; i--) {
                int otherSize = this.trees[x][i];
                if (otherSize >= size) {
                    viewingDistance += 1;
                    break;
                }
                viewingDistance += 1;
            }

            return viewingDistance;
        }

        int getViewingDistanceDown(int x, int y) {
            int viewingDistance = 0;
            int size = this.trees[x][y];

            for (int i = y + 1; i < this.trees[0].length; i++) {
                int otherSize = this.trees[x][i];
                if (otherSize >= size) {
                    viewingDistance += 1;
                    break;
                }
                viewingDistance += 1;
            }

            return viewingDistance;
        }

        public int getVisible() {
            int visibleTrees = 0;

            for (int y = 0; y < this.trees[0].length; y++) {
                for (int x = 0; x < this.trees.length; x++) {
                    if (this.isVisible(x, y)) {
                        visibleTrees += 1;
                    }
                }
            }

            return visibleTrees;
        }

        boolean isEdge(int x, int y) {
            return x == 0 || x == this.trees.length - 1 || y == 0 || y == this.trees[0].length - 1;
        }

        boolean isVisible(int x, int y) {
            if (this.isEdge(x, y)) {
                return true;
            }

            return this.isVisibleRight(x, y) || this.isVisibleLeft(x, y) || this.isVisibleUp(x, y) || this.isVisibleDown(x, y);
        }

        boolean isVisibleRight(int x, int y) {
            int size = this.trees[x][y];

            for (int i = x + 1; i < this.trees.length; i++) {
                int otherSize = this.trees[i][y];
                if (otherSize >= size) {
                    return false;
                }
            }

            return true;
        }

        boolean isVisibleLeft(int x, int y) {
            int size = this.trees[x][y];

            for (int i = x - 1; i >= 0; i--) {
                int otherSize = this.trees[i][y];
                if (otherSize >= size) {
                    return false;
                }
            }

            return true;
        }

        boolean isVisibleUp(int x, int y) {
            int size = this.trees[x][y];

            for (int i = y - 1; i >= 0; i--) {
                int otherSize = this.trees[x][i];
                if (otherSize >= size) {
                    return false;
                }
            }

            return true;
        }

        boolean isVisibleDown(int x, int y) {
            int size = this.trees[x][y];

            for (int i = y + 1; i < this.trees[0].length; i++) {
                int otherSize = this.trees[x][i];
                if (otherSize >= size) {
                    return false;
                }
            }

            return true;
        }
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
            sum of trees visible from outside of grid:
            input has height of trees
                0 shortest
                9 tallest
            visible if in row or col no taller/same to the edge
         */
        Grid g = new Grid(input);

        int visibleTrees = g.getVisible();

        System.out.println(visibleTrees);
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
            calc scenic score:
                multiply together the viewing distances
            viewing distance is:
                look at all directions
                count trees until blocked
            find highest scenic score
         */
        Grid g = new Grid(input);

        ArrayList<Integer> scenicScores = g.getScenicScores();

        int highest = 0;
        for (int score : scenicScores) {
            if (score > highest) {
                highest = score;
            }
        }

        System.out.println(highest);
    }
}
