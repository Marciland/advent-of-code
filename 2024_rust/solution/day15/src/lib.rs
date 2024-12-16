extern crate helpers;
use std::convert::TryInto;

use helpers::{Direction, Position};

trait WH {
    fn summed_gps(&self) -> u64;
    fn move_robot(&mut self);
}

#[derive(PartialEq, Clone)]
struct BigBox {
    pub left: Position,
    pub right: Position,
}

struct BigWarehouse {
    pub robot: Position,
    pub moves: Vec<char>,
    pub boxes: Vec<BigBox>,
    pub walls: Vec<Position>,
}

impl BigWarehouse {
    fn attempt(&mut self, m: char) {
        let direction = match m {
            '>' => Direction::Right,
            '^' => Direction::Up,
            '<' => Direction::Left,
            'v' => Direction::Down,
            _ => panic!("invalid move"),
        };

        let next_position = self.robot.add(&direction.value());

        if self.walls.contains(&next_position) {
            return;
        }

        let mut to_be_pushed = Vec::new();
        for b in self.boxes.clone() {
            if b.left != next_position && b.right != next_position {
                continue;
            }

            if self.can_push(&b, &direction, &mut to_be_pushed) {
                break;
            }

            return;
        }

        for b in &mut self.boxes {
            if to_be_pushed.contains(b) {
                *b = BigBox {
                    left: b.left.add(&direction.value()),
                    right: b.right.add(&direction.value()),
                };
            }
        }

        self.robot = self.robot.add(&direction.value());
    }

    fn can_push(
        &mut self,
        big_box: &BigBox,
        direction: &Direction,
        to_be_pushed: &mut Vec<BigBox>,
    ) -> bool {
        let mut can_push = true;

        let next = match direction {
            Direction::Down | Direction::Up => vec![
                big_box.left.add(&direction.value()),
                big_box.right.add(&direction.value()),
            ],
            Direction::Left => vec![big_box.left.add(&direction.value())],
            Direction::Right => vec![big_box.right.add(&direction.value())],
        };

        for next_position in next {
            if self.walls.contains(&next_position) {
                can_push = false;
                break;
            }

            for b in self.boxes.clone() {
                if b.left == next_position || b.right == next_position {
                    can_push = can_push && self.can_push(&b, direction, to_be_pushed);
                    break;
                }
            }
        }

        if can_push {
            to_be_pushed.push(big_box.clone());
        }

        can_push
    }
}

impl WH for BigWarehouse {
    fn summed_gps(&self) -> u64 {
        let mut sum = 0;

        for b in &self.boxes {
            sum += 100 * b.left.y + b.left.x;
        }

        sum.try_into().unwrap()
    }

    fn move_robot(&mut self) {
        for m in self.moves.clone() {
            self.attempt(m);
        }
    }
}

struct Warehouse {
    pub robot: Position,
    pub moves: Vec<char>,
    pub boxes: Vec<Position>,
    pub walls: Vec<Position>,
}

impl Warehouse {
    fn attempt(&mut self, m: char) {
        let direction = match m {
            '>' => Direction::Right,
            '^' => Direction::Up,
            '<' => Direction::Left,
            'v' => Direction::Down,
            _ => panic!("invalid move"),
        };

        let mut next_position = self.robot.add(&direction.value());

        if self.walls.contains(&next_position) {
            return;
        }

        if !self.boxes.contains(&next_position) {
            self.robot = next_position;
            return;
        }

        let mut to_be_pushed = vec![next_position.clone()];
        loop {
            next_position = next_position.add(&direction.value());

            if self.walls.contains(&next_position) {
                return;
            }

            if self.boxes.contains(&next_position) {
                to_be_pushed.push(next_position.clone());
                continue;
            }

            break;
        }

        for b in &mut self.boxes {
            if to_be_pushed.contains(b) {
                *b = b.add(&direction.value());
            }
        }

        self.robot = self.robot.add(&direction.value());
    }
}

impl WH for Warehouse {
    fn summed_gps(&self) -> u64 {
        let mut sum = 0;

        for b in &self.boxes {
            sum += 100 * b.y + b.x;
        }

        sum.try_into().unwrap()
    }

    fn move_robot(&mut self) {
        for m in self.moves.clone() {
            self.attempt(m);
        }
    }
}

fn parse_input(input: &[String]) -> (&[String], String) {
    let parts: Vec<&[String]> = input.split(String::is_empty).collect();

    let warehouse_map = parts.first().unwrap();
    let moves_string = parts.get(1).unwrap().join("");

    (warehouse_map, moves_string)
}

fn parse_small(warehouse_map: &[String], moves_string: &str) -> Warehouse {
    let mut robot = None;
    let mut boxes = Vec::new();
    let mut walls = Vec::new();
    for (y, line) in warehouse_map.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            let position = Position {
                x: x.try_into().unwrap(),
                y: y.try_into().unwrap(),
            };

            match char {
                '@' => robot = Some(position),
                'O' => boxes.push(position),
                '#' => walls.push(position),
                _ => (),
            }
        }
    }

    let moves: Vec<char> = moves_string.chars().collect();

    Warehouse {
        robot: robot.unwrap(),
        moves,
        boxes,
        walls,
    }
}

fn parse_big(warehouse_map: &[String], moves_string: &str) -> BigWarehouse {
    let mut robot = None;
    let mut boxes = Vec::new();
    let mut walls = Vec::new();
    for (y, line) in warehouse_map.iter().enumerate() {
        let mut x = 0;
        for char in line.chars() {
            let position = Position {
                x: x.into(),
                y: y.try_into().unwrap(),
            };

            x += 1;

            let double_position = Position {
                x: x.into(),
                y: y.try_into().unwrap(),
            };

            match char {
                '@' => robot = Some(position),
                'O' => boxes.push(BigBox {
                    left: position,
                    right: double_position,
                }),
                '#' => {
                    walls.push(position);
                    walls.push(double_position);
                }
                _ => (),
            }

            x += 1;
        }
    }

    let moves: Vec<char> = moves_string.chars().collect();

    BigWarehouse {
        robot: robot.unwrap(),
        moves,
        boxes,
        walls,
    }
}

pub fn star1(input: &[String]) {
    /*
        robot: @
        box: O
        wall: #

        push if possible

        sum for all boxes gps
        where gps: 100 * from_top * from_left
    */
    let (warehouse_map, moves_string) = parse_input(input);
    let mut warehouse = parse_small(warehouse_map, &moves_string);

    warehouse.move_robot();

    let summed_gps = warehouse.summed_gps();

    println!("{summed_gps}");
}

pub fn star2(input: &[String]) {
    /*
        double everything, wide boxes can now be pushed together
    */
    let (warehouse_map, moves_string) = parse_input(input);
    let mut warehouse = parse_big(warehouse_map, &moves_string);

    warehouse.move_robot();

    let summed_gps = warehouse.summed_gps();

    println!("{summed_gps}");
}
