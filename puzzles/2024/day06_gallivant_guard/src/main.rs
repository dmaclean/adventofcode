use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufReader, BufRead};
use std::path::Path;

type Position = (usize, usize);
type VisitState = (usize, usize, char);
type Grid = Vec<Vec<char>>;
#[derive(Debug)]
enum Error {
    NoStartPosition,
    Io(io::Error),
    InvalidDirection(char),
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Error::NoStartPosition => write!(f, "No starting position found in map"),
            Error::Io(err) => write!(f, "IO error: {}", err),
            Error::InvalidDirection(c) => write!(f, "Invalid direction character: {}", c),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Io(err) => Some(err),
            _ => None
        }
    }
}

impl From<io::Error> for Error {
    fn from(err: io::Error) -> Self {
        Error::Io(err)
    }
}

/// Parse the input file into a 2D grid of characters.
///
/// # Arguments
///
/// * `input` - A BufRead implementation containing the input file
///
/// # Returns
///
/// A Result containing the Grid (Vec<Vec<char>>) where each inner Vec represents a row
fn parse_input(input: impl BufRead) -> io::Result<Grid> {
    input.lines()
        .map(|line| line.map(|l| l.chars().collect()))
        .collect()
}

/// Find the starting position of the guard on the map.
///
/// # Arguments
///
/// * `map` - The 2D grid representing the map
///
/// # Returns
///
/// A Result containing a Position tuple (row, column) indicating the guard's starting position
///
/// # Errors
///
/// Returns NoStartPosition if no starting position ('^', 'v', '<', or '>') is found
fn find_start_position(map: &Grid) -> Result<Position, Error> {
    for (i, row) in map.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {
            if matches!(cell, '^' | 'v' | '<' | '>') {
                return Ok((i, j));
            }
        }
    }
    Err(Error::NoStartPosition)
}

/// Check if a given position is outside the map boundaries.
///
/// # Arguments
///
/// * `map` - The 2D grid representing the map
/// * `i` - Row coordinate to check (can be negative)
/// * `j` - Column coordinate to check (can be negative)
///
/// # Returns
///
/// `true` if the position is off the map, `false` otherwise
fn is_off_map(map: &Grid, i: isize, j: isize) -> bool {
    i < 0 || j < 0 || i as usize >= map.len() || j as usize >= map[0].len()
}

/// Check if a given position contains an obstacle.
///
/// # Arguments
///
/// * `map` - The 2D grid representing the map
/// * `i` - Row coordinate to check
/// * `j` - Column coordinate to check
///
/// # Returns
///
/// `true` if the position contains an obstacle ('#'), `false` otherwise
fn is_obstacle(map: &Grid, i: usize, j: usize) -> bool {
    map[i][j] == '#'
}

/// Get the next direction when hitting an obstacle (turning right).
///
/// # Arguments
///
/// * `direction` - Current direction character ('>', '<', '^', or 'v')
///
/// # Returns
///
/// A Result containing the next direction character after turning right
///
/// # Errors
///
/// Returns InvalidDirection if the input direction is not valid
fn turn_right(direction: char) -> Result<char, Error> {
    match direction {
        '>' => Ok('v'),
        'v' => Ok('<'),
        '<' => Ok('^'),
        '^' => Ok('>'),
        c => Err(Error::InvalidDirection(c)),
    }
}

/// Simulates the guard's path with an additional obstacle to check for loops.
///
/// # Arguments
///
/// * `original_map` - The original 2D grid representing the map
/// * `obstacle_pos` - Position tuple (row, column) where to place the additional obstacle
///
/// # Returns
///
/// A Result containing a boolean: true if a loop is found, false if guard exits map
///
/// # Errors
///
/// Returns InvalidDirection if an invalid direction is encountered during simulation
fn simulate_path_with_obstacle(original_map: &Grid, obstacle_pos: Position) -> Result<bool, Error> {
    let mut map = original_map.clone();
    let (obstacle_x, obstacle_y) = obstacle_pos;
    map[obstacle_x][obstacle_y] = '#';

    let (mut i, mut j) = find_start_position(&map)?;
    let mut visits = HashSet::new();
    visits.insert((i, j, map[i][j]));

    loop {
        let (next_i, next_j) = match map[i][j] {
            '>' => (i as isize, j as isize + 1),
            '<' => (i as isize, j as isize - 1),
            '^' => (i as isize - 1, j as isize),
            'v' => (i as isize + 1, j as isize),
            c => return Err(Error::InvalidDirection(c)),
        };

        if is_off_map(&map, next_i, next_j) {
            return Ok(false);
        }

        let next_i = next_i as usize;
        let next_j = next_j as usize;

        if is_obstacle(&map, next_i, next_j) {
            map[i][j] = turn_right(map[i][j])?;
        } else {
            map[next_i][next_j] = map[i][j];
            i = next_i;
            j = next_j;
        }

        if !visits.insert((i, j, map[i][j])) {
            return Ok(true);
        }
    }
}

fn main() -> Result<(), Error> {
    let path = Path::new("input.txt");
    let reader = BufReader::new(File::open(path)?);
    let map = parse_input(reader)?;

    let start_pos = find_start_position(&map)?;
    println!("Start position: {:?}", start_pos);

    let mut num_loop_options = 0;
    
    // Try placing an additional obstacle at each empty position
    for i in 0..map.len() {
        for j in 0..map[0].len() {
            if map[i][j] == '.' && simulate_path_with_obstacle(&map, (i, j))? {
                println!("Loop option found with obstacle at ({}, {})", i, j);
                num_loop_options += 1;
            }
        }
    }

    println!("Number of loop options: {}", num_loop_options);
    Ok(())
}
