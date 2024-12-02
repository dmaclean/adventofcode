use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() -> io::Result<()> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = io::BufReader::new(file);

    let mut first_numbers = Vec::new();
    let mut second_numbers = Vec::new();

    // Read the file line by line
    for line in reader.lines() {
        let line = line?;
        // Split the line by whitespace and collect into a vector
        let numbers: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();

        // Add numbers to their respective vectors
        if numbers.len() == 2 {
            first_numbers.push(numbers[0]);
            second_numbers.push(numbers[1]);
        }
    }

    first_numbers.sort();
    second_numbers.sort();

    let mut total_distance = 0;
    for i in 0..first_numbers.len() {
        let distance = (first_numbers[i] - second_numbers[i]).abs();
        total_distance += distance;
    }

    // Print the results
    println!("First numbers: {:?}", first_numbers);
    println!("Second numbers: {:?}", second_numbers);
    println!("Total distance: {}", total_distance);

    Ok(())
}
