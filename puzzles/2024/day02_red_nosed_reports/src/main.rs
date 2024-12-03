use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

/// Processes input file containing level sequences and counts safe sequences.
/// A sequence is considered safe if it's either strictly increasing or decreasing
/// with a maximum difference of 3 between adjacent elements.
fn main() -> io::Result<()> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);

    let mut safe_count = 0;
    for line in reader.lines() {
        let line = line?;
        let levels: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        
        if is_sequence_safe(&levels) {
            safe_count += 1;
            continue;
        }

        // If the original sequence isn't safe, try removing one element
        if try_find_safe_subsequence(&levels) {
            safe_count += 1;
        }
    }

    println!("Safe count: {}", safe_count);
    Ok(())
}

/// Checks if a sequence of levels is safe.
/// 
/// A sequence is considered safe if it meets one of these criteria:
/// - Contains fewer than 2 elements
/// - Is strictly increasing with max difference of 3 between adjacent elements
/// - Is strictly decreasing with max difference of 3 between adjacent elements
///
/// # Arguments
/// * `levels` - A slice of integers representing the sequence to check
///
/// # Returns
/// * `true` if the sequence is safe, `false` otherwise
fn is_sequence_safe(levels: &[i32]) -> bool {
    if levels.len() < 2 {
        return true;
    }

    // Check if increasing with max step of 3
    let is_increasing = levels.windows(2)
        .all(|w| w[0] < w[1] && (w[1] - w[0]).abs() <= 3);
    if is_increasing {
        println!("\x1b[32mIncreasing is safe\x1b[0m");
        return true;
    }

    // Check if decreasing with max step of 3
    let is_decreasing = levels.windows(2)
        .all(|w| w[0] > w[1] && (w[0] - w[1]).abs() <= 3);
    if is_decreasing {
        println!("\x1b[32mDecreasing is safe\x1b[0m");
        return true;
    }

    println!("\x1b[31mNOT SAFE {:?}\x1b[0m", levels);
    false
}

/// Attempts to find a safe subsequence by removing one element.
///
/// # Arguments
/// * `levels` - A slice of integers representing the original sequence
///
/// # Returns
/// * `true` if a safe subsequence is found, `false` otherwise
fn try_find_safe_subsequence(levels: &[i32]) -> bool {
    for i in 0..levels.len() {
        let mut modified = levels.to_vec();
        modified.remove(i);
        if is_sequence_safe(&modified) {
            return true;
        }
    }
    false
}
