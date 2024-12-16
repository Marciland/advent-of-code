extern crate helpers;
use std::convert::TryInto;

use helpers::{Direction, Position};

struct Maze {
    pub start: Position,
    pub end: Position,
    pub paths: Vec<Position>,
}

impl Maze {
    pub fn shortest(&self) -> u64 {
        let mut scores = Vec::new();
        self.step(&self.start, &Direction::Right, Vec::new(), 0, &mut scores);

        scores.sort_unstable();

        *scores.first().unwrap()
    }

    fn step(
        &self,
        current_position: &Position,
        current_direction: &Direction,
        mut visited: Vec<Position>,
        score: u64,
        scores: &mut Vec<u64>,
    ) {
        visited.push(current_position.clone());

        for next_direction in [
            current_direction,
            &current_direction.clockwise(),
            &current_direction.counter_clockwise(),
        ] {
            let next_step = current_position.add(&next_direction.value());
            if visited.contains(&next_step) {
                continue;
            }

            let new_score = if next_direction.value() == current_direction.value() {
                score + 1
            } else {
                score + 1001
            };

            if self.end == next_step {
                println!("{new_score}");
                scores.push(new_score);
                return;
            }

            if self.paths.contains(&next_step) {
                self.step(
                    &next_step,
                    next_direction,
                    visited.clone(),
                    new_score,
                    scores,
                );
            }
        }
    }
}

fn parse_input(input: &[String]) -> Maze {
    let mut start: Option<Position> = None;
    let mut end: Option<Position> = None;
    let mut paths: Vec<Position> = Vec::new();

    for (y, line) in input.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            let current_position = Position {
                x: x.try_into().unwrap(),
                y: y.try_into().unwrap(),
            };

            match char {
                'S' => start = Some(current_position),
                'E' => end = Some(current_position),
                '.' => paths.push(current_position),
                _ => (),
            }
        }
    }

    Maze {
        start: start.unwrap(),
        end: end.unwrap(),
        paths,
    }
}

pub fn star1(input: &[String]) {
    /*
        lowest score?
            start on S, end on E
            start direction east
            . is path, # is wall
            move forward costs 1
            rotate 90° costs 1000
    */
    let maze = parse_input(input);
    let score = maze.shortest();

    println!("{score}");
}

pub fn star2(_input: &[String]) {}
