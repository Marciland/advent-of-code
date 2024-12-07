#[derive(Clone)]
enum Operator {
    Addition,
    Multiplication,
    Concat,
}

impl Operator {
    pub fn concatenate(left: u128, right: u128) -> u128 {
        let number_string = left.to_string() + &right.to_string();

        number_string.parse().unwrap()
    }
}

struct Equation {
    pub result: u128,
    pub numbers: Vec<u128>,
}

impl Equation {
    pub fn solve(&self, operators: &[Operator]) -> u128 {
        let combinations = self.create_combinations(operators);

        for combination in combinations {
            if self.is_possible(&combination) {
                return self.result;
            }
        }

        0
    }

    fn is_possible(&self, combination: &[Operator]) -> bool {
        assert!(combination.len() == self.numbers.len() - 1);

        let mut res = *self.numbers.first().unwrap();
        let mut next_number_index = 1;

        for operator in combination {
            let next_number = self.numbers.get(next_number_index).unwrap();

            match operator {
                Operator::Addition => res += next_number,
                Operator::Multiplication => res *= next_number,
                Operator::Concat => res = Operator::concatenate(res, *next_number),
            }

            next_number_index += 1;
        }

        res == self.result
    }

    fn create_combinations(&self, operators: &[Operator]) -> Vec<Vec<Operator>> {
        // kreuzprodukt operator & operations
        let mut combinations: Vec<Vec<Operator>> = vec![vec![]];

        let amount_of_operations = self.numbers.len() - 1;

        for _ in 0..amount_of_operations {
            let mut new_combinations: Vec<Vec<Operator>> = Vec::with_capacity(amount_of_operations);
            for combination in &combinations {
                for operator in operators {
                    let mut new_combination = combination.clone();
                    new_combination.push(operator.clone());
                    new_combinations.push(new_combination);
                }
            }
            combinations = new_combinations;
        }

        combinations
    }
}

fn parse_input(input: &[String]) -> Vec<Equation> {
    let mut equations: Vec<Equation> = Vec::with_capacity(input.len());

    for line in input {
        let line_parts: Vec<&str> = line.split(':').collect();
        let result = line_parts[0].parse().expect("Not a number");
        let numbers = line_parts[1]
            .trim()
            .split(' ')
            .map(|str| str.trim().parse::<u128>().expect("Not a number"))
            .collect();

        equations.push(Equation { result, numbers });
    }

    equations
}

pub fn star1(input: &[String]) {
    /*
       create equations
       sum the ones that work
    */
    let equations: Vec<Equation> = parse_input(input);
    let operators: Vec<Operator> = vec![Operator::Addition, Operator::Multiplication];

    let mut sum = 0;
    for equation in equations {
        sum += equation.solve(&operators);
    }

    println!("{sum}");
}

pub fn star2(input: &[String]) {
    /*
       Same, concat..
    */
    let equations: Vec<Equation> = parse_input(input);
    let operators: Vec<Operator> = vec![
        Operator::Addition,
        Operator::Multiplication,
        Operator::Concat,
    ];

    let mut sum = 0;
    for equation in equations {
        sum += equation.solve(&operators);
    }

    println!("{sum}");
}
