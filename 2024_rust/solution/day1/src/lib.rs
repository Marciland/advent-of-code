fn split_input(input: &[String]) -> (Vec<u32>, Vec<u32>) {
    let mut left: Vec<u32> = Vec::with_capacity(input.len());
    let mut right: Vec<u32> = Vec::with_capacity(input.len());

    for line in input {
        let parts: Vec<&str> = line.split("   ").collect();
        assert_eq!(parts.len(), 2);

        let left_number: u32 = parts[0].trim().parse().expect("Should be u32");
        left.push(left_number);

        let right_number: u32 = parts[1].trim().parse().expect("Should be u32");
        right.push(right_number);
    }

    (left, right)
}

pub fn star1(input: &[String]) {
    /*
        Find the total distance between left and right.
        Where both lists have been sorted.

        Eg. compare smallest of both lists, then second smallest etc.
    */
    let mut total_distance = 0;

    let (mut left, mut right) = split_input(input);
    assert_eq!(left.len(), right.len());

    left.sort_unstable();
    right.sort_unstable();

    for index in 0..left.len() {
        let left_number = left[index];
        let right_number = right[index];

        let distance = left_number.abs_diff(right_number);

        total_distance += distance;
    }

    println!("Total distance is: {total_distance}");
}

pub fn star2(input: &[String]) {
    /*
       Find the similarity score.
       For each number on the left side, find its number of occurances in the right list.
       The similarity score is its value multiplied by its number of occurances.
    */
    let mut similarity_score = 0;

    let (left, right) = split_input(input);

    for left_number in left {
        let mut occurances = 0;
        for right_number in &right {
            if left_number == *right_number {
                occurances += 1;
            }
        }
        similarity_score += left_number * occurances;
    }

    println!("Total similarity score is: {similarity_score}");
}
