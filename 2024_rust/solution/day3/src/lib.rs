extern crate regex;
use regex::Regex;

pub fn star1(input: &[String]) {
    /*
        Find mul(number, number)
        sum the multiplications
    */
    let merged_input = input.join("");
    let regex = Regex::new(r"mul\(\d*,\d*\)").unwrap();

    let mut sum = 0;

    for (multiplication, _) in regex
        .captures_iter(&merged_input)
        .map(|multiplication| multiplication.extract::<0>())
    {
        let numbers = multiplication.replace("mul", "").replace(['(', ')'], "");
        let vals: Vec<&str> = numbers.split(',').collect();

        let left: u32 = vals[0].parse().expect("Not a number");
        let right: u32 = vals[1].parse().expect("Not a number");

        sum += left * right;
    }

    println!("{sum}");
}

pub fn star2(input: &[String]) {
    /*
        Same but only if do() was before
        dont() should not be included
    */
    let merged_input = input.join("");

    let mut matches = collect_matches(&merged_input);
    matches.sort_by_key(|a| a.index);

    let mut sum = 0;

    let mut should_multi = true;
    for m in matches {
        if m.value.contains("don't") {
            should_multi = false;
            continue;
        }
        if m.value.contains("do") {
            should_multi = true;
            continue;
        }

        if m.value.contains("mul") && should_multi {
            let numbers = m.value.replace("mul", "").replace(['(', ')'], "");
            let vals: Vec<&str> = numbers.split(',').collect();

            let left: u32 = vals[0].parse().expect("Not a number");
            let right: u32 = vals[1].parse().expect("Not a number");

            sum += left * right;
        }
    }

    println!("{sum}");
}

struct Match {
    pub index: usize,
    pub value: String,
}

fn collect_matches(input: &str) -> Vec<Match> {
    let mut matches = Vec::<Match>::new();

    let do_regex = Regex::new(r"do\(\)").unwrap();
    let mul_regex = Regex::new(r"mul\(\d*,\d*\)").unwrap();
    let dont_regex = Regex::new(r"don't\(\)").unwrap();

    for cap in do_regex.captures_iter(input).map(|c| c.get(0)) {
        let Some(c) = cap else {
            continue;
        };

        matches.push(Match {
            index: c.start(),
            value: c.as_str().to_owned(),
        });
    }

    for cap in mul_regex.captures_iter(input).map(|c| c.get(0)) {
        let Some(c) = cap else {
            continue;
        };

        matches.push(Match {
            index: c.start(),
            value: c.as_str().to_owned(),
        });
    }

    for cap in dont_regex.captures_iter(input).map(|c| c.get(0)) {
        let Some(c) = cap else {
            continue;
        };

        matches.push(Match {
            index: c.start(),
            value: c.as_str().to_owned(),
        });
    }

    matches
}
