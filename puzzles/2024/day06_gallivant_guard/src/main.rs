use std::collections::HashSet;
use std::fs::File;
use std::io::{BufReader, BufRead};
use std::path::Path;

/// Represents a visit to a cell on the map, storing the direction and coordinates
#[derive(Debug, Clone, PartialEq)]
struct Visit {
    /// Direction the guard was facing when visiting this cell ('>', '<', '^', or 'v')
    direction: char,
    /// Row coordinate of the visited cell
    x: usize,
    /// Column coordinate of the visited cell
    y: usize,
}

/// Parse the input file into a 2D vector of characters representing the map.
///
/// # Arguments
///
/// * `input` - A BufReader containing the input file
///
/// # Returns
///
/// A Vec<Vec<char>> where each inner Vec represents a row of the map
fn parse_input(input: BufReader<File>) -> Vec<Vec<char>> {
    input
        .lines()
        .map(|line| line.unwrap().chars().collect())
        .collect()
}

/// Find the starting position of the guard on the map.
///
/// # Arguments
///
/// * `map` - The 2D vector representing the map
///
/// # Returns
///
/// A tuple (row, column) indicating the guard's starting position
///
/// # Panics
///
/// Panics if no starting position ('^', 'v', '<', or '>') is found on the map
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

/// Check if a given position is outside the map boundaries.
///
/// # Arguments
///
/// * `map` - The 2D vector representing the map
/// * `i` - Row coordinate to check
/// * `j` - Column coordinate to check
///
/// # Returns
///
/// `true` if the position is off the map, `false` otherwise
fn is_off_map(map: &Vec<Vec<char>>, i: isize, j: isize) -> bool {
    i < 0 || j < 0 || i as usize >= map.len() || j as usize >= map[i as usize].len()
}

/// Check if a given position contains an obstacle.
///
/// # Arguments
///
/// * `map` - The 2D vector representing the map
/// * `i` - Row coordinate to check
/// * `j` - Column coordinate to check
///
/// # Returns
///
/// `true` if the position contains an obstacle ('#'), `false` otherwise
fn is_obstacle(map: &Vec<Vec<char>>, i: usize, j: usize) -> bool {
    map[i][j] == '#'
}

/// Print the current state of the map to stdout.
///
/// # Arguments
///
/// * `map` - The 2D vector representing the map
fn print_map(map: &Vec<Vec<char>>) {
    for row in map {
        for cell in row {
            print!("{}", cell);
        }
        println!();
    }
}

/// Check if moving in a given direction from a starting position will lead to a loop.
///
/// # Arguments
///
/// * `map` - The 2D vector representing the map
/// * `visits` - Vector of previous Visit records
/// * `start_x` - Starting row coordinate
/// * `start_y` - Starting column coordinate
/// * `direction` - Direction to check ('>', '<', '^', or 'v')
///
/// # Returns
///
/// `true` if a loop is found in the given direction, `false` otherwise
///
/// # Panics
///
/// Panics if an invalid direction character is provided
fn check_direction_for_loop(
    map: &Vec<Vec<char>>,
    visits: &Vec<Visit>,
    start_x: usize,
    start_y: usize,
    direction: char,
) -> bool {
    let mut x = start_x as isize;
    let mut y = start_y as isize;

    // Define direction offsets
    let (dx, dy) = match direction {
        '>' => (0, 1),
        '<' => (0, -1),
        '^' => (-1, 0),
        'v' => (1, 0),
        _ => panic!("Invalid direction"),
    };

    loop {
        x += dx;
        y += dy;

        // Check if we've gone off the map
        if is_off_map(map, x, y) {
            return false;
        }

        let x_usize = x as usize;
        let y_usize = y as usize;

        // Check if we've hit an obstacle
        if is_obstacle(map, x_usize, y_usize) {
            return false;
        }

        if visits.iter()
            .filter(|v| v.x == x_usize && v.y == y_usize)
            .any(|v| v.direction == direction) {
            return true;
        }
    }
}

fn main() {
    let path = Path::new("sample_input3.txt");
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    let mut map = parse_input(reader);
    // println!("{:?}", map);

    let (start_x, start_y) = find_start_position(&map);
    println!("Start position: ({}, {})", start_x, start_y);

    let mut visits: Vec<Visit> = Vec::new();
    let mut guard_on_map = true;
    let mut i = start_x;
    let mut j = start_y;
    
    visits.push(Visit {
        direction: map[i][j],
        x: i,
        y: j,
    });

    let mut num_loop_options = 0;
    let mut num_obstacles_hit = 0;
    while guard_on_map {
        let current_direction = map[i][j];

        if map[i][j] == '>' {
            if is_off_map(&map, i as isize, j as isize + 1) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i, j + 1) {
                num_obstacles_hit += 1;
                visits.push(Visit {
                    direction: '>',
                    x: i,
                    y: j,
                });
                visits.push(Visit {
                    direction: 'v',
                    x: i,
                    y: j,
                });
                map[i][j] = 'v';
            } else {
                if !is_off_map(&map, i as isize + 1, j as isize)
                    // && map[i + 1][j] == 'X'
                    && check_direction_for_loop(&map, &visits, i, j, 'v')
                    && num_obstacles_hit >= 3
                {
                    println!("Loop option found at ({}, {})", i + 1, j);
                    num_loop_options += 1;
                    // num_obstacles_hit = 0;
                }
                // map[i][j] = '';
                map[i][j + 1] = '>';
                // prev_i = i;
                // prev_j = j;
                j += 1;
            }
        } else if map[i][j] == '<' {
            if is_off_map(&map, i as isize, j as isize - 1) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i, j - 1) {
                num_obstacles_hit += 1;
                visits.push(Visit {
                    direction: '<',
                    x: i,
                    y: j,
                });
                visits.push(Visit {
                    direction: '^',
                    x: i,
                    y: j,
                });
                map[i][j] = '^';
            } else {
                if !is_off_map(&map, i as isize - 1, j as isize)
                    // && map[i - 1][j] == 'X'
                    && check_direction_for_loop(&map, &visits, i, j, '^')
                    && num_obstacles_hit >= 3
                {
                    println!("Loop option found at ({}, {})", i - 1, j);
                    // num_obstacles_hit = 0;
                    num_loop_options += 1;
                }
                // map[i][j] = 'X';
                map[i][j - 1] = '<';
                // prev_i = i;
                // prev_j = j;
                j -= 1;
            }
        } else if map[i][j] == '^' {
            if is_off_map(&map, i as isize - 1, j as isize) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i - 1, j) {
                num_obstacles_hit += 1;
                visits.push(Visit {
                    direction: '^',
                    x: i,
                    y: j,
                });
                visits.push(Visit {
                    direction: '>',
                    x: i,
                    y: j,
                });
                map[i][j] = '>';
            } else {
                if !is_off_map(&map, i as isize - 1, j as isize)
                    // && map[i - 1][j] == 'X'
                    && check_direction_for_loop(&map, &visits, i, j, '>')
                    && num_obstacles_hit >= 3
                {
                    println!("Loop option found at ({}, {})", i - 1, j);
                    // num_obstacles_hit = 0;
                    num_loop_options += 1;
                }
                // map[i][j] = 'X';
                map[i - 1][j] = '^';
                // prev_i = i;
                // prev_j = j;
                i -= 1;
            }
        } else if map[i][j] == 'v' {
            if is_off_map(&map, i as isize + 1, j as isize) {
                map[i][j] = 'X';
                guard_on_map = false;
            } else if is_obstacle(&map, i + 1, j) {
                num_obstacles_hit += 1;
                visits.push(Visit {
                    direction: 'v',
                    x: i,
                    y: j,
                });
                visits.push(Visit {
                    direction: '<',
                    x: i,
                    y: j,
                });
                map[i][j] = '<';
            } else {
                if !is_off_map(&map, i as isize + 1, j as isize)
                    // && map[i + 1][j] == 'X'
                    && check_direction_for_loop(&map, &visits, i, j, '<')
                    && num_obstacles_hit >= 3
                {
                    println!("Loop option found at ({}, {})", i + 1, j);
                    // num_obstacles_hit = 0;
                    num_loop_options += 1;
                }
                // map[i][j] = 'X';
                map[i + 1][j] = 'v';
                // prev_i = i;
                // prev_j = j;
                i += 1;
            }
        }

        if map[i][j] != 'X' && current_direction == map[i][j] {
            visits.push(Visit {
                direction: map[i][j],
                x: i,
                y: j,
            });
        }

        println!();
        println!("{:?}", visits.last().unwrap());
        print_map(&map);
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
    println!("Number of loop options: {}", num_loop_options);
}
