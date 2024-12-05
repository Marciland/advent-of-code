use std::convert::TryFrom;

#[derive(Clone)]
struct Rule {
    pub before: u32,
    pub after: u32,
}

impl Rule {
    fn is_ignored(before: i8, after: i8) -> bool {
        before == -1 || after == -1
    }
}

struct Update {
    pub pages: Vec<u32>,
}

impl Update {
    fn fix(&mut self, rules: &[Rule]) {
        for rule in rules {
            let (before, after) = self.get_rule_indices(rule);
            if Rule::is_ignored(before, after) {
                continue;
            }

            if before < after {
                continue;
            }

            #[allow(clippy::cast_sign_loss)]
            let before_index = before as usize;
            #[allow(clippy::cast_sign_loss)]
            let after_index = after as usize;

            let after_page = self.pages.remove(after_index);
            if self.pages.len() == before_index {
                self.pages.push(after_page);
                continue;
            }

            self.pages.insert(before_index + 1, after_page);
        }
    }

    fn get_rule_indices(&self, rule: &Rule) -> (i8, i8) {
        let mut before_index: i8 = -1;
        let mut after_index: i8 = -1;

        for (index, page) in self.pages.iter().enumerate() {
            if rule.before == *page {
                before_index = i8::try_from(index).expect("Out of range for i8");
            }

            if rule.after == *page {
                after_index = i8::try_from(index).expect("Out of range for i8");
            }
        }

        (before_index, after_index)
    }

    fn is_valid(&self, rules: &[Rule]) -> bool {
        for rule in rules {
            let (before, after) = self.get_rule_indices(rule);

            if Rule::is_ignored(before, after) {
                continue;
            }

            if before > after {
                return false;
            }
        }

        true
    }

    fn middle(&self) -> &u32 {
        self.pages.get(self.pages.len() / 2).unwrap()
    }
}

fn split_input(input: &[String]) -> (Vec<Rule>, Vec<Update>) {
    let mut rules = Vec::new();
    let mut updates = Vec::new();

    let mut processing_rules = true;
    for line in input {
        if line.is_empty() {
            processing_rules = false;
            continue;
        }

        if processing_rules {
            let rule: Vec<&str> = line.split('|').collect();
            assert_eq!(rule.len(), 2);
            rules.push(Rule {
                before: rule[0].parse::<u32>().expect("Not a number"),
                after: rule[1].parse::<u32>().expect("Not a number"),
            });
            continue;
        }

        let update: Vec<&str> = line.split(',').collect();
        updates.push(Update {
            pages: update
                .iter()
                .map(|page| page.parse::<u32>().expect("Not a number"))
                .collect(),
        });
    }

    (rules, updates)
}

pub fn star1(input: &[String]) {
    /*
        Rules & Updates
            left must be before right in updates
        for each update that is OK, sum the middle numbers
    */
    let (rules, updates) = split_input(input);

    let mut sum = 0;
    for update in updates {
        if update.is_valid(&rules) {
            sum += update.middle();
        }
    }

    println!("{sum}");
}

pub fn star2(input: &[String]) {
    /*
        Fix invalids and then sum their middle
    */
    let (rules, updates) = split_input(input);

    let mut sum = 0;
    for mut update in updates {
        if update.is_valid(&rules) {
            continue;
        }

        while !update.is_valid(&rules) {
            update.fix(&rules);
        }

        sum += update.middle();
    }

    println!("{sum}");
}
