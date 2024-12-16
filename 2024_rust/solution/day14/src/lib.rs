extern crate helpers;

use helpers::Position;

struct Robot {
    pub pos: Position,
    pub vel: Position,
}

impl Robot {
    pub fn take_step(&mut self, max_width: u8, max_height: u8) {
        let mut new_x = self.pos.x + self.vel.x;
        if new_x < 0 {
            new_x += i64::from(max_width);
        }

        if new_x >= max_width.into() {
            new_x -= i64::from(max_width);
        }

        let mut new_y = self.pos.y + self.vel.y;
        if new_y < 0 {
            new_y += i64::from(max_height);
        }

        if new_y >= max_height.into() {
            new_y -= i64::from(max_height);
        }

        self.pos.x = new_x;
        self.pos.y = new_y;
    }
}

struct Map {
    pub robots: Vec<Robot>,
    pub width: u8,
    pub height: u8,
}

impl Map {
    pub fn elapse_time(&mut self) {
        for robot in &mut self.robots {
            robot.take_step(self.width, self.height);
        }
    }

    pub fn safety_factor(&self) -> u64 {
        let x_del = self.width / 2;
        let y_del = self.height / 2;

        let mut quads: Vec<u64> = vec![0; 4];
        for y in 0..self.height {
            if y == y_del {
                continue;
            }

            for x in 0..self.width {
                if x == x_del {
                    continue;
                }

                let current_pos = Position {
                    x: x.into(),
                    y: y.into(),
                };

                for robot in &self.robots {
                    if robot.pos != current_pos {
                        continue;
                    }

                    if x < x_del && y < y_del {
                        quads[0] += 1;
                    } else if x < x_del && y > y_del {
                        quads[2] += 1;
                    } else if x > x_del && y < y_del {
                        quads[1] += 1;
                    } else if x > x_del && y > y_del {
                        quads[3] += 1;
                    }
                }
            }
        }

        quads[0] * quads[1] * quads[2] * quads[3]
    }
}

fn parse_input(input: &[String]) -> Map {
    let mut robots = Vec::with_capacity(input.len());

    for line in input {
        let parts: Vec<&str> = line.split(' ').collect();

        let position: Vec<&str> = parts[0].split('=').collect::<Vec<_>>()[1]
            .split(',')
            .collect();
        let velocity: Vec<&str> = parts[1].split('=').collect::<Vec<_>>()[1]
            .split(',')
            .collect();

        let pos = Position {
            x: position[0].parse().unwrap(),
            y: position[1].parse().unwrap(),
        };

        let vel = Position {
            x: velocity[0].parse().unwrap(),
            y: velocity[1].parse().unwrap(),
        };

        robots.push(Robot { pos, vel });
    }

    Map {
        robots,
        width: 101,
        height: 103,
    }
}

pub fn star1(input: &[String]) {
    /*
        Safety factor after 100 seconds?
        amount of robot per quadrant as product
        middle is cut out vert/hori (divisible by 2)
        field size x101 and y103
    */
    let mut map = parse_input(input);

    for _ in 0..100 {
        map.elapse_time();
    }

    let factor = map.safety_factor();

    println!("{factor}");
}

pub fn star2(input: &[String]) {
    /*
        Fewest seconds until you see a christmas tree
        (lowest security factor)
    */
    let mut map = parse_input(input);

    let mut least = 0;
    let mut f = 0;
    for seconds in 0..10000 {
        map.elapse_time();
        let factor = map.safety_factor();

        if least > factor || least == 0 {
            least = factor;
            f = seconds + 1;
        }
    }

    println!("{least}");
    println!("{f}");
}
