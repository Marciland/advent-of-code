use std::convert::TryInto;

#[derive(Clone)]
struct Position {
    pub x: i16,
    pub y: i16,
}

impl PartialEq for Position {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl Position {
    pub fn left(&self) -> Position {
        Position {
            x: self.x - 1,
            y: self.y,
        }
    }

    pub fn right(&self) -> Position {
        Position {
            x: self.x + 1,
            y: self.y,
        }
    }

    pub fn up(&self) -> Position {
        Position {
            x: self.x,
            y: self.y - 1,
        }
    }

    pub fn down(&self) -> Position {
        Position {
            x: self.x,
            y: self.y + 1,
        }
    }

    pub fn neighbours(&self) -> Vec<Position> {
        vec![self.left(), self.right(), self.up(), self.down()]
    }
}

struct Garden {
    pub width: usize,
    pub height: usize,
    pub map: Vec<Vec<char>>,
}

impl Garden {
    pub fn find_regions(&self) -> Vec<Region> {
        let mut regions = Vec::new();

        for y in 0..self.height {
            for x in 0..self.width {
                let current_position = Position {
                    x: x.try_into().unwrap(),
                    y: y.try_into().unwrap(),
                };

                let mut plants = Vec::new();
                self.find_region(
                    &current_position,
                    self.plant(&current_position),
                    &mut plants,
                );

                regions.push(Region { plants });
            }
        }

        regions
    }

    fn plant(&self, position: &Position) -> char {
        #[allow(clippy::cast_sign_loss)]
        self.map[position.y as usize][position.x as usize]
    }

    fn find_region(&self, current_position: &Position, plant: char, plants: &mut Vec<Position>) {
        for position in plants.iter() {
            if current_position == position {
                return;
            }
        }

        plants.push(current_position.clone());

        for neighbour in current_position.neighbours() {
            if !self.is_in_bounds(&neighbour) {
                continue;
            }

            if self.plant(&neighbour) != plant {
                continue;
            }

            self.find_region(&neighbour, plant, plants);
        }
    }

    fn is_in_bounds(&self, position: &Position) -> bool {
        if position.x < 0 || position.y < 0 {
            return false;
        }

        #[allow(clippy::cast_sign_loss)]
        let x = position.x as usize;
        #[allow(clippy::cast_sign_loss)]
        let y = position.y as usize;

        x < self.width && y < self.height
    }
}

struct Region {
    pub plants: Vec<Position>,
}

impl PartialEq for Region {
    fn eq(&self, other: &Self) -> bool {
        let mut eq = true;
        for other_pos in &other.plants {
            if !self.plants.contains(other_pos) {
                eq = false;
            }
        }

        for pos in &self.plants {
            if !other.plants.contains(pos) {
                eq = false;
            }
        }

        eq
    }
}

impl Region {
    pub fn price(&self) -> u64 {
        let area = self.plants.len();
        let perimeter = self.perimeter();

        area as u64 * perimeter
    }

    pub fn price_sides(&self) -> u64 {
        let area = self.plants.len();
        let sides = self.sides();

        area as u64 * sides
    }

    fn sides(&self) -> u64 {
        let mut max_x = 0;
        let mut max_y = 0;
        for plant in &self.plants {
            if plant.x > max_x {
                max_x = plant.x;
            }
            if plant.y > max_y {
                max_y = plant.y;
            }
        }

        let mut min_x = max_x;
        let mut min_y = max_y;
        for plant in &self.plants {
            if plant.x < min_x {
                min_x = plant.x;
            }
            if plant.y < min_y {
                min_y = plant.y;
            }
        }
        /*
        self.left(min_x, max_x, min_y, max_y)
            + self.right(min_x, max_x, min_y, max_y)
            + self.above(min_x, max_x, min_y, max_y)
            + self.below(min_x, max_x, min_y, max_y)
            */
        0
    }

    fn perimeter(&self) -> u64 {
        let mut fences: u64 = 0;

        for position in &self.plants {
            let mut fence: u8 = 4;
            for neighbour in position.neighbours() {
                if self.plants.contains(&neighbour) {
                    fence -= 1;
                }
            }
            fences += u64::from(fence);
        }

        fences
    }
}

fn parse_input(input: &[String]) -> Garden {
    let mut map = Vec::with_capacity(input.len());

    for line in input {
        let mut row: Vec<char> = Vec::with_capacity(line.len());

        for char in line.chars() {
            row.push(char);
        }

        map.push(row);
    }

    Garden {
        width: input.first().unwrap().len(),
        height: input.len(),
        map,
    }
}

pub fn star1(input: &[String]) {
    /*
       Find all regions
       multiply area by perimeter
       sum prices
    */
    let garden = parse_input(input);

    let regions = garden.find_regions();

    let mut unique_regions = Vec::new();
    for region in regions {
        if !unique_regions.contains(&region) {
            unique_regions.push(region);
        }
    }

    let mut total_price = 0;
    for region in unique_regions {
        total_price += region.price();
    }

    println!("{total_price}");
}

pub fn star2(input: &[String]) {
    /*
        instead of counting fences, count sides
    */
    let garden = parse_input(input);

    let regions = garden.find_regions();

    let mut unique_regions = Vec::new();
    for region in regions {
        if !unique_regions.contains(&region) {
            unique_regions.push(region);
        }
    }

    let mut total_price = 0;
    for region in unique_regions {
        let price = region.price_sides();

        total_price += price;
    }

    println!("{total_price}");
}
