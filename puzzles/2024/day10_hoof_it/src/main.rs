use log::debug;

/// Main function that processes the hiking map and finds all possible paths to peaks.
/// Reads input from a file, finds all starting points (height 0), and calculates
/// the total number of unique paths to peaks (height 9).
fn main() {
    env_logger::init();
    let input = std::fs::read_to_string("input.txt").unwrap();
    let map = extract_map(&input);
    debug!("{:?}", &map);
    let start_points = find_start_point(&map);
    let mut scores = 0;
    for start in start_points {
        let mut visited = Vec::new();
        let mut peak_paths: Vec<Vec<(usize, usize)>> = Vec::new();
        hike(&map, &mut visited, start.0, start.1, &mut peak_paths);
        debug!("Peak paths for start: (r:{}, c:{}) - {}", start.0, start.1, peak_paths.len());
        scores += peak_paths.len();
    }
    println!("{}", scores);
}

/// Recursively explores all possible paths from a given position to peaks.
/// 
/// # Arguments
/// * `map` - The 2D grid representing heights
/// * `visited` - Vector tracking the current path being explored
/// * `r` - Current row position
/// * `c` - Current column position
/// * `peak_paths` - Collection of all valid paths found to peaks
///
/// A valid path must increase in height by exactly 1 at each step and end at height 9.
fn hike(map: &Vec<Vec<i8>>, visited: &mut Vec<(usize, usize)>, r: usize, c: usize, peak_paths: &mut Vec<Vec<(usize, usize)>>) {
    visited.push((r, c));
    debug!("Visiting: (r:{}, c:{}) - {}", r, c, map[r][c]);

    if map[r][c] == 9 {
        peak_paths.push(visited.clone());
        debug!("Peak found: (r:{}, c:{}) - {:?}", r, c, &visited);
        visited.pop();
        return;
    }

    // Check up
    if is_valid_move(map, visited, r as i32 - 1, c as i32, map[r][c] as u8) {
        hike(map, visited, r - 1, c, peak_paths);
    }

    // Check down
    if is_valid_move(map, visited, r as i32 + 1, c as i32, map[r][c] as u8) {
        hike(map, visited, r + 1, c, peak_paths);
    }

    // Check left
    if is_valid_move(map, visited, r as i32, c as i32 - 1, map[r][c] as u8) {
        hike(map, visited, r, c - 1, peak_paths);
    }

    // Check right
    if is_valid_move(map, visited, r as i32, c as i32 + 1, map[r][c] as u8) {
        hike(map, visited, r, c + 1, peak_paths);
    }

    visited.pop();
    debug!("Backtracking from: (r:{}, c:{}) - {}", r, c, map[r][c]);
}

/// Checks if a move to a new position is valid.
/// 
/// # Arguments
/// * `map` - The 2D grid representing heights
/// * `visited` - Vector of positions already visited in current path
/// * `r` - Target row position (can be negative for boundary checking)
/// * `c` - Target column position (can be negative for boundary checking)
/// * `current_height` - Height of the current position
///
/// # Returns
/// `true` if the move is valid (in bounds, not visited, and exactly one height higher)
fn is_valid_move(map: &Vec<Vec<i8>>, visited: &Vec<(usize, usize)>, r: i32, c: i32, current_height: u8) -> bool {
    let r_idx = match usize::try_from(r) {
        Ok(val) => val,
        Err(_) => return false,
    };
    let c_idx = match usize::try_from(c) {
        Ok(val) => val,
        Err(_) => return false,
    };

    if r_idx >= map.len() || c_idx >= map[0].len() {
        return false;
    }

    if visited.contains(&(r_idx, c_idx)) {
        return false;
    }

    let target_height = map[r_idx][c_idx];
    target_height == current_height as i8 + 1
}

/// Finds all starting points (positions with height 0) in the map.
/// 
/// # Arguments
/// * `map` - The 2D grid representing heights
///
/// # Returns
/// Vector of (row, column) coordinates for all starting positions
fn find_start_point(map: &Vec<Vec<i8>>) -> Vec<(usize, usize)> {
    let mut start_points = Vec::new();
    for (r, row) in map.iter().enumerate() {
        for (c, &cell) in row.iter().enumerate() {
            if cell == 0 {
                start_points.push((r, c));
            }
        }
    }
    start_points
}

/// Converts the input string into a 2D grid of heights.
/// 
/// # Arguments
/// * `input` - String containing the map data
///
/// # Returns
/// 2D vector where:
/// * -1 represents '.' (invalid position)
/// * 0-9 represent heights
///
/// Each character in the input is converted to a number, with '.'
/// being converted to -1 and digits being converted to their numeric value.
fn extract_map(input: &str) -> Vec<Vec<i8>> {
    input.lines()
        .map(|line| line.chars()
            .map(|c| if c == '.' { -1 } else { c.to_digit(10).unwrap() as i8 })
            .collect())
        .collect()
}
