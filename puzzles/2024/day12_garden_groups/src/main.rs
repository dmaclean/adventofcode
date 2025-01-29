use std::collections::{HashSet, VecDeque};

#[derive(Clone, Debug)]
struct Plot {
    r: usize,
    c: usize,
    label: char
}

#[derive(Debug)]
struct Region {
    label: char,
    plots: Vec<Plot>
}

fn is_on_grid(r: i32, c: i32, grid: &Vec<Vec<char>>) -> bool {
    if r < 0 || c < 0 {
        return false;
    }
    r < grid.len() as i32 && c < grid[0].len() as i32
}

fn main() {
    let input = std::fs::read_to_string("sample_input.txt").unwrap();
    let grid = input.lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>();
    println!("{:?}", grid);

    let mut queue: VecDeque<Plot> = VecDeque::new();
    let mut secondary_queue: VecDeque<Plot> = VecDeque::new();
    let mut visited: HashSet<(usize, usize)> = HashSet::new();
    let mut regions: Vec<Region> = Vec::new();
    let start = Plot { r: 0, c: 0, label: grid[0][0] };
    secondary_queue.push_back(start);

    while !secondary_queue.is_empty() {
        let popped: Plot = secondary_queue.pop_front().unwrap();
        if visited.contains(&(popped.r, popped.c)) {
            println!("Already visited ({}, {}) {}", popped.r, popped.c, popped.label);
            continue;
        }
        let popped_clone = popped.clone();
        let popped_label = popped.label;
        println!("\n\nMoving from secondary to primary queue: ({}, {}) {}", popped.r, popped.c, popped.label);
        queue.push_back(popped);

        let mut current_region: Region = Region { label: popped_label, plots: Vec::new() };
        current_region.plots.push(popped_clone);
        while !queue.is_empty() {
            let current = queue.pop_front().unwrap();
            println!("Processing plot: ({}, {}) {}", current.r, current.c, current.label);
            if visited.contains(&(current.r, current.c)) {
                println!("Already visited ({}, {}) {}", current.r, current.c, current.label);
                continue;
            }
            visited.insert((current.r, current.c));
            
            // Check UP
            if is_on_grid(current.r as i32 - 1, current.c as i32, &grid) && 
                    !visited.contains(&(current.r - 1, current.c)) {
                let up = Plot { 
                    r: current.r - 1, 
                    c: current.c, 
                    label: grid[current.r - 1][current.c] 
                };
                let up_clone = up.clone();
                if up.label == current.label {
                    println!("Pushing to primary queue (UP): ({}, {}) {}", up.r, up.c, up.label);
                    queue.push_back(up);
                    current_region.plots.push(up_clone);
                } else {
                    println!("Pushing to secondary queue (UP): ({}, {}) {}", up.r, up.c, up.label);
                    secondary_queue.push_back(up);
                }
            }
    
            // Check DOWN
            if is_on_grid(current.r as i32 + 1, current.c as i32, &grid) && 
                    !visited.contains(&(current.r + 1, current.c)) {
                let down = Plot { 
                    r: current.r + 1, 
                    c: current.c, 
                    label: grid[current.r + 1][current.c] 
                };
                let down_clone = down.clone();
                if down.label == current.label {
                    println!("Pushing to primary queue (DOWN): ({}, {}) {}", down.r, down.c, down.label);
                    queue.push_back(down);
                    current_region.plots.push(down_clone);
                } else {
                    println!("Pushing to secondary queue (DOWN): ({}, {}) {}", down.r, down.c, down.label);
                    secondary_queue.push_back(down);
                }
            }
    
            // Check LEFT
            if is_on_grid(current.r as i32, current.c as i32 - 1, &grid) && 
                    !visited.contains(&(current.r, current.c - 1)) {
                let left = Plot { 
                    r: current.r, 
                    c: current.c - 1, 
                    label: grid[current.r][current.c - 1] 
                };
                let left_clone = left.clone();
                if left.label == current.label {
                    println!("Pushing to primary queue (LEFT): ({}, {}) {}", left.r, left.c, left.label);
                    queue.push_back(left);
                    current_region.plots.push(left_clone);
                } else {
                    println!("Pushing to secondary queue (LEFT): ({}, {}) {}", left.r, left.c, left.label);
                    secondary_queue.push_back(left);
                }
            }
    
            // Check RIGHT
            if is_on_grid(current.r as i32, current.c as i32 + 1, &grid) && 
                    !visited.contains(&(current.r, current.c + 1)) {
                let right = Plot { 
                    r: current.r, 
                    c: current.c + 1, 
                    label: grid[current.r][current.c + 1] 
                };
                let right_clone = right.clone();
                if right.label == current.label {
                    println!("Pushing to primary queue (RIGHT): ({}, {}) {}", right.r, right.c, right.label);
                    queue.push_back(right);
                    current_region.plots.push(right_clone);
                } else {
                    println!("Pushing to secondary queue (RIGHT): ({}, {}) {}", right.r, right.c, right.label);
                    secondary_queue.push_back(right);
                }
            }
        }

        regions.push(current_region);
        println!("\nSecondary Queue contents:");
        for plot in &secondary_queue {
            println!("    ({}, {}) -> {}", plot.r, plot.c, plot.label);
        }
    }

    println!("Regions:");
    for (i, region) in regions.iter().enumerate() {
        println!("\nRegion {} (label: {})", i + 1, region.label);
        println!("Plots:");
        for plot in &region.plots {
            println!("    ({}, {}) -> {}", plot.r, plot.c, plot.label);
        }
    }
}

