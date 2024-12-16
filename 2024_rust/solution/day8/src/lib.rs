extern crate helpers;
use helpers::Position;

use std::{
    collections::{HashMap, HashSet},
    convert::TryInto,
};

struct Map {
    pub width: usize,
    pub height: usize,
    pub antennas: HashMap<char, Vec<Position>>,
}

impl Map {
    pub fn get_all_antinodes(&self, harmony: bool) -> HashSet<Position> {
        let mut antinodes: HashSet<Position> = HashSet::new();

        for frequency_positions in self.antennas.values() {
            antinodes.extend(self.find_antinodes(frequency_positions, harmony));
        }

        antinodes
    }

    fn find_antinodes(&self, positions: &[Position], harmony: bool) -> Vec<Position> {
        let mut antinodes = Vec::new();

        for position in positions {
            if harmony && positions.len() > 1 {
                antinodes.push(position.clone());
            }

            for other_position in positions {
                if position == other_position {
                    continue;
                }

                let abs_dif = position.dif(other_position);

                let (x_dif, y_dif) =
                    if position.x > other_position.x && position.y > other_position.y {
                        (abs_dif.x, abs_dif.y)
                    } else if position.x > other_position.x && position.y < other_position.y {
                        (abs_dif.x, -abs_dif.y)
                    } else if position.x < other_position.x && position.y > other_position.y {
                        (-abs_dif.x, abs_dif.y)
                    } else if position.x < other_position.x && position.y < other_position.y {
                        (-abs_dif.x, -abs_dif.y)
                    } else {
                        panic!("bad logic above")
                    };

                let mut next = Position {
                    x: position.x + x_dif,
                    y: position.y + y_dif,
                };

                while self.is_in_bounds(&next) {
                    antinodes.push(next.clone());

                    if !harmony {
                        break;
                    }

                    next = Position {
                        x: next.x + x_dif,
                        y: next.y + y_dif,
                    };
                }
            }
        }

        antinodes
    }

    fn is_in_bounds(&self, pos: &Position) -> bool {
        !(pos.x >= self.width.try_into().unwrap()
            || pos.x < 0
            || pos.y >= self.height.try_into().unwrap()
            || pos.y < 0)
    }
}

fn parse_input(input: &[String]) -> Map {
    let mut antennas: HashMap<char, Vec<Position>> = HashMap::new();

    for (y, line) in input.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            if char == '.' {
                continue;
            }

            let antenna_position = Position {
                x: x.try_into().unwrap(),
                y: y.try_into().unwrap(),
            };

            if let Some(positions) = antennas.get_mut(&char) {
                positions.push(antenna_position);
            } else {
                let positions = vec![antenna_position];
                antennas.insert(char, positions);
            }
        }
    }

    Map {
        width: input.first().unwrap().len(),
        height: input.len(),
        antennas,
    }
}

pub fn star1(input: &[String]) {
    /*
        How many unique locations contain antinodes?

        antinode:
            two antennas with same frequency
            but one is twice as far away as the other
    */
    let map = parse_input(input);

    let antinodes = map.get_all_antinodes(false);
    let unique_locations = antinodes.len();

    println!("{unique_locations}");
}

pub fn star2(input: &[String]) {
    /*
       include if inline with at least two of the same frequency
    */
    let map = parse_input(input);

    let antinodes = map.get_all_antinodes(true);
    let unique_locations = antinodes.len();

    println!("{unique_locations}");
}
