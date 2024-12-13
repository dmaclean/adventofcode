use std::{collections::{HashMap, HashSet}, fs};

fn extract_grid(input: &str) -> Vec<Vec<String>> {
    input
    .lines()
    .map(|line| line
        .chars()
        .map(|c| c.to_string())
        .collect())
    .collect()
}

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

/// Check if the given coordinates are on the grid
fn is_on_grid(grid: &Vec<Vec<String>>, i: i32, j: i32) -> bool {
    i >= 0 && j >= 0 && i < grid.len() as i32 && j < grid[0].len() as i32
}


fn main() {
    let input = fs::read_to_string("input.txt").unwrap();
    let grid: Vec<Vec<String>> = extract_grid(&input);
    let pairs = extract_pairs(&grid);
    
    let mut unique_positions: HashSet<(usize, usize)> = HashSet::new();
    for (symbol, positions) in &pairs {
        // Iterate through pairs of positions
        for i in 0..positions.len()-1 {
            for j in i+1..positions.len() {
                let (i1, j1) = positions[i];
                let (i2, j2) = positions[j];
                let i_diff = (i1 as i32 - i2 as i32).abs();
                let j_diff = (j1 as i32 - j2 as i32).abs();

                // Calculate the new positions
                let mut new_i_1: i32 = 0;
                let mut new_j_1: i32 = 0;
                if i1 < i2 {
                    new_i_1 = i1 as i32 - i_diff;
                } else {
                    new_i_1 = i1 as i32 + i_diff;
                }
                if j1 < j2 {
                    new_j_1 = j1 as i32 - j_diff;
                } else {
                    new_j_1 = j1 as i32 + j_diff;
                }

                let mut new_i_2: i32 = 0;
                let mut new_j_2: i32 = 0;
                if i1 < i2 {
                    new_i_2 = i2 as i32 + i_diff;
                } else {
                    new_i_2 = i2 as i32 - i_diff;
                }
                if j1 < j2 {
                    new_j_2 = j2 as i32 + j_diff;
                } else {
                    new_j_2 = j2 as i32 - j_diff;
                }

                if is_on_grid(&grid, new_i_1, new_j_1) {
                    unique_positions.insert((new_i_1 as usize, new_j_1 as usize));
                }
                if is_on_grid(&grid, new_i_2, new_j_2) {
                    unique_positions.insert((new_i_2 as usize, new_j_2 as usize));
                }
            }
        }
    }
    println!("{:?}", unique_positions.len());
    println!("{:?}", unique_positions);
}
