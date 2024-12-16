use std::{collections::HashMap, convert::TryInto};

use helpers::Position;
use regex::Regex;

pub struct WordSearch {
    pub width: usize,
    pub height: usize,
    pub data: HashMap<Position, char>,
}

impl WordSearch {
    pub fn from(input: &[String]) -> Self {
        Self {
            width: input[0].len(),
            height: input.len(),
            data: Self::fill(input),
        }
    }

    pub fn search_x_mas(&self) -> u64 {
        let mut found: u64 = 0;

        let a: Vec<&Position> = self
            .data
            .iter()
            .filter_map(|(pos, char)| if *char == 'A' { Some(pos) } else { None })
            .collect();

        for pos in a {
            if self.is_edge(pos) {
                continue;
            }

            if self.is_x_mas(pos) {
                found += 1;
            }
        }

        found
    }

    fn is_x_mas(&self, pos: &Position) -> bool {
        let top_left_pos = Position {
            x: pos.x - 1,
            y: pos.y - 1,
        };
        let top_right_pos = Position {
            x: pos.x + 1,
            y: pos.y - 1,
        };
        let bottom_left_pos = Position {
            x: pos.x - 1,
            y: pos.y + 1,
        };
        let bottom_right_pos = Position {
            x: pos.x + 1,
            y: pos.y + 1,
        };

        let top_left_char = *self.data.get(&top_left_pos).unwrap();
        let top_right_char = *self.data.get(&top_right_pos).unwrap();
        let bottom_left_char = *self.data.get(&bottom_left_pos).unwrap();
        let bottom_right_char = *self.data.get(&bottom_right_pos).unwrap();

        (top_left_char == 'M' && bottom_right_char == 'S'
            || top_left_char == 'S' && bottom_right_char == 'M')
            && (bottom_left_char == 'M' && top_right_char == 'S'
                || bottom_left_char == 'S' && top_right_char == 'M')
    }

    fn is_edge(&self, pos: &Position) -> bool {
        pos.x == 0
            || pos.x == (self.width - 1).try_into().unwrap()
            || pos.y == 0
            || pos.y == (self.height - 1).try_into().unwrap()
    }

    pub fn find(&self, target: &str) -> u64 {
        let regex = Regex::new(target).unwrap();

        let mut found: u64 = 0;

        found += self.find_horizontal(&regex);
        found += self.find_vertical(&regex);
        found += self.find_diagonal(&regex);

        found
    }

    fn find_diagonal(&self, regex: &Regex) -> u64 {
        let mut found: u64 = 0;

        for diagonal in self.get_rising() {
            found += for_and_backwards(regex, &diagonal);
        }

        for diagonal in self.get_falling() {
            found += for_and_backwards(regex, &diagonal);
        }

        found
    }

    fn get_rising(&self) -> Vec<String> {
        fn construct_diagonal(grid: &WordSearch, x: usize, y: usize, mut result: String) -> String {
            let Some(position) = grid.data.get(&Position {
                x: x.try_into().unwrap(),
                y: y.try_into().unwrap(),
            }) else {
                panic!("Trying to find out of bounds");
            };
            result.push(*position);

            let next_x = x + 1;

            if next_x == grid.width {
                return result;
            }

            if y == 0 {
                return result;
            }

            construct_diagonal(grid, next_x, y - 1, result) // link unten nach rechts oben
        }

        let mut rising: Vec<String> = Vec::with_capacity(self.width);

        for y in 0..self.height {
            if y == self.height - 1 {
                for x in 0..self.width {
                    let diagonal: String = construct_diagonal(self, x, y, String::new());

                    rising.push(diagonal);
                }

                break;
            }

            let diagonal: String = construct_diagonal(self, 0, y, String::new());

            rising.push(diagonal);
        }

        rising
    }

    fn get_falling(&self) -> Vec<String> {
        fn construct_diagonal(grid: &WordSearch, x: usize, y: usize, mut result: String) -> String {
            let Some(position) = grid.data.get(&Position {
                x: x.try_into().unwrap(),
                y: y.try_into().unwrap(),
            }) else {
                panic!("Trying to find out of bounds");
            };
            result.push(*position);

            let next_x = x + 1;
            let next_y = y + 1;

            if next_x == grid.width {
                return result;
            }

            if next_y == grid.height {
                return result;
            }

            construct_diagonal(grid, next_x, next_y, result) // links oben nach rechts unten
        }

        let mut falling: Vec<String> = Vec::with_capacity(self.width);

        for x in (0..self.width).rev() {
            if x == 0 {
                for y in 0..self.height {
                    let diagonal = construct_diagonal(self, x, y, String::new());

                    falling.push(diagonal);
                }

                break;
            }

            let diagonal = construct_diagonal(self, x, 0, String::new());

            falling.push(diagonal);
        }

        falling
    }

    fn find_vertical(&self, regex: &Regex) -> u64 {
        let mut found: u64 = 0;

        for x in 0..self.width {
            let mut line = String::new();

            for y in 0..self.height {
                let Some(char) = self.data.get(&Position {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                }) else {
                    panic!("Trying to find out of bounds");
                };

                line.push(*char);
            }

            found += for_and_backwards(regex, &line);
        }

        found
    }

    fn find_horizontal(&self, regex: &Regex) -> u64 {
        let mut found = 0;

        for y in 0..self.height {
            let mut line = String::new();

            for x in 0..self.width {
                let Some(char) = self.data.get(&Position {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                }) else {
                    panic!("Trying to find out of bounds");
                };

                line.push(*char);
            }

            found += for_and_backwards(regex, &line);
        }

        found
    }

    fn fill(input: &[String]) -> HashMap<Position, char> {
        let mut data: HashMap<Position, char> = HashMap::new();

        for (y, line) in input.iter().enumerate() {
            for (x, char) in line.chars().enumerate() {
                data.insert(
                    Position {
                        x: x.try_into().unwrap(),
                        y: y.try_into().unwrap(),
                    },
                    char,
                );
            }
        }

        data
    }
}

fn for_and_backwards(regex: &Regex, line: &str) -> u64 {
    let reversed: String = line.chars().rev().collect();

    regex.captures_iter(line).count() as u64 + regex.captures_iter(&reversed).count() as u64
}
