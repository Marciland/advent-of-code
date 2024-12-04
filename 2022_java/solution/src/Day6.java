
import java.util.ArrayList;

public class Day6 extends Day {

    int searchMarker(char[] signal, int distinct) {
        int markerPosition = 0;
        int valid = 0;

        search:
        for (int i = 0; i < signal.length; i++) {
            if (valid == distinct) {
                markerPosition = i;
                break;
            }

            for (int j = 1; j < distinct - valid; j++) {
                if (signal[i] == signal[i + j]) {
                    valid = 0;
                    continue search;
                }
            }

            valid += 1;
        }

        return markerPosition;
    }

    @Override
    public void star1(ArrayList<String> input) {
        /*
      find the marker:
      four characters that are all different
      how many chars are processed before the marker?
         */
        assert input.size() == 1;

        char[] signal = input.get(0).toCharArray();
        int position = searchMarker(signal, 4);

        System.out.println(position);
    }

    @Override
    public void star2(ArrayList<String> input) {
        /*
      Same, but 14 distinct characters
         */
        assert input.size() == 1;

        char[] signal = input.get(0).toCharArray();
        int position = searchMarker(signal, 14);

        System.out.println(position);
    }
}
