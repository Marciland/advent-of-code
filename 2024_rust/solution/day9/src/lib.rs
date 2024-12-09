use std::convert::TryFrom;

#[derive(Clone, PartialEq)]
struct File {
    pub id: Option<u64>,
    pub size: u64,
}

struct Disk {
    pub map: Vec<File>,
}

impl Disk {
    fn first_free_space_index(&self) -> usize {
        self.map.iter().position(|file| file.id.is_none()).unwrap()
    }

    fn last_file_index(&self) -> usize {
        self.map.len()
            - 1
            - self
                .map
                .iter()
                .rev()
                .position(|file| file.id.is_some())
                .unwrap()
    }

    pub fn compact(&mut self) -> &mut Self {
        loop {
            let free_space_index = self.first_free_space_index();
            let last_file_index = self.last_file_index();

            if free_space_index > last_file_index {
                break;
            }

            let mut free_space = self.map.remove(free_space_index);
            let mut last_file = self.map.remove(last_file_index - 1);

            if free_space.size == last_file.size {
                self.map.insert(free_space_index, last_file);
                self.map.insert(last_file_index, free_space);
                continue;
            }

            if free_space.size > last_file.size {
                free_space.size -= last_file.size;

                self.map.insert(free_space_index, last_file);
                self.map.insert(free_space_index + 1, free_space);
                continue;
            }

            if free_space.size < last_file.size {
                let remaining_file = File {
                    id: last_file.id,
                    size: last_file.size - free_space.size,
                };
                last_file.size = free_space.size;

                self.map.insert(free_space_index, last_file);
                self.map.insert(last_file_index, remaining_file);
            }
        }

        self
    }

    pub fn quick_sum(&mut self) -> u64 {
        let mut files: Vec<File> = self
            .map
            .iter()
            .filter_map(|file| {
                if file.id.is_some() {
                    Some(file.clone())
                } else {
                    None
                }
            })
            .collect();
        files.sort_by_key(|file| file.id.unwrap());
        files.reverse();

        let mut checksum = 0;

        let mut file_position: usize = 0;
        let mut block_position: u64 = 0;
        loop {
            if file_position == self.map.len() {
                break;
            }

            let file = self.map.get(file_position).unwrap();

            if let Some(id) = file.id {
                for _ in 0..file.size {
                    checksum += block_position * id;
                    block_position += 1;
                }

                let mut file_index = None;
                for (index, f) in files.iter().enumerate() {
                    if id == f.id.unwrap() {
                        file_index = Some(index);
                        break;
                    }
                }

                if let Some(index) = file_index {
                    files.remove(index);
                }
            } else {
                let mut file_index = None;
                let file_size = file.size;

                for (index, f) in files.iter().enumerate() {
                    if f.size > file.size {
                        continue;
                    }

                    for _ in 0..f.size {
                        checksum += block_position * f.id.unwrap();
                        block_position += 1;
                    }

                    if f.size < file.size {
                        self.map.insert(
                            file_position + 1,
                            File {
                                id: None,
                                size: file.size - f.size,
                            },
                        );
                    }

                    let mut map_file_index = None;
                    for (map_index, map_file) in self.map.iter().enumerate() {
                        if map_file.id.is_none() {
                            continue;
                        }

                        if f.id.unwrap() == map_file.id.unwrap() {
                            map_file_index = Some(map_index);
                            break;
                        }
                    }

                    self.map.remove(map_file_index.unwrap());
                    self.map.insert(
                        map_file_index.unwrap(),
                        File {
                            id: None,
                            size: f.size,
                        },
                    );

                    file_index = Some(index);
                    break;
                }

                match file_index {
                    Some(index) => {
                        files.remove(index);
                    }
                    None => {
                        for _ in 0..file_size {
                            block_position += 1;
                        }
                    }
                };
            };

            file_position += 1;
        }

        checksum
    }

    pub fn checksum(&self) -> u64 {
        let mut checksum = 0;

        let mut block_position = -1;
        for file in &self.map {
            for _ in 0..file.size {
                block_position += 1;

                if file.id.is_none() {
                    continue;
                }

                checksum += u64::try_from(block_position).unwrap() * file.id.unwrap();
            }
        }

        checksum
    }
}

fn parse_input(input: &[String]) -> Disk {
    let input = input.join("");
    let numbers: Vec<u64> = input
        .chars()
        .map(|c| u64::from(c.to_digit(10).expect("Not a base 10 digit")))
        .collect();

    let mut map: Vec<File> = Vec::with_capacity(input.len());
    let mut file_id: u64 = 0;
    for (index, number) in numbers.iter().enumerate() {
        let is_file = index % 2 == 0;

        if !is_file {
            file_id += 1;
        }

        let file = File {
            id: if is_file { Some(file_id) } else { None },
            size: *number,
        };

        map.push(file);
    }

    Disk { map }
}

pub fn star1(input: &[String]) {
    /*
        disk map:
            alternating file, free space
            file id incrementing, ignoring free space

        compacting:
            move from end of file to start of gap

        checksum:
            block position * file id number
            sum the products
    */
    let checksum = parse_input(input).compact().checksum();

    println!("{checksum}");
}

pub fn star2(input: &[String]) {
    /*
        Move files whole if possible
    */

    let checksum = parse_input(input).quick_sum();

    println!("{checksum}");
}
