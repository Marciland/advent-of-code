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

#[derive(Eq, Hash, Clone, PartialEq, PartialOrd, Ord)]
pub struct Position {
    pub x: i64,
    pub y: i64,
}

impl Position {
    #[must_use]
    pub fn dif(&self, other_position: &Position) -> Position {
        #[allow(clippy::cast_possible_wrap)]
        let x_dif = self.x.abs_diff(other_position.x) as i64;
        #[allow(clippy::cast_possible_wrap)]
        let y_dif = self.y.abs_diff(other_position.y) as i64;

        Position { x: x_dif, y: y_dif }
    }

    #[must_use]
    pub fn add(&self, other: &Position) -> Position {
        Position {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }

    #[must_use]
    pub fn left(&self) -> Position {
        Position {
            x: self.x - 1,
            y: self.y,
        }
    }

    #[must_use]
    pub fn right(&self) -> Position {
        Position {
            x: self.x + 1,
            y: self.y,
        }
    }

    #[must_use]
    pub fn up(&self) -> Position {
        Position {
            x: self.x,
            y: self.y - 1,
        }
    }

    #[must_use]
    pub fn down(&self) -> Position {
        Position {
            x: self.x,
            y: self.y + 1,
        }
    }

    #[must_use]
    pub fn neighbours(&self) -> Vec<Position> {
        vec![self.left(), self.right(), self.up(), self.down()]
    }
}

#[derive(Clone)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Direction {
    #[must_use]
    pub fn value(&self) -> Position {
        match self {
            Direction::Up => Position { x: 0, y: -1 },
            Direction::Down => Position { x: 0, y: 1 },
            Direction::Left => Position { x: -1, y: 0 },
            Direction::Right => Position { x: 1, y: 0 },
        }
    }

    #[must_use]
    pub fn clockwise(&self) -> Direction {
        match self {
            Direction::Up => Direction::Right,
            Direction::Down => Direction::Left,
            Direction::Left => Direction::Up,
            Direction::Right => Direction::Down,
        }
    }

    #[must_use]
    pub fn counter_clockwise(&self) -> Direction {
        match self {
            Direction::Up => Direction::Left,
            Direction::Down => Direction::Right,
            Direction::Left => Direction::Down,
            Direction::Right => Direction::Up,
        }
    }
}
