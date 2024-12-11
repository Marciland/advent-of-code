use std::collections::HashMap;

fn blink(map: HashMap<String, u64>) -> HashMap<String, u64> {
    let mut new_map = HashMap::new();

    for (key, value) in map {
        if key == "0" {
            increment_if_exist(&mut new_map, "1", value);
            continue;
        }

        if key.len() % 2 == 0 {
            let mut new_numbers = key.clone();
            let right = new_numbers.split_off(new_numbers.len() / 2);

            increment_if_exist(&mut new_map, &new_numbers, value);

            let trimmed_right = right.trim_start_matches('0');

            if trimmed_right.is_empty() {
                increment_if_exist(&mut new_map, "0", value);
            } else {
                increment_if_exist(&mut new_map, trimmed_right, value);
            }

            continue;
        }

        let new_number = key.parse::<u64>().unwrap() * 2024;
        increment_if_exist(&mut new_map, &new_number.to_string(), value);
    }

    new_map
}

fn increment_if_exist(map: &mut HashMap<String, u64>, key: &str, increment: u64) {
    if let Some(old_value) = map.insert(key.to_owned(), increment) {
        map.insert(key.to_owned(), old_value + increment);
    }
}

fn parse_input(input: &[String]) -> HashMap<String, u64> {
    let mut stones = HashMap::new();

    for number_str in input.join("").split(' ') {
        increment_if_exist(&mut stones, number_str, 1);
    }

    stones
}

pub fn star1(input: &[String]) {
    /*
        How many stones after 25 blinks?

        each blink the first rule applicable:
            number 0 replaced by 1
            even number of digits replaced by two stones:
                left half of digits on left stone ...
                no leading zeros
            multiplied by 2024

        order is preserved
    */
    let mut stones = parse_input(input);
    for _ in 0..25 {
        stones = blink(stones);
    }

    let mut amount_of_stones = 0;
    for amount in stones.values() {
        amount_of_stones += amount;
    }

    println!("{amount_of_stones}");
}

pub fn star2(input: &[String]) {
    /*
       75 blinks..
    */
    let mut stones = parse_input(input);
    for _ in 0..75 {
        stones = blink(stones);
    }

    let mut amount_of_stones = 0;
    for amount in stones.values() {
        amount_of_stones += amount;
    }

    println!("{amount_of_stones}");
}
