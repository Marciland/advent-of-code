use std::{
    convert::{TryFrom, TryInto},
    fmt::{Display, Formatter, Result},
};

#[derive(Clone, PartialEq)]
enum OpCode {
    Adv,
    Bxl,
    Bst,
    Jnz,
    Bxc,
    Out,
    Bdv,
    Cdv,
}

impl OpCode {
    pub fn from(value: u8) -> OpCode {
        match value {
            0 => OpCode::Adv,
            1 => OpCode::Bxl,
            2 => OpCode::Bst,
            3 => OpCode::Jnz,
            4 => OpCode::Bxc,
            5 => OpCode::Out,
            6 => OpCode::Bdv,
            7 => OpCode::Cdv,
            _ => panic!("invalid opcode value"),
        }
    }

    pub fn value(&self) -> u8 {
        match self {
            OpCode::Adv => 0,
            OpCode::Bxl => 1,
            OpCode::Bst => 2,
            OpCode::Jnz => 3,
            OpCode::Bxc => 4,
            OpCode::Out => 5,
            OpCode::Bdv => 6,
            OpCode::Cdv => 7,
        }
    }
}

impl Display for OpCode {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{}", self.value())
    }
}

type Operand = u64;

#[derive(Clone)]
struct Instruction {
    pub op_code: OpCode,
    pub operand: Operand,
}

impl Display for Instruction {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "{},{}", self.op_code, self.operand)
    }
}

struct Computer {
    pub a: u64,
    pub b: u64,
    pub c: u64,
    pub program: Vec<Instruction>,
}

impl Computer {
    pub fn run_program(&mut self) -> String {
        let mut output = Vec::new();

        let mut instruction_pointer = 0;
        loop {
            if instruction_pointer == self.program.len() {
                break;
            }

            let instruction = self.program.get(instruction_pointer).unwrap();
            instruction_pointer += 1;

            let combo_operand = self.combo(instruction.operand);
            let numerator = self.a;

            match instruction.op_code {
                OpCode::Adv => self.a = numerator / 2_u64.pow(combo_operand.try_into().unwrap()),
                OpCode::Bdv => self.b = numerator / 2_u64.pow(combo_operand.try_into().unwrap()),
                OpCode::Cdv => self.c = numerator / 2_u64.pow(combo_operand.try_into().unwrap()),

                OpCode::Bxl => self.b ^= instruction.operand,
                OpCode::Bst => self.b = combo_operand % 8,
                OpCode::Bxc => self.b ^= self.c,

                OpCode::Out => output.push((combo_operand % 8).to_string()),

                OpCode::Jnz => {
                    if self.a != 0 {
                        instruction_pointer = usize::try_from(instruction.operand).unwrap();
                    }
                }
            }
        }

        output.join(",")
    }

    pub fn find_copy(&self) -> u64 {
        let mut lowest = 0;

        let mut computer = Computer {
            a: lowest,
            b: 0,
            c: 0,
            program: self.program.clone(),
        };

        loop {
            let output = computer.run_program();

            if self.is_copy(&output) {
                break;
            }

            lowest += 1;

            computer.a = lowest;
            computer.b = 0;
            computer.c = 0;
        }

        lowest
    }

    fn is_copy(&self, output: &str) -> bool {
        self.program
            .iter()
            .map(Instruction::to_string)
            .collect::<Vec<String>>()
            .join(",")
            == output
    }

    fn combo(&self, op: Operand) -> Operand {
        match op {
            0..=3 => op,
            4 => self.a,
            5 => self.b,
            6 => self.c,
            _ => panic!("invalid operand"),
        }
    }
}

fn parse_input(input: &[String]) -> Computer {
    let parts = input.split(String::is_empty).collect::<Vec<&[String]>>();
    let registers = parts[0];
    let program_string = parts[1];

    let mut reg_a = 0;
    let mut reg_b = 0;
    let mut reg_c = 0;

    for line in registers {
        let line_parts = line.split(':').collect::<Vec<&str>>();
        let identifier = line_parts[0];
        let register = line_parts[1].trim().parse::<u64>().expect("Not a number");

        if identifier.contains('A') {
            reg_a = register;
        } else if identifier.contains('B') {
            reg_b = register;
        } else if identifier.contains('C') {
            reg_c = register;
        }
    }

    let mut program = Vec::new();
    let program_codes = program_string.join("").split(' ').collect::<Vec<&str>>()[1]
        .trim()
        .to_owned();

    let mut instruction = Instruction {
        op_code: OpCode::Adv,
        operand: 0,
    };
    for (index, code) in program_codes.split(',').enumerate() {
        let number = code.parse().expect("Not a number");

        if index % 2 == 0 {
            instruction.op_code = OpCode::from(number);
        } else {
            instruction.operand = number.into();
            program.push(instruction.clone());
        }
    }

    Computer {
        a: reg_a,
        b: reg_b,
        c: reg_c,
        program,
    }
}

pub fn star1(input: &[String]) {
    /*
        Let computer run program,
        capture outs and join by ,
    */
    let mut computer = parse_input(input);

    let output = computer.run_program();

    println!("{output}");
}

pub fn star2(input: &[String]) {
    /*
        Find lowest value for A
        to create an exact copy of the program
    */
    let computer = parse_input(input);

    let register_a = computer.find_copy();

    println!("{register_a}");
}
