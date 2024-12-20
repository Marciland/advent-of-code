use std::collections::HashMap;

struct Onsen {
    pub patterns: Vec<String>,
    pub designs: Vec<String>,
}

impl Onsen {
    pub fn get_possibilities(&self) -> u64 {
        let mut possibilities: u64 = 0;

        for design in &self.designs {
            for pattern in &self.patterns {
                possibilities += self.possibilities(design, pattern, &mut HashMap::new());
            }
        }

        possibilities
    }

    pub fn get_possible(&self) -> u64 {
        let mut possible = 0;

        for design in &self.designs {
            for pattern in &self.patterns {
                if self.possibilities(design, pattern, &mut HashMap::new()) >= 1 {
                    possible += 1;
                    break;
                }
            }
        }

        possible
    }

    fn possibilities(
        &self,
        design: &str,
        result: &str,
        cache: &mut HashMap<(String, String), u64>,
    ) -> u64 {
        if design == result {
            return 1;
        }

        if !design.starts_with(result) {
            return 0;
        }

        let key = (design.to_owned(), result.to_owned());
        if let Some(&cached) = cache.get(&key) {
            return cached;
        }

        let mut can_build = 0;
        for pattern in &self.patterns {
            let new_result = result.to_owned() + pattern;
            can_build += self.possibilities(design, &new_result, cache);
        }

        cache.insert(key, can_build);

        can_build
    }
}

fn parse_input(input: &[String]) -> Onsen {
    let parts = input.split(String::is_empty).collect::<Vec<&[String]>>();

    let patterns: Vec<String> = parts[0]
        .join("")
        .split(',')
        .map(|str| str.trim().to_owned())
        .collect();

    let designs = parts[1].to_owned();

    Onsen { patterns, designs }
}

pub fn star1(input: &[String]) {
    /*
        Arrange the towels
        order is important
        how many designs are possible with the given patterns?
    */
    let onsen = parse_input(input);

    println!("{}", onsen.get_possible());
}

pub fn star2(input: &[String]) {
    /*
       Not only check IF, but how many possibilities
    */
    let onsen = parse_input(input);

    println!("{}", onsen.get_possibilities());
}
