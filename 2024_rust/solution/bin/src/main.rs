extern crate day1;
extern crate day10;
extern crate day11;
extern crate day12;
extern crate day13;
extern crate day14;
extern crate day15;
extern crate day16;
extern crate day17;
extern crate day18;
extern crate day19;
extern crate day2;
extern crate day20;
extern crate day21;
extern crate day22;
extern crate day23;
extern crate day24;
extern crate day3;
extern crate day4;
extern crate day5;
extern crate day6;
extern crate day7;
extern crate day8;
extern crate day9;

use std::time::Instant;

use day3::{star1, star2};

fn main() {
    let before = Instant::now();
    star1();
    println!(
        "Time to solve part 1: {:?}",
        Instant::now().duration_since(before)
    );
    let before = Instant::now();
    star2();
    println!(
        "Time to solve part 2: {:?}",
        Instant::now().duration_since(before)
    );
}
