use log::debug;
use env_logger;

#[derive(Debug)]
struct Stone {
    num: u64,
    length: u8
}

fn create_stone_from_string(s: &str) -> Stone {
    let num = s.parse::<u64>().unwrap();
    let length = s.parse::<u64>().unwrap().to_string().len() as u8;
    Stone { num, length }
}

fn extract_stones(s: &str) -> Vec<Stone> {
    s.split_whitespace()
        .map(|s| create_stone_from_string(s))
        .collect::<Vec<Stone>>()
}

fn print_stones(stones: &Vec<Stone>) {
    for stone in stones {
        debug!("{} ", stone.num);
    }
    debug!("");
}

fn main() {
    env_logger::init();

    let input = std::fs::read_to_string("input.txt").unwrap();

    let mut stones = extract_stones(&input);

    for i in 0 .. 75 {
        let mut s = 0;
        while s < stones.len() {
            let stone = &mut stones[s];

            if stone.num == 0 {
                // Replace with stone with number 1
                stones[s] = Stone { num: 1, length: 1 };
                s += 1;
            } else if stone.length % 2 == 0 {
                let left_stone_val_str = stone.num
                    .to_string()
                    .chars()
                    .take(stone.length as usize / 2)
                    .collect::<String>();
                let left_stone = create_stone_from_string(&left_stone_val_str);

                let right_stone_val_str = stone.num
                    .to_string()
                    .chars()
                    .skip(stone.length as usize / 2)
                    .collect::<String>();
                let right_stone = create_stone_from_string(&right_stone_val_str);

                stones[s] = left_stone;
                stones.insert(s + 1, right_stone);
                s += 2;
            } else {
                stones[s] = Stone { num: stone.num * 2024, length: (stone.num * 2024).to_string().len() as u8 };
                s += 1;
            }
            // print_stones(&stones);
        }
        println!("Finished iteration {} with {} stones", i, stones.len());
    }

    println!("{}", stones.len());
}
