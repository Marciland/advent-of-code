
import java.util.ArrayList;

public class Day2 extends Day {

    class MoveSet {

        public ArrayList<String> opponentMoves;
        public ArrayList<String> playerMoves;

        public MoveSet(ArrayList<String> input) {
            this.opponentMoves = new ArrayList();
            this.playerMoves = new ArrayList();

            for (String line : input) {
                String[] moves = line.split(" ");
                assert moves.length == 2;
                this.opponentMoves.add(moves[0]);
                this.playerMoves.add(moves[1]);
            }

            assert opponentMoves.size() == playerMoves.size();
        }

        public int calculateScore(int index) {
            String opponent = this.opponentMoves.get(index);
            String player = this.playerMoves.get(index);

            int score = 0;

            switch (player) {
                case "X" -> {
                    score += 1;
                    if (opponent.equals("C")) {
                        score += 6;
                    } else if (opponent.equals("A")) {
                        score += 3;
                    }
                }
                case "Y" -> {
                    score += 2;
                    if (opponent.equals("A")) {
                        score += 6;
                    } else if (opponent.equals("B")) {
                        score += 3;
                    }
                }
                case "Z" -> {
                    score += 3;
                    if (opponent.equals("B")) {
                        score += 6;
                    } else if (opponent.equals("C")) {
                        score += 3;
                    }
                }
            }

            return score;
        }

        public void adjustPlayer() {
            ArrayList<String> adjustedPlayerMoves = new ArrayList();

            for (int i = 0; i < this.playerMoves.size(); i++) {
                String opponent = this.opponentMoves.get(i);
                String player = this.playerMoves.get(i);

                switch (player) {
                    case "X" -> {
                        switch (opponent) {
                            case "A" -> {
                                adjustedPlayerMoves.add("Z");
                            }
                            case "B" -> {
                                adjustedPlayerMoves.add("X");
                            }
                            case "C" -> {
                                adjustedPlayerMoves.add("Y");
                            }
                        }
                    }
                    case "Y" -> {
                        switch (opponent) {
                            case "A" -> {
                                adjustedPlayerMoves.add("X");
                            }
                            case "B" -> {
                                adjustedPlayerMoves.add("Y");
                            }
                            case "C" -> {
                                adjustedPlayerMoves.add("Z");
                            }
                        }
                    }
                    case "Z" -> {
                        switch (opponent) {
                            case "A" -> {
                                adjustedPlayerMoves.add("Y");
                            }
                            case "B" -> {
                                adjustedPlayerMoves.add("Z");
                            }
                            case "C" -> {
                                adjustedPlayerMoves.add("X");
                            }
                        }
                    }
                }
            }

            this.playerMoves = adjustedPlayerMoves;
        }

    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
            Total score: sum all rounds,
            where a round is:
                0 lost
                3 draw
                6 won
                bonus:
                1 rock
                2 paper
                3 scissors

            Rock: A X
            Paper: B Y
            Scissors: C Z

            first opponent then player
         */
        MoveSet moves = new MoveSet(input);

        int totalScore = 0;

        for (int i = 0; i < moves.playerMoves.size(); i++) {
            totalScore += moves.calculateScore(i);
        }

        System.out.println(totalScore);
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
            X Lose
            Y Draw
            Z Win

            then select the shape
         */
        MoveSet moves = new MoveSet(input);

        moves.adjustPlayer();

        int totalScore = 0;
        for (int i = 0; i < moves.playerMoves.size(); i++) {
            totalScore += moves.calculateScore(i);
        }

        System.out.println(totalScore);
    }
}
