use std::collections::HashSet;

fn main() {
    let input = std::fs::read_to_string("input.txt").unwrap();
    let map = extract_map(&input);
    // print_map(&map);
    let start_points = find_start_point(&map);
    let mut scores = 0;
    for start in start_points {
        let mut visited = Vec::new();
        let mut peaks_visited: HashSet<(usize, usize)> = HashSet::new();
        hike(&map, &mut visited, start.0, start.1, &mut peaks_visited);
        scores += peaks_visited.len();
    }
    println!("{}", scores);
}

fn hike(map: &Vec<Vec<i8>>, visited: &mut Vec<(usize, usize)>, r: usize, c: usize, peaks_visited: &mut HashSet<(usize, usize)>) {
    visited.push((r, c));
    println!("Visiting: (r:{}, c:{}) - {}", r, c, map[r][c]);

    if map[r][c] == 9 {
        peaks_visited.insert((r, c));
        println!("Peak found: (r:{}, c:{}) - {}", r, c, map[r][c]);
        return;
    }

    // Check up
    if is_valid_move(map, visited, r as i32 - 1, c as i32, map[r][c] as u8) {
        hike(map, visited, r - 1, c, peaks_visited);
    }

    // Check down
    if is_valid_move(map, visited, r as i32 + 1, c as i32, map[r][c] as u8) {
        hike(map, visited, r + 1, c, peaks_visited);
    }

    // Check left
    if is_valid_move(map, visited, r as i32, c as i32 - 1, map[r][c] as u8) {
        hike(map, visited, r, c - 1, peaks_visited);
    }

    // Check right
    if is_valid_move(map, visited, r as i32, c as i32 + 1, map[r][c] as u8) {
        hike(map, visited, r, c + 1, peaks_visited);
    }

    visited.pop();
    println!("Backtracking from: (r:{}, c:{}) - {}", r, c, map[r][c]);
}

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

fn extract_map(input: &str) -> Vec<Vec<i8>> {
    input.lines()
        .map(|line| line.chars()
            .map(|c| if c == '.' { -1 } else { c.to_digit(10).unwrap() as i8 })
            .collect())
        .collect()
}

fn print_map(map: &Vec<Vec<i8>>) {
    for row in map {
        println!("{:?}", row);
    }
}
