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

    let occurrences_second_map = determine_occurrences(second_numbers);
    let mut total_similarity = 0;

    for i in 0..first_numbers.len() {
        let num = first_numbers[i];
        let second_occurrences = occurrences_second_map.get(&num).unwrap_or(&0);
        let similarity = num * second_occurrences;
        println!("{} * {} = {}", num, second_occurrences, similarity);
        total_similarity += similarity;
    }

    // Print the results
    println!("Total similarity: {}", total_similarity);

    Ok(())
}


/// Determines how many times each number appears in the input vector
/// 
/// # Arguments
/// * `numbers` - A vector of i32 integers to count occurrences from
///
/// # Returns
/// A HashMap mapping each unique number to its count of occurrences
fn determine_occurrences(numbers: Vec<i32>) -> std::collections::HashMap<i32, i32> {
    let mut occurrences_map = std::collections::HashMap::new();
    for i in 0..numbers.len() {
        if !occurrences_map.contains_key(&numbers[i]) {
            occurrences_map.insert(numbers[i], 1);
        } else {
            let count = occurrences_map.get(&numbers[i]).unwrap();
            occurrences_map.insert(numbers[i], count + 1);
        }
    }
    occurrences_map
}
