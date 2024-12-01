use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::PathBuf,
};

#[must_use]
pub fn input_to_string_vector(day: u8) -> Vec<String> {
    let file_path = PathBuf::from("../input/day".to_owned() + &day.to_string() + ".input");
    let Ok(file) = File::open(file_path) else {
        panic!("input file missing: {}", day)
    };
    let reader = BufReader::new(file);

    reader
        .lines()
        .map(|line| line.expect("Invalid input formatting"))
        .collect()
}
