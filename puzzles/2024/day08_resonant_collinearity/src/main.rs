use std::{collections::{HashMap, HashSet}, fs};

/// Converts the input string into a 2D grid of strings.
/// 
/// # Arguments
/// 
/// * `input` - A string containing newline-separated rows of characters
/// 
/// # Returns
/// 
/// Returns a Vec<Vec<String>> where each character from the input is converted to a String
/// in a 2D grid structure.
/// 
/// # Example
/// 
/// ```
/// let input = "1.2\n.3.\n4.5";
/// let grid = extract_grid(input);
/// assert_eq!(grid[0][0], "1");
/// assert_eq!(grid[1][1], "3");
/// ```
fn extract_grid(input: &str) -> Vec<Vec<String>> {
    input
    .lines()
    .map(|line| line
        .chars()
        .map(|c| c.to_string())
        .collect())
    .collect()
}

/// Creates a HashMap mapping symbols to their positions in the grid.
/// 
/// # Arguments
/// 
/// * `grid` - A 2D vector of strings representing the grid
/// 
/// # Returns
/// 
/// Returns a HashMap where:
/// * Keys are the symbols found in the grid (excluding ".")
/// * Values are vectors of (row, column) coordinates where each symbol appears
/// 
/// # Details
/// 
/// * Ignores "." characters in the grid
/// * Each position is stored as a tuple of (row, column) coordinates
/// * If a symbol appears multiple times, all positions are stored in the vector
fn extract_pairs(grid: &Vec<Vec<String>>) -> HashMap<String, Vec<(usize, usize)>> {
    let mut pairs: HashMap<String, Vec<(usize, usize)>> = HashMap::new();
    for (i, row) in grid.iter().enumerate() {
        for (j, cell) in row.iter().enumerate() {
            if cell == "." {
                continue;
            }
            pairs.entry(cell.clone())
                .and_modify(|v| v.push((i, j)))
                .or_insert_with(|| vec![(i, j)]);
        }
    }
    pairs
}

/// Checks if given coordinates are within the bounds of the grid.
/// 
/// # Arguments
/// 
/// * `grid` - The 2D grid to check against
/// * `i` - Row index (can be negative)
/// * `j` - Column index (can be negative)
/// 
/// # Returns
/// 
/// Returns `true` if both conditions are met:
/// * Both indices are non-negative
/// * Both indices are within the grid dimensions
/// 
/// # Note
/// 
/// This function accepts i32 coordinates to handle negative index checking,
/// but compares against usize grid dimensions after conversion.
fn is_on_grid(grid: &Vec<Vec<String>>, i: i32, j: i32) -> bool {
    i >= 0 && j >= 0 && i < grid.len() as i32 && j < grid[0].len() as i32
}

/// Main entry point for the antenna placement calculator.
/// 
/// # Algorithm
/// 
/// 1. Reads the grid from "input.txt"
/// 2. Identifies all pairs of matching symbols
/// 3. For each pair:
///    - Calculates possible antenna positions in both directions
///    - Marks valid positions with "#"
///    - Stores unique positions in a HashSet
/// 4. Calculates and prints the total number of valid positions:
///    - Sum of unique new positions
///    - Plus the count of original antenna positions
/// 
/// # Panics
/// 
/// Will panic if:
/// * "input.txt" cannot be read
/// * The input file contains invalid UTF-8
/// * The grid is empty or malformed
fn main() {
    let input = fs::read_to_string("input.txt").unwrap();
    let mut grid: Vec<Vec<String>> = extract_grid(&input);
    let pairs = extract_pairs(&grid);
    
    let mut unique_positions: HashSet<(usize, usize)> = HashSet::new();
    for (_, positions) in &pairs {
        // Iterate through pairs of positions
        for i in 0..positions.len()-1 {
            for j in i+1..positions.len() {
                let (i1, j1) = positions[i];
                let (i2, j2) = positions[j];
                let i_diff = (i1 as i32 - i2 as i32).abs();
                let j_diff = (j1 as i32 - j2 as i32).abs();

                // Calculate the new positions, continuing until we go off the grid
                let mut new_i_1: i32 = i1 as i32;
                let mut new_j_1: i32 = j1 as i32;
                while is_on_grid(&grid, new_i_1, new_j_1) {
                    if i1 < i2 {
                        new_i_1 = new_i_1 - i_diff;
                    } else {
                        new_i_1 = new_i_1 + i_diff;
                    }
                    if j1 < j2 {
                        new_j_1 = new_j_1 - j_diff;
                    } else {
                        new_j_1 = new_j_1 + j_diff;
                    }
                    if is_on_grid(&grid, new_i_1, new_j_1)
                        && grid[new_i_1 as usize][new_j_1 as usize] == "." {
                        unique_positions.insert((new_i_1 as usize, new_j_1 as usize));
                        grid[new_i_1 as usize][new_j_1 as usize] = "#".to_string();
                    }
                }

                // Calculate the new positions in opposite direction, continuing until we go off the grid
                let mut new_i_2: i32 = i2 as i32;
                let mut new_j_2: i32 = j2 as i32;
                while is_on_grid(&grid, new_i_2, new_j_2) {
                    if i1 < i2 {
                        new_i_2 = new_i_2 + i_diff;
                    } else {
                        new_i_2 = new_i_2 - i_diff;
                    }
                    if j1 < j2 {
                        new_j_2 = new_j_2 + j_diff;
                    } else {
                        new_j_2 = new_j_2 - j_diff;
                    }
                    if is_on_grid(&grid, new_i_2, new_j_2)
                        && grid[new_i_2 as usize][new_j_2 as usize] == "." {
                        unique_positions.insert((new_i_2 as usize, new_j_2 as usize));
                        grid[new_i_2 as usize][new_j_2 as usize] = "#".to_string();
                    }
                }
            }
        }
    }
    let num_antennas = pairs
        .values()
        .map(|positions| positions.len())
        .sum::<usize>();
    println!("{:?}", unique_positions.len() + num_antennas);
}
