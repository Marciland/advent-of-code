#[derive(Clone, PartialEq)]
struct Pos {
    pub x: u128,
    pub y: u128,
}

impl Pos {
    pub fn mul(&self, val: u128) -> Pos {
        Pos {
            x: self.x * val,
            y: self.y * val,
        }
    }

    pub fn add(&self, other: &Pos) -> Pos {
        Pos {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

#[derive(Clone)]
struct ClawMachine {
    pub a: Pos,
    pub b: Pos,
    pub prize: Pos,
}

impl ClawMachine {
    pub fn grab_prize(&self) -> Option<u128> {
        let mut fewest_token = None;

        for a in 0..100 {
            for b in 0..100 {
                let pos = self.a.mul(a).add(&self.b.mul(b));

                if pos.x > self.prize.x || pos.y > self.prize.y {
                    break;
                }

                if pos != self.prize {
                    continue;
                }

                let current_cost = a * 3 + b;

                let Some(fewest) = fewest_token else {
                    fewest_token = Some(current_cost);
                    break;
                };

                if fewest > current_cost {
                    fewest_token = Some(current_cost);
                }

                break;
            }
        }

        fewest_token
    }

    pub fn solve(&self) -> u128 {
        /*
           self.a.x * a + self.b.x * b = self.prize.x;
           self.a.y * a + self.b.y * b = self.prize.y;

           solve for a and b?
        */
        todo!()
    }
}

fn parse_input(input: &[String]) -> Vec<ClawMachine> {
    let mut machines: Vec<ClawMachine> = Vec::new();

    let mut machine = ClawMachine {
        a: Pos { x: 0, y: 0 },
        b: Pos { x: 0, y: 0 },
        prize: Pos { x: 0, y: 0 },
    };
    for line in input {
        if line.is_empty() {
            machines.push(machine.clone());
            continue;
        }

        let numbers = line.split(':').collect::<Vec<&str>>()[1]
            .split(',')
            .collect::<Vec<&str>>();
        let (x, y) = if line.contains('=') {
            let x: u128 = numbers[0].split('=').collect::<Vec<&str>>()[1]
                .trim()
                .parse()
                .unwrap();
            let y: u128 = numbers[1].split('=').collect::<Vec<&str>>()[1]
                .trim()
                .parse()
                .unwrap();

            (x, y)
        } else {
            let x: u128 = numbers[0].split('+').collect::<Vec<&str>>()[1]
                .trim()
                .parse()
                .unwrap();
            let y: u128 = numbers[1].split('+').collect::<Vec<&str>>()[1]
                .trim()
                .parse()
                .unwrap();

            (x, y)
        };

        if line.contains("Prize") {
            machine.prize = Pos { x, y };
        }

        if line.contains("Button A") {
            machine.a = Pos { x, y };
        }

        if line.contains("Button B") {
            machine.b = Pos { x, y };
        }
    }
    machines.push(machine.clone());

    machines
}

pub fn star1(input: &[String]) {
    /*
        Claw machines:
            A 3 token
            B 1 token
        max 100 of each
        not all prices possible

        fewest token to reach all prizes possible?
    */
    let machines = parse_input(input);

    let mut token_cost = 0;
    for machine in machines {
        if let Some(cost) = machine.grab_prize() {
            token_cost += cost;
        }
    }

    println!("{token_cost}");
}

pub fn star2(input: &[String]) {
    /*
       increase prize x and prize y by 10000000000000
    */
    let mut machines = parse_input(input);

    let mut token_cost = 0;
    for machine in &mut machines {
        machine.prize.x += 10_000_000_000_000;
        machine.prize.y += 10_000_000_000_000;

        // WIP
        token_cost += machine.solve();
    }

    println!("{token_cost}");
}
