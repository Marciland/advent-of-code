use std::convert::TryFrom;

#[derive(Clone, PartialEq, Ord, PartialOrd, Eq)]
struct Position {
    pub x: i16,
    pub y: i16,
}

impl Position {
    pub fn add(&self, other: &Position) -> Position {
        Position {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

#[derive(Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    pub fn value(&self) -> Position {
        match self {
            Direction::Up => Position { x: 0, y: -1 },
            Direction::Down => Position { x: 0, y: 1 },
            Direction::Left => Position { x: -1, y: 0 },
            Direction::Right => Position { x: 1, y: 0 },
        }
    }
}

#[derive(Clone)]
struct Guard {
    pub current_position: Position,
    pub direction: Direction,
    pub visited: Vec<Position>,
}

impl Guard {
    pub fn new(start: &Position) -> Self {
        Self {
            current_position: start.clone(),
            direction: Direction::Up,
            visited: Vec::new(),
        }
    }

    pub fn patrol(&mut self, lab: &Lab) {
        while !self.round_complete(lab) {
            self.visited.push(self.current_position.clone());
            self.move_once(lab);
        }
    }

    pub fn is_looping(&mut self, lab: &Lab) -> bool {
        loop {
            if self.round_complete(lab) {
                return false;
            }
            if self.inf_loop(lab) {
                return true;
            }
            self.visited.push(self.current_position.clone());
            self.move_once(lab);
        }
    }

    fn inf_loop(&self, lab: &Lab) -> bool {
        lab.width * lab.height < self.visited.len()
    }

    fn round_complete(&self, lab: &Lab) -> bool {
        let x = self.current_position.x;
        let y = self.current_position.y;

        if x < 0 || y < 0 {
            return true;
        }

        #[allow(clippy::cast_sign_loss)]
        let x = x as usize;
        #[allow(clippy::cast_sign_loss)]
        let y = y as usize;
        x >= lab.width || y >= lab.height
    }

    fn move_once(&mut self, lab: &Lab) {
        while !lab.can_move(&self.current_position, &self.direction) {
            self.turn_right();
        }

        self.current_position = self.current_position.add(&self.direction.value());
    }

    fn turn_right(&mut self) {
        match self.direction {
            Direction::Up => self.direction = Direction::Right,
            Direction::Down => self.direction = Direction::Left,
            Direction::Left => self.direction = Direction::Up,
            Direction::Right => self.direction = Direction::Down,
        }
    }
}

struct Lab {
    pub start: Position,
    pub width: usize,
    pub height: usize,
    pub obstructions: Vec<Position>,
}

impl Lab {
    pub fn can_move(&self, position: &Position, direction: &Direction) -> bool {
        let next_position = position.add(&direction.value());

        !self.obstructions.contains(&next_position)
    }
}

fn parse_input(input: &[String]) -> Lab {
    let mut start: Option<Position> = None;
    let mut obstructions: Vec<Position> = Vec::new();

    for (y, line) in input.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            match char {
                '^' => {
                    start = Some(Position {
                        x: i16::try_from(x).unwrap(),
                        y: i16::try_from(y).unwrap(),
                    });
                }
                '#' => obstructions.push(Position {
                    x: i16::try_from(x).unwrap(),
                    y: i16::try_from(y).unwrap(),
                }),
                _ => (),
            }
        }
    }

    Lab {
        start: start.expect("Failed to determine start position"),
        width: input.first().unwrap().len(),
        height: input.len(),
        obstructions,
    }
}

pub fn star1(input: &[String]) {
    /*
       Move a guard:
           straight until obstruction
           turn right
           stop at start

       How many distinct positions have been visited?
    */

    let lab = parse_input(input);
    let mut guard = Guard::new(&lab.start);

    guard.patrol(&lab);
    guard.visited.sort();
    guard.visited.dedup();
    let distinct_positions = guard.visited.len();
    println!("{distinct_positions}");
}

pub fn star2(input: &[String]) {
    /*
        Place one additional obstruction to create a loop.

        How many positions are valid to create a loop?
    */
    let lab = parse_input(input);
    let guard = Guard::new(&lab.start);
    let mut possible_locations = Vec::<Position>::new();

    for y in 0..lab.height {
        for x in 0..lab.width {
            let pos = Position {
                x: i16::try_from(x).unwrap(),
                y: i16::try_from(y).unwrap(),
            };

            if lab.obstructions.contains(&pos) {
                continue;
            }

            let mut new_obstructions = lab.obstructions.clone();
            new_obstructions.push(pos.clone());
            let new_lab = Lab {
                start: lab.start.clone(),
                width: lab.width,
                height: lab.height,
                obstructions: new_obstructions,
            };

            let mut new_guard = guard.clone();
            if new_guard.is_looping(&new_lab) {
                possible_locations.push(pos);
            }
        }
    }

    let obstruction_positions = possible_locations.len();
    println!("{obstruction_positions}");
}
