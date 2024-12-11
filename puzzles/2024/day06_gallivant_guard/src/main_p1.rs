use std::fs::File;
use std::io::{BufReader, BufRead};
use std::path::Path;

/// Parse the input into a 2D vector of characters.
fn parse_input(input: BufReader<File>) -> Vec<Vec<char>> {
    input
        .lines()
        .map(|line| line.unwrap().chars().collect())
        .collect()
}

fn find_start_position(map: &Vec<Vec<char>>) -> (usize, usize) {
    for i in 0..map.len() {
        for j in 0..map[i].len() {
            if map[i][j] == '^' || map[i][j] == 'v' || map[i][j] == '<' || map[i][j] == '>' {
                return (i, j);
            }
        }
    }
    panic!("Start position not found");
}

fn is_off_map(map: &Vec<Vec<char>>, i: usize, j: usize) -> bool {
    i < 0 || j < 0 || i >= map.len() || j >= map[i].len()
}

fn is_obstacle(map: &Vec<Vec<char>>, i: usize, j: usize) -> bool {
    map[i][j] == '#'
}

fn print_map(map: &Vec<Vec<char>>) {
    for row in map {
        for cell in row {
            print!("{}", cell);
        }
        println!();
    }
}

fn main() {
    let path = Path::new("input.txt");
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    let mut map = parse_input(reader);
    println!("{:?}", map);

    let (start_x, start_y) = find_start_position(&map);
    println!("Start position: ({}, {})", start_x, start_y);

    let mut guard_on_map = true;
    let mut i = start_x;
    let mut j = start_y;
    while guard_on_map {
        // println!();
        // print_map(&map);

        if map[i][j] == '>' {
            if is_off_map(&map, i, j + 1) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i, j + 1) {
                map[i][j] = 'v';
            } else {
                map[i][j] = 'X';
                map[i][j + 1] = '>';
                j += 1;
            }
        } else if map[i][j] == '<' {
            if is_off_map(&map, i, j - 1) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i, j - 1) {
                map[i][j] = '^';
            } else {
                map[i][j] = 'X';
                map[i][j - 1] = '<';
                j -= 1;
            }
        } else if map[i][j] == '^' {
            if is_off_map(&map, i - 1, j) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i - 1, j) {
                map[i][j] = '>';
            } else {
                map[i][j] = 'X';
                map[i - 1][j] = '^';
                i -= 1;
            }
        } else if map[i][j] == 'v' {
            if is_off_map(&map, i + 1, j) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i + 1, j) {
                map[i][j] = '<';
            } else {
                map[i][j] = 'X';
                map[i + 1][j] = 'v';
                i += 1;
            }
        }
    }

    let mut num_visited = 0;
    for row in map {
        for cell in row {
            if cell == 'X' {
                num_visited += 1;
            }
        }
    }
    println!("Number of visited cells: {}", num_visited);
}
