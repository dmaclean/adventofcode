use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

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
        
        if is_safe(levels) {
            safe_count += 1;
        }
    }

    println!("Safe count: {}", safe_count);

    Ok(())
}


/// Returns true if the levels are either all increasing or all decreasing.
fn is_safe(levels: Vec<i32>) -> bool {
    // Check increasing
    let mut increasing = true;
    for i in 0..levels.len() - 1 {
        if levels[i] >= levels[i + 1] || (levels[i] - levels[i + 1]).abs() > 3 {
            increasing = false;
            break;
        }
    }
    if increasing {
        return true;
    }

    // Check decreasing
    let mut decreasing = true;
    for i in 0..levels.len() - 1 {
        if levels[i] <= levels[i + 1] || (levels[i] - levels[i + 1]).abs() > 3 {
            decreasing = false;
            break;
        }
    }
    decreasing
}
