extern crate helpers;
use helpers::Position;

struct MemorySpace {
    pub width: usize,
    pub height: usize,
    pub grid: Vec<Vec<bool>>,
}

impl MemorySpace {
    pub fn drop_bytes(&mut self, bytes: &[Position], amount: u64) {
        todo!()
    }

    pub fn find_shortest_path(&self) -> u64 {
        todo!()
    }

    fn is_corrupted(&self, x: usize, y: usize) -> bool {
        *self.grid.get(x).unwrap().get(y).unwrap()
    }
}

fn parse_input(input: &[String]) -> Vec<Position> {
    todo!()
}

pub fn star1(input: &[String]) {
    /*
        Bytes fall on you..
        0..70 grid
        input is x,y
        move from 0,0 to 70,70
        simulate 1kb then find the shortest path
        number of steps, no diagonal
    */
    let bytes = parse_input(input);

    let mut memory_space = MemorySpace {
        width: 70,
        height: 70,
        grid: vec![vec![false; 70]],
    };
    memory_space.drop_bytes(&bytes, 1024);

    let least_steps = memory_space.find_shortest_path();

    println!("{least_steps}");
}

pub fn star2(_input: &[String]) {}
