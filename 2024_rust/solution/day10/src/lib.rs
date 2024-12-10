use std::{convert::TryInto, vec};

#[derive(Eq, Hash, PartialEq, Clone, Ord, PartialOrd)]
struct Position {
    pub x: i16,
    pub y: i16,
}

impl Position {
    pub fn left(&self) -> Position {
        Position {
            x: self.x - 1,
            y: self.y,
        }
    }

    pub fn right(&self) -> Position {
        Position {
            x: self.x + 1,
            y: self.y,
        }
    }

    pub fn up(&self) -> Position {
        Position {
            x: self.x,
            y: self.y - 1,
        }
    }

    pub fn down(&self) -> Position {
        Position {
            x: self.x,
            y: self.y + 1,
        }
    }

    pub fn neighbours(&self) -> Vec<Position> {
        vec![self.left(), self.right(), self.up(), self.down()]
    }
}

struct TopographicMap {
    // x,y
    pub map: Vec<Vec<u8>>,
    pub trailheads: Vec<Position>,
}

impl TopographicMap {
    pub fn sum_score(&self, unique: bool) -> u64 {
        let mut score: u64 = 0;

        for trailhead in &self.trailheads {
            let mut found: Vec<Position> = Vec::new();

            self.try(trailhead, &mut found);

            if unique {
                found.sort();
                found.dedup();
            }

            score += found.len() as u64;
        }

        score
    }

    fn try(&self, start: &Position, found: &mut Vec<Position>) {
        #[allow(clippy::cast_sign_loss)]
        let start_value = self.map[start.x as usize][start.y as usize];

        if start_value == 9 {
            found.push(start.clone());
            return;
        }

        let mut next_steps: Vec<Position> = Vec::with_capacity(4);
        for neighbour in start.neighbours() {
            if !self.is_in_bounds(&neighbour) {
                continue;
            }

            #[allow(clippy::cast_sign_loss)]
            let neighbour_value = self.map[neighbour.x as usize][neighbour.y as usize];

            if start_value + 1 != neighbour_value {
                continue;
            }

            next_steps.push(neighbour);
        }

        if next_steps.is_empty() {
            return;
        }

        for step in next_steps {
            self.try(&step, found);
        }
    }

    fn is_in_bounds(&self, position: &Position) -> bool {
        position.x >= 0
            && position.x < self.map.len().try_into().unwrap()
            && position.y >= 0
            && position.y < self.map.first().unwrap().len().try_into().unwrap()
    }
}

fn parse_input(input: &[String]) -> TopographicMap {
    let mut map: Vec<Vec<u8>> = vec![vec![0; input.len()]; input.first().unwrap().len()];
    let mut trailheads: Vec<Position> = Vec::new();

    for (y, line) in input.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            let number: u8 = char.to_string().parse().expect("Not a number");
            map[x][y] = number;

            if number == 0 {
                trailheads.push(Position {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                });
            }
        }
    }

    TopographicMap { map, trailheads }
}

pub fn star1(input: &[String]) {
    /*
       For each trailhead (0) create a score:
           How many 9 can be reached
           going +1 every move Up,Down,Right,Left
       Sum the scores
    */
    let score = parse_input(input).sum_score(true);

    println!("{score}");
}

pub fn star2(input: &[String]) {
    /*
        sum the ratings
            distinct hiking trails
    */
    let score = parse_input(input).sum_score(false);

    println!("{score}");
}
